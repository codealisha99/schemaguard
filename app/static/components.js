/* Lightweight adaptations of Aceternity UI components by Manu Arora.
 * Sources and adaptation notes: THIRD_PARTY_NOTICES.md.
 * DOM + Web Animations replace React/Motion; no submitted text becomes HTML.
 */
"use strict";
(() => {
  const reducedMotion = () =>
    matchMedia("(prefers-reduced-motion: reduce)").matches;
  const feedbackTimers = new WeakMap();
  function icon(kind) {
    const svg = Hugeicons.create(
      {
        loading: "loading",
        passed: "check",
        failure: "alert",
        fallback: "fallback",
        idle: "arrow",
      }[kind],
    );
    svg.classList.add("run-icon");
    if (kind === "loading") svg.classList.add("run-spinner");
    return svg;
  }

  function renderRunButton(button, state = "idle") {
    clearTimeout(feedbackTimers.get(button));
    button.dataset.state = state;
    const labels = {
      idle: "Repair & validate",
      loading: "Validating…",
      valid: "Validated",
      repaired: "Repaired & validated",
      fallback: "Fallback used",
      failure: "Review input",
    };
    const kind = ["valid", "repaired"].includes(state) ? "passed" : state;
    const content = document.createElement("span");
    content.className = "run-content";
    const label = document.createElement("span");
    label.className = "run-label";
    label.textContent = labels[state];
    button.setAttribute("aria-label", labels[state]);
    content.append(icon(kind), label);
    button.replaceChildren(content);
    if (!reducedMotion() && state !== "idle")
      content.animate(
        [
          { opacity: 0.5, transform: "translateY(3px)" },
          { opacity: 1, transform: "translateY(0)" },
        ],
        { duration: 160, easing: "ease-out" },
      );
    if (!["idle", "loading"].includes(state))
      feedbackTimers.set(
        button,
        setTimeout(() => {
          if (button.dataset.state === state) renderRunButton(button, "idle");
        }, 2200),
      );
  }

  function createSchemaTabs(container, select, panel) {
    const activeSurface = document.createElement("span");
    activeSurface.className = "schema-tab-surface";
    activeSurface.setAttribute("aria-hidden", "true");
    const buttons = Array.from(select.options, (option) => {
      const button = document.createElement("button");
      button.type = "button";
      button.id = `tab-${option.value}`;
      button.className = "schema-tab";
      button.dataset.schema = option.value;
      button.setAttribute("role", "tab");
      button.setAttribute("aria-controls", panel.id);
      const label = document.createElement("span");
      label.className = "schema-tab-label";
      label.textContent = option.textContent;
      button.append(label);
      container.append(button);
      button.addEventListener("click", () => {
        if (select.value !== option.value) {
          select.value = option.value;
          select.dispatchEvent(new Event("change"));
        }
      });
      return button;
    });
    function sync(animate = true) {
      const old = activeSurface.isConnected
        ? activeSurface.getBoundingClientRect()
        : null;
      const selected = buttons.find(
        (button) => button.dataset.schema === select.value,
      );
      for (const button of buttons) {
        const active = button === selected;
        button.setAttribute("aria-selected", String(active));
        button.tabIndex = active ? 0 : -1;
      }
      activeSurface.getAnimations().forEach((animation) => animation.cancel());
      selected.prepend(activeSurface);
      panel.setAttribute("aria-labelledby", selected.id);
      const current = activeSurface.getBoundingClientRect();
      if (old && animate && !reducedMotion())
        activeSurface.animate(
          [
            {
              transform: `translate(${old.x - current.x}px, ${old.y - current.y}px) scaleX(${old.width / current.width})`,
            },
            { transform: "translate(0, 0) scaleX(1)" },
          ],
          { duration: 320, easing: "cubic-bezier(.22,1,.36,1)" },
        );
    }
    container.addEventListener("keydown", (event) => {
      if (
        !["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key) ||
        select.disabled
      )
        return;
      event.preventDefault();
      const index = buttons.indexOf(document.activeElement);
      let next = index;
      if (event.key === "Home") next = 0;
      else if (event.key === "End") next = buttons.length - 1;
      else
        next =
          (index + (event.key === "ArrowRight" ? 1 : -1) + buttons.length) %
          buttons.length;
      buttons[next].focus();
      buttons[next].click();
    });
    select.addEventListener("change", () => sync());
    sync(false);
  }

  window.SchemaGuardUI = { renderRunButton, createSchemaTabs };
})();
