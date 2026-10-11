import assert from "node:assert/strict";
import { readFile, access } from "node:fs/promises";
import { spawnSync } from "node:child_process";

for (const file of [
  "app/static/app.js",
  "app/static/components.js",
  "app/static/hugeicons.js",
  "scripts/build-frontend.mjs",
]) {
  const result = spawnSync(process.execPath, ["--check", file], {
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr);
}

const css = await readFile("app/static/tokens.css", "utf8");
const tokens = Object.fromEntries(
  [...css.matchAll(/--([\w-]+):\s*(#[\da-f]{6})/gi)].map((match) => [
    match[1],
    match[2],
  ]),
);
function luminance(hex) {
  const channels = [1, 3, 5].map(
    (offset) => parseInt(hex.slice(offset, offset + 2), 16) / 255,
  );
  const linear = channels.map((channel) =>
    channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4,
  );
  return linear.reduce(
    (sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index],
    0,
  );
}
function contrast(foreground, background) {
  const [dark, light] = [
    luminance(tokens[foreground]),
    luminance(tokens[background]),
  ].sort((a, b) => a - b);
  return (light + 0.05) / (dark + 0.05);
}
const textPairs = [
  ["ink", "page"],
  ["text", "page"],
  ["muted", "page"],
  ["muted", "surface"],
  ["brand", "page"],
  ["brand", "selected"],
  ["page", "brand"],
  ["page", "brand-hover"],
  ["page", "success"],
  ["page", "warning"],
  ["page", "error"],
  ["success", "success-bg"],
  ["warning", "warning-bg"],
  ["error", "error-bg"],
  ["info", "info-bg"],
  ["code-text", "code"],
  ["code-text", "code-surface"],
  ["code-muted", "code"],
  ["code-muted", "code-surface"],
  ["code-key", "code"],
  ["code-string", "code"],
  ["code-number", "code"],
  ["code-literal", "code"],
  ["code-success", "code-success-bg"],
  ["code-warning", "code-warning-bg"],
  ["code-error", "code-error-bg"],
];
for (const pair of textPairs)
  assert(contrast(...pair) >= 4.5, `${pair.join("/")} fails AA text contrast`);
for (const pair of [
  ["border-strong", "page"],
  ["focus", "page"],
  ["code-key", "code"],
]) {
  assert(contrast(...pair) >= 3, `${pair.join("/")} fails non-text contrast`);
}

for (const [file, page] of [
  ["dist/index.html", "landing"],
  ["dist/playground.html", "playground"],
]) {
  const html = await readFile(file, "utf8");
  assert(html.includes(`data-page="${page}"`));
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(ids).size, ids.length, `${file} has duplicate IDs`);
  for (const match of html.matchAll(
    /(?:href|src)="(\/static\/[^"?]+)(?:\?[^" ]*)?"/g,
  )) {
    await access(`dist${match[1]}`);
  }
  for (const match of html.matchAll(
    /(?:aria-controls|aria-labelledby|aria-describedby)="([^"]+)"/g,
  )) {
    for (const id of match[1].split(" "))
      assert(ids.includes(id), `${file} has a broken ARIA reference: ${id}`);
  }
}
const minimum = Math.min(...textPairs.map((pair) => contrast(...pair)));
console.log(
  `Frontend checks passed: JavaScript syntax, both build outputs, assets, ARIA references, and ${textPairs.length} text contrast pairs (minimum ${minimum.toFixed(2)}:1).`,
);
