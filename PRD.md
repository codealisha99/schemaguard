# SchemaGuard public demo

Visitors can turn malformed LLM-style output into validated JSON in under a minute, with three built-in schemas, editable examples, field-level issues, explicit fallback, and an actual repair timeline.

The service is deterministic and stateless. It calls no LLM and requires no keys. Conservative repairs cover enclosing Markdown fences, single-quoted string tokens, and trailing commas. Strict Pydantic validation rejects missing/extra fields and wrong types. Invalid fallback objects are rejected. Size, depth, retry, connection, and request-rate limits are enforced on the server.

The responsive playground and API ship in one FastAPI Docker service. See README.md for execution, API semantics, safety boundaries, and Railway deployment; see VERIFICATION.md for checked results.
