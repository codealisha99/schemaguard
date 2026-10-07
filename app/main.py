"""Stateless, deterministic JSON repair and schema validation."""
import ast
import asyncio
import json
import math
import os
import re
import time
from collections import deque
from pathlib import Path
from threading import Lock
from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, ValidationError

MAX_INPUT = 16_384
MAX_BODY = 65_536
MAX_DEPTH = 32
MAX_NODES = 4096
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
GLOBAL_LIMIT = int(os.getenv("RATE_LIMIT_GLOBAL_PER_MINUTE", "180"))


class DemoModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")


class UserProfile(DemoModel):
    name: Annotated[str, Field(min_length=1, max_length=120)]
    age: Annotated[int, Field(ge=0, le=150)]
    skills: Annotated[list[Annotated[str, Field(max_length=120)]], Field(max_length=50)]


class ProductListing(DemoModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    price: Annotated[float, Field(ge=0, allow_inf_nan=False)]
    currency: Literal["USD", "EUR", "GBP", "INR"]
    in_stock: bool


class SupportTicket(DemoModel):
    subject: Annotated[str, Field(min_length=1, max_length=200)]
    description: Annotated[str, Field(min_length=1, max_length=4000)]
    priority: Literal["low", "medium", "high"]
    tags: Annotated[list[Annotated[str, Field(max_length=80)]], Field(max_length=30)]


SCHEMAS = {m.__name__: m for m in (UserProfile, ProductListing, SupportTicket)}
app = FastAPI(title="SchemaGuard", version="2.0.0", description="Deterministic JSON repair and strict schema validation. No LLM calls.")


class GuardMiddleware:
    """Bound bodies before JSON decoding; bounded ephemeral rate counters, no content."""
    def __init__(self, app):
        self.app = app
        self.clients = {}
        self.global_times = deque()
        self.lock = Lock()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        if scope["method"] == "POST":
            now = time.monotonic()
            key = (scope.get("client") or ("unknown",))[0]
            with self.lock:
                self.clients = {k: q for k, q in self.clients.items() if q and q[-1] > now - 60}
                q = self.clients.get(key, deque())
                for queue in (q, self.global_times):
                    while queue and queue[0] <= now - 60:
                        queue.popleft()
                limited = len(q) >= RATE_LIMIT or len(self.global_times) >= GLOBAL_LIMIT or (key not in self.clients and len(self.clients) >= 2048)
                if not limited:
                    q.append(now)
                    self.global_times.append(now)
                    self.clients[key] = q
            if limited:
                return await JSONResponse({"detail": "Request limit reached. Try again in 60 seconds."}, 429, headers={"Retry-After": "60"})(scope, receive, send)
            chunks, size = [], 0
            while True:
                try:
                    message = await asyncio.wait_for(receive(), timeout=10)
                except TimeoutError:
                    return await JSONResponse({"detail": "Request body timed out."}, 408)(scope, receive, send)
                if message["type"] == "http.disconnect":
                    return
                size += len(message.get("body", b""))
                if size > MAX_BODY:
                    return await JSONResponse({"detail": "Request body exceeds 64 KiB."}, 413)(scope, receive, send)
                chunks.append(message.get("body", b""))
                if not message.get("more_body"):
                    break
            payload = b"".join(chunks)
            # Reject deeply nested request envelopes before FastAPI's JSON decoder.
            try:
                check_depth(payload.decode("utf-8"))
            except (ValueError, UnicodeError):
                return await JSONResponse({"detail": "Request nesting exceeds 32 levels or encoding is invalid."}, 422)(scope, receive, send)
            async def bounded_receive():
                return {"type": "http.request", "body": payload, "more_body": False}
            receive = bounded_receive
        async def secure_send(message):
            if message["type"] == "http.response.start":
                csp = (b"default-src 'self'; script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; img-src 'self' data: https://fastapi.tiangolo.com; frame-ancestors 'none'; base-uri 'none'" if scope["path"].startswith(("/docs", "/redoc")) else b"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
                message["headers"] += [(b"x-content-type-options", b"nosniff"), (b"referrer-policy", b"no-referrer"), (b"cache-control", b"no-store"), (b"content-security-policy", csp)]
            await send(message)
        await self.app(scope, receive, secure_send)


app.add_middleware(GuardMiddleware)


@app.exception_handler(RequestValidationError)
async def request_error(request, exc):
    # Pydantic's default response echoes submitted input. Return metadata only.
    return JSONResponse({"detail": [{"path": ".".join(map(str, e["loc"])), "message": e["msg"], "type": e["type"]} for e in exc.errors()]}, 422)


def check_depth(text):
    depth, quote, escaped = 0, None, False
    for char in text:
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char in "{[":
            depth += 1
            if depth > MAX_DEPTH:
                raise ValueError("Nesting exceeds 32 levels")
        elif char in "}]":
            depth -= 1


def normalize_quotes(text):
    """Convert only quoted string tokens; never evaluate an expression."""
    result, i = [], 0
    while i < len(text):
        if text[i] not in "\"'":
            result.append(text[i]); i += 1; continue
        start, quote = i, text[i]
        i += 1
        while i < len(text):
            if text[i] == "\\":
                i += 2
            elif text[i] == quote:
                i += 1; break
            else:
                i += 1
        token = text[start:i]
        if not token.endswith(quote) or len(token) < 2:
            raise ValueError("Unterminated string")
        if quote == "'":
            # literal_eval is used on one bounded string token, never the submitted object.
            if re.search(r"\\(?![\\'\"bfnrt/])", token):
                raise ValueError("Unsupported single-quoted escape")
            value = ast.literal_eval(token.replace("\\/", "/"))
            result.append(json.dumps(value, ensure_ascii=True))
        else:
            result.append(token)
    return "".join(result)


def remove_trailing_commas(text):
    result, quote, escaped = [], False, False
    for i, char in enumerate(text):
        if quote:
            result.append(char)
            if escaped: escaped = False
            elif char == "\\": escaped = True
            elif char == '"': quote = False
        elif char == '"':
            quote = True; result.append(char)
        elif char == ',' and re.match(r"\s*[}\]]", text[i + 1:]):
            continue
        else:
            result.append(char)
    return "".join(result)


def parse(text):
    check_depth(text)
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValueError("Duplicate object keys are ambiguous")
            obj[key] = value
        return obj
    def invalid_constant(value):
        raise ValueError("Non-finite numbers are not JSON")
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=invalid_constant)
    stack, count = [value], 0
    while stack:
        item = stack.pop(); count += 1
        if count > MAX_NODES: raise ValueError("JSON exceeds 4096 values")
        if isinstance(item, dict): stack.extend(item.values())
        elif isinstance(item, list): stack.extend(item)
        elif isinstance(item, float) and not math.isfinite(item): raise ValueError("Non-finite numbers are not JSON")
    return value


class ValidateIn(BaseModel):
    raw_output: Annotated[str, Field(max_length=MAX_INPUT)]
    schema_name: str = "UserProfile"
    max_retries: Annotated[int, Field(strict=True, ge=0, le=3)] = 3
    fallback: dict | None = None


def errors_for(exc, model, source):
    root = model.model_json_schema()
    result = []
    for error in exc.errors(include_input=False, include_url=False):
        expected = root
        for part in error["loc"]:
            expected = expected.get("items", {}) if isinstance(part, int) else expected.get("properties", {}).get(str(part), {})
        result.append({"path": ".".join(map(str, error["loc"])) or "$", "message": error["msg"], "type": error["type"], "expected": expected, "source": source})
    return result


class FormatIn(BaseModel):
    raw_output: Annotated[str, Field(max_length=MAX_INPUT)]


@app.post("/v1/format")
def format_json(body: FormatIn):
    try:
        return {"formatted": json.dumps(parse(body.raw_output), indent=2, ensure_ascii=False, allow_nan=False)}
    except ValueError:
        raise HTTPException(422, "Formatting requires unambiguous, bounded, valid JSON. Run repair & validate for malformed input.")


@app.get("/health")
def health():
    return {"status": "ok", "service": "schemaguard"}


@app.get("/v1/schemas")
def schemas():
    return {"schemas": list(SCHEMAS), "definitions": {name: model.model_json_schema() for name, model in SCHEMAS.items()}}


@app.post("/v1/validate")
def validate(body: ValidateIn):
    model = SCHEMAS.get(body.schema_name)
    if model is None: raise HTTPException(404, "schema not found")
    steps, errors, retries = [], [], 0
    candidate = body.raw_output.strip()
    def attempt(text, source="input"):
        try:
            value = parse(text)
            steps.append({"stage": "parse", "outcome": "passed", "message": "Parsed JSON successfully.", "attempt": retries})
        except (ValueError, SyntaxError, RecursionError):
            steps.append({"stage": "parse", "outcome": "failed", "message": "Could not parse unambiguous, bounded JSON.", "attempt": retries})
            return None, [{"path": "$", "message": "Invalid or unsafe JSON. Check quotes, delimiters, duplicate keys and resource limits.", "expected": {"type": "object"}, "type": "json_invalid", "source": source}]
        try:
            output = model.model_validate(value).model_dump()
            steps.append({"stage": "validate", "outcome": "passed", "message": f"Validated against {body.schema_name}.", "attempt": retries})
            return output, []
        except ValidationError as exc:
            steps.append({"stage": "validate", "outcome": "failed", "message": "JSON parsed, but fields do not match the schema.", "attempt": retries})
            return None, errors_for(exc, model, source)
    output, errors = attempt(candidate)
    if output is not None:
        status = "valid"
    else:
        transformations = [
            ("fences", "Removed the enclosing Markdown code fence.", lambda s: re.fullmatch(r"```(?:json)?\s*\n?([\s\S]*?)\n?```", s, re.I).group(1).strip() if re.fullmatch(r"```(?:json)?\s*\n?([\s\S]*?)\n?```", s, re.I) else s),
            ("quotes", "Converted single-quoted string tokens to JSON strings.", normalize_quotes),
            ("commas", "Removed trailing commas outside strings.", remove_trailing_commas),
        ]
        # Never try syntax changes after a successful parse / schema mismatch.
        if errors[0]["type"] == "json_invalid":
            for stage, message, transform in transformations:
                if retries >= body.max_retries: break
                try: changed = transform(candidate)
                except (ValueError, SyntaxError): continue
                if changed == candidate: continue
                candidate = changed; retries += 1
                steps.append({"stage": stage, "outcome": "repaired", "message": message, "attempt": retries})
                output, errors = attempt(candidate)
                if output is not None or errors[0]["type"] != "json_invalid": break
        status = "repaired" if output is not None else "failure"
    if status == "failure" and body.fallback is not None:
        try:
            # Enforce the same JSON resource constraints on the request fallback.
            fallback = parse(json.dumps(body.fallback, allow_nan=False))
            output = model.model_validate(fallback).model_dump()
            status = "fallback"
            steps.append({"stage": "fallback", "outcome": "passed", "message": "Validated the explicitly supplied fallback; original input still failed.", "attempt": retries})
        except ValidationError as exc:
            errors += errors_for(exc, model, "fallback")
            steps.append({"stage": "fallback", "outcome": "failed", "message": "Fallback does not match the selected schema.", "attempt": retries})
        except ValueError:
            errors.append({"path": "$", "message": "Fallback exceeds JSON resource limits.", "type": "json_invalid", "expected": {"type": "object"}, "source": "fallback"})
            steps.append({"stage": "fallback", "outcome": "failed", "message": "Fallback exceeds JSON resource limits.", "attempt": retries})
    return {"status": status, "output": output, "validation_errors": errors, "repair_steps": steps, "success": status in ("valid", "repaired"), "data": output, "retries": retries, "fallback": status == "fallback", "repair_log": steps, "error": errors[0]["message"] if errors else None}


STATIC = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def playground():
    return FileResponse(STATIC / "index.html")
