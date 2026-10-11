import { cp, mkdir, rm, readFile, writeFile } from "node:fs/promises";

await rm("dist", { recursive: true, force: true });
await mkdir("dist", { recursive: true });
await cp("app/static", "dist/static", { recursive: true });
await cp("app/static/index.html", "dist/index.html");
const template = await readFile("app/static/index.html", "utf8");
await writeFile("dist/playground.html", template
  .replace('data-page="landing"', 'data-page="playground"')
  .replace("SchemaGuard · Turn messy output into validated JSON", "Playground · SchemaGuard"));
