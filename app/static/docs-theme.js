"use strict";
(() => {
  const viewer = document.querySelector("redoc");
  if (!viewer) return;
  const styles = getComputedStyle(document.documentElement);
  const token = (name) => styles.getPropertyValue(`--${name}`).trim();
  viewer.setAttribute(
    "theme",
    JSON.stringify({
      colors: {
        primary: { main: token("brand") },
        success: { main: token("success") },
        error: { main: token("error") },
        warning: { main: token("warning") },
        text: { primary: token("ink"), secondary: token("muted") },
        http: { get: token("info"), post: token("brand") },
      },
      typography: {
        fontFamily: token("font"),
        fontSize: token("text-sm"),
        headings: { fontFamily: token("font"), fontWeight: "650" },
        code: { fontFamily: token("mono"), color: token("error"), wrap: true },
        links: { color: token("brand"), hover: token("brand-hover") },
      },
      sidebar: {
        backgroundColor: token("surface"),
        textColor: token("text"),
        activeTextColor: token("brand"),
      },
      rightPanel: {
        backgroundColor: token("code"),
        textColor: token("code-text"),
      },
    }),
  );
})();
