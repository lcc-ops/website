// Copy the source-controlled `.assetsignore` into the built dist/ so that
// `wrangler deploy` does not treat `dist/_worker.js/` as uploadable static
// assets (which would abort the deploy).
import { copyFile, mkdir } from "node:fs/promises";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const SRC = new URL("../.assetsignore", import.meta.url);
const DEST = new URL("../dist/.assetsignore", import.meta.url);

await mkdir(dirname(fileURLToPath(DEST)), { recursive: true });
await copyFile(SRC, DEST);
console.log(`synced .assetsignore → ${fileURLToPath(DEST)}`);
