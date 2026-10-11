import { cp, mkdir, rm } from "node:fs/promises";

await rm("dist", { recursive: true, force: true });
await mkdir("dist", { recursive: true });
await cp("app/static", "dist/static", { recursive: true });
await cp("app/static/index.html", "dist/index.html");
