"use strict";
const $ = (id) => document.getElementById(id);
const samples = {
  UserProfile: {
    name: "Alisha Chen",
    age: 30,
    skills: ["Python", "TypeScript"],
  },
  ProductListing: {
    title: "Mechanical keyboard",
    price: 89.99,
    currency: "USD",
    in_stock: true,
  },
  SupportTicket: {
    subject: "Unable to sign in",
    description: "The reset link has expired.",
    priority: "high",
    tags: ["account", "login"],
  },
};
const labels = {
  valid: "Valid JSON",
  fences: "Markdown fences",
  commas: "Trailing commas",
  quotes: "Single quotes",
  mismatch: "Schema mismatch",
  broken: "Unrecoverable",
};
let definitions = {},
  busy = false,
  lastOutput = null,
  controller = null;
const pretty = (value) => JSON.stringify(value, null, 2);
function example(kind) {
  const obj = structuredClone(samples[$("schema").value]);
  const json = pretty(obj);
  if (kind === "fences") return "```json\n" + json + "\n```";
  if (kind === "commas") return json.replace(/\n}$/, ",\n}");
  if (kind === "quotes") return json.replaceAll('"', "'");
  if (kind === "mismatch") {
    delete obj[Object.keys(obj)[0]];
    obj.age = "not a number";
    return pretty(obj);
  }
  if (kind === "broken")
    return 'Here is the result: { "unfinished": [\nI could not complete this response.';
  return json;
}
function count() {
  const raw = $("input").value;
  $("count").textContent = `${raw.length.toLocaleString("en-US")} / 16,384`;
  const lines = Math.min(raw.split("\n").length, 4096);
  $("line-numbers").textContent = Array.from(
    { length: lines },
    (_, i) => i + 1,
  ).join("\n");
  $("line-numbers").scrollTop = $("input").scrollTop;
}
$("input").addEventListener("scroll", () => {
  $("line-numbers").scrollTop = $("input").scrollTop;
});
function renderOutput(value, message = "No schema-valid output.") {
  const pre = $("output");
  pre.replaceChildren();
  pre.tabIndex = value === null ? -1 : 0;
  if (value === null) {
    pre.textContent = message;
    return;
  }
  const json = pretty(value);
  const tokens =
    /"(?:\\.|[^"\\])*"(?=\s*:)|"(?:\\.|[^"\\])*"|\b(?:true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/g;
  let end = 0;
  for (const match of json.matchAll(tokens)) {
    pre.append(document.createTextNode(json.slice(end, match.index)));
    const token = document.createElement("span");
    token.textContent = match[0];
    token.className =
      match[0][0] === '"'
        ? /^\s*:/.test(json.slice(match.index + match[0].length))
          ? "token-key"
          : "token-string"
        : /^(true|false|null)$/.test(match[0])
          ? "token-literal"
          : "token-number";
    pre.append(token);
    end = match.index + match[0].length;
  }
  pre.append(document.createTextNode(json.slice(end)));
}
function clearResult() {
  SchemaGuardUI.renderRunButton($("run"));
  lastOutput = null;
  $("copy").disabled = true;
  $("errors-section").hidden = true;
  document.querySelector(".output-panel").dataset.state = "neutral";
  $("duration").textContent = "";
  $("result-status").className = "status neutral";
  $("result-status").textContent = "Ready to validate";
  $("result-description").textContent =
    "Run the example to see validated JSON and a step-by-step repair trace.";
  renderOutput(null, "Your result will appear here.");
  $("result-meta").textContent = "Only schema-valid objects appear here";
  $("timeline").replaceChildren();
  addStep(
    "Waiting for input",
    "Run validation to inspect the actual pipeline.",
    "pending",
    "·",
  );
  $("attempts").textContent = "Every attempt, accounted for";
  $("notice").textContent = "";
}
function addStep(title, description, outcome, symbol) {
  const li = document.createElement("li");
  li.className = outcome;
  const dot = document.createElement("span");
  dot.className = "step-dot";
  dot.textContent = symbol;
  const text = document.createElement("div");
  text.textContent = title;
  const detail = document.createElement("span");
  detail.textContent = description;
  text.append(detail);
  li.append(dot, text);
  $("timeline").append(li);
}
function loadExample(kind) {
  $("input").value = example(kind);
  count();
  clearResult();
  document.querySelectorAll(".example").forEach((button) => {
    const active = button.dataset.kind === kind;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}
for (const [kind, label] of Object.entries(labels)) {
  const button = document.createElement("button");
  button.className = "example";
  button.textContent = label;
  button.dataset.kind = kind;
  button.setAttribute("aria-pressed", "false");
  button.addEventListener("click", () => loadExample(kind));
  $("examples").append(button);
}
function updateSchema() {
  $("schema-view").textContent = definitions[$("schema").value]
    ? pretty(definitions[$("schema").value])
    : "Schema definitions unavailable. Open /docs for API details.";
  $("fallback-view").textContent = pretty(samples[$("schema").value]);
  $("schema-fields").textContent = Object.keys(samples[$("schema").value]).join(
    " · ",
  );
  loadExample("fences");
}
$("schema").addEventListener("change", updateSchema);
$("input").addEventListener("input", () => {
  count();
  clearResult();
  document.querySelectorAll(".example").forEach((b) => {
    b.classList.remove("active");
    b.setAttribute("aria-pressed", "false");
  });
});
$("use-fallback").addEventListener("change", () => {
  clearResult();
  $("fallback-details").open = $("use-fallback").checked;
});
$("reset").addEventListener("click", () => {
  $("use-fallback").checked = false;
  $("fallback-details").open = false;
  loadExample("fences");
});
$("format").addEventListener("click", async () => {
  if (busy) return;
  setBusy(true);
  const abort = new AbortController(),
    timeout = setTimeout(() => abort.abort(), 15000);
  try {
    const response = await fetch("/v1/format", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ raw_output: $("input").value }),
      signal: abort.signal,
    });
    if (!response.ok)
      throw Error(
        response.status === 429
          ? "Request limit reached. Wait 60 seconds and try again."
          : "Formatting requires unambiguous, valid JSON. Run repair & validate for malformed input.",
      );
    $("input").value = (await response.json()).formatted;
    count();
    clearResult();
    $("notice").textContent =
      "Input formatted. Run validation to check the schema.";
  } catch (error) {
    $("notice").textContent =
      error.name === "AbortError"
        ? "Formatting timed out. Try again."
        : error.message;
  } finally {
    clearTimeout(timeout);
    setBusy(false);
  }
});
async function copy(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    const original = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => {
      button.textContent = original;
    }, 1500);
  } catch {
    $("notice").textContent =
      "Clipboard unavailable. Select and copy the text manually.";
  }
}
$("copy").addEventListener("click", () => {
  if (lastOutput !== null) copy(pretty(lastOutput), $("copy"));
});
const apiRequest = `curl -X POST '${location.origin}/v1/validate' \\\n  -H 'Content-Type: application/json' \\\n  -d '{"raw_output":"{\\"name\\":\\"Alisha\\",\\"age\\":30,\\"skills\\":[\\"Python\\"]}","schema_name":"UserProfile","max_retries":3}'`;
$("api-request").textContent = apiRequest;
$("copy-request").addEventListener("click", () =>
  copy(apiRequest, $("copy-request")),
);
function setBusy(value, outcome = "idle") {
  busy = value;
  document
    .querySelectorAll("button, select, textarea, #use-fallback")
    .forEach((el) => (el.disabled = value));
  $("copy").disabled = value || lastOutput === null;
  SchemaGuardUI.renderRunButton($("run"), value ? "loading" : outcome);
  $("run").setAttribute("aria-busy", String(value));
  $("result").setAttribute("aria-busy", String(value));
}
$("run").addEventListener("click", async () => {
  if (busy) return;
  clearResult();
  if (!$("input").value.trim()) {
    $("notice").textContent = "Paste JSON or choose an example to begin.";
    $("input").focus();
    return;
  }
  if ($("input").value.length > 16384) {
    $("notice").textContent =
      "Input exceeds 16,384 characters. Shorten it and try again.";
    return;
  }
  let outcome = "idle";
  const started = performance.now();
  document.querySelector(".output-panel").dataset.state = "loading";
  renderOutput(null, "Processing input…");
  setBusy(true);
  $("result-status").textContent = "Validating…";
  $("result-description").textContent =
    "Parsing your input and checking the selected schema.";
  controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const body = {
      raw_output: $("input").value,
      schema_name: $("schema").value,
      max_retries: 3,
    };
    if ($("use-fallback").checked) body.fallback = samples[$("schema").value];
    const response = await fetch("/v1/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    if (!response.ok)
      throw new Error(
        response.status === 429
          ? "Request limit reached. Wait 60 seconds and try again."
          : response.status === 413
            ? "Request is too large. Shorten the input."
            : `Request failed (${response.status}). Check your input and try again.`,
      );
    const result = await response.json();
    outcome = result.status;
    const messages = {
      valid: [
        "Valid input",
        "Your input parsed directly and matches the schema.",
      ],
      repaired: [
        "Repaired input",
        "Syntax repaired. The resulting object matches the schema.",
      ],
      fallback: [
        "Fallback used",
        "Original input failed. Showing the explicitly supplied, validated sample fallback.",
      ],
      failure: [
        "Validation failed",
        "No validated output. Review the issues below or choose another example.",
      ],
    };
    document.querySelector(".output-panel").dataset.state = result.status;
    $("duration").textContent =
      `${Math.max(1, Math.round(performance.now() - started))} ms`;
    $("duration").title = "Request round-trip time";
    $("result-status").className = `status ${result.status}`;
    $("result-status").textContent = messages[result.status][0];
    $("result-description").textContent = messages[result.status][1];
    lastOutput = result.output;
    renderOutput(result.output);
    $("result-meta").textContent =
      `${$("schema").selectedOptions[0].textContent} · ${result.retries} repair${result.retries === 1 ? "" : "s"} · ${result.fallback ? "Sample fallback" : "Original input"}`;
    $("timeline").replaceChildren();
    result.repair_steps.forEach((s, i) =>
      addStep(
        s.message,
        `Attempt ${s.attempt + 1} · ${s.stage} · ${s.outcome}`,
        s.outcome,
        s.outcome === "passed"
          ? "✓"
          : s.outcome === "failed"
            ? "!"
            : String(i + 1),
      ),
    );
    $("attempts").textContent = `${result.repair_steps.length} recorded steps`;
    $("errors").replaceChildren();
    $("errors-section").hidden = result.validation_errors.length === 0;
    for (const error of result.validation_errors) {
      const li = document.createElement("li"),
        path = document.createElement("strong"),
        detail = document.createElement("span");
      path.textContent = `${error.source === "fallback" ? "Fallback · " : ""}${error.path}`;
      detail.textContent = `${error.message} Expected: ${error.expected.enum ? error.expected.enum.join(" | ") : error.expected.type || "schema constraint"}.`;
      li.append(path, detail);
      $("errors").append(li);
    }
  } catch (error) {
    outcome = "failure";
    document.querySelector(".output-panel").dataset.state = "failure";
    $("result-status").className = "status failure";
    $("result-status").textContent = "Request failed";
    $("result-description").textContent =
      error.name === "AbortError"
        ? "Request timed out. Please try again."
        : error instanceof TypeError
          ? "Could not reach the service. Check your connection and try again."
          : error.message;
    renderOutput(null, "No result received.");
  } finally {
    clearTimeout(timeout);
    setBusy(false, outcome);
    if (matchMedia("(max-width: 650px)").matches) {
      document.querySelector(".output-panel").scrollIntoView({
        block: "center",
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "instant"
          : "smooth",
      });
    }
  }
});
updateSchema();
fetch("/v1/schemas")
  .then((r) => {
    if (!r.ok) throw Error();
    return r.json();
  })
  .then((data) => {
    definitions = data.definitions;
    $("schema-view").textContent = pretty(definitions[$("schema").value]);
  })
  .catch(() => {
    $("schema-view").textContent =
      "Could not load schema definitions. Reload the page or open /docs.";
  });

// Native platform shortcut; the button remains the primary, accessible action.
const isMac = /Mac|iPhone|iPad/.test(navigator.platform);
document.querySelector(".shortcut kbd").textContent = isMac ? "⌘" : "Ctrl";
document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    event.preventDefault();
    if (!busy) $("run").click();
  }
});
fetch("/health")
  .then((response) => {
    if (!response.ok) throw Error();
    return response.json();
  })
  .then(() => {
    const dot = document.createElement("span");
    dot.className = "signal";
    $("service-state").replaceChildren(
      dot,
      document.createTextNode("Service online"),
    );
  })
  .catch(() => {
    $("service-state").classList.add("offline");
    $("service-state").textContent = "Service unavailable";
  });

const schemaDetails = document.querySelector(".schema-details");
document.addEventListener("click", (event) => {
  if (!schemaDetails.contains(event.target)) schemaDetails.open = false;
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && schemaDetails.open) {
    schemaDetails.open = false;
    schemaDetails.querySelector("summary").focus();
  }
});

SchemaGuardUI.createSchemaTabs(
  $("schema-tabs"),
  $("schema"),
  $("schema-panel"),
);
SchemaGuardUI.initHoverCards(document.querySelector(".how-grid"));
