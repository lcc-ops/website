// Build a static search index from src/content (blog + tools) and write it to
// public/search-index.json. Runs in postbuild, no external dependencies — keeps
// the SSR/Cloudflare Pages deploy workflow untouched.
//
// Index shape (consumed by SearchDialog.astro):
//   [{ url, locale, title, description, category, tags, excerpt, body }]

import { readFile, readdir, writeFile, mkdir } from "node:fs/promises";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(fileURLToPath(import.meta.url), "..", "..");
const CONTENT = join(ROOT, "src", "content");
const OUT = join(ROOT, "public", "search-index.json");

const LOCALES = ["en", "zh"];

// Per-build timestamp suffix. Append as ?v=… to the fetch URL so the
// browser never serves a stale index across deploys (the asset itself is
// re-emitted on every build so the file URL is stable, but the cache
// key needs to change).
const BUILD_ID = Date.now().toString(36);

/**
 * Extract the YAML frontmatter block from a Markdown file as a plain object.
 * Minimal hand-rolled parser — we only need string / array / scalar fields the
 * search dialog actually displays. Avoids pulling in a YAML library.
 */
function parseFrontmatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return {};
  const block = match[1];
  const data = {};
  const lines = block.split(/\r?\n/);
  let currentKey = null;
  let currentList = null;
  for (const line of lines) {
    if (!line.trim()) continue;
    const listItem = line.match(/^\s*-\s+(.*)$/);
    if (listItem && currentList) {
      currentList.push(unquote(listItem[1]));
      continue;
    }
    const kv = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$/);
    if (!kv) continue;
    const [, key, rawValue] = kv;
    const value = rawValue.trim();
    if (value === "" || value === "|" || value === ">") {
      // could be a list or block scalar; assume list unless next non-blank line
      // is a "key: value" continuation. For our schema, empty value == list.
      currentList = [];
      data[key] = currentList;
      currentKey = key;
      continue;
    }
    if (value.startsWith("[") && value.endsWith("]")) {
      data[key] = value
        .slice(1, -1)
        .split(",")
        .map((s) => unquote(s.trim()))
        .filter(Boolean);
      currentList = null;
      currentKey = null;
      continue;
    }
    data[key] = unquote(value);
    currentList = null;
    currentKey = key;
  }
  return data;
}

function unquote(v) {
  const s = v.trim();
  if (
    (s.startsWith("'") && s.endsWith("'")) ||
    (s.startsWith('"') && s.endsWith('"'))
  ) {
    return s.slice(1, -1);
  }
  return s;
}

/**
 * Strip Markdown punctuation to produce a readable excerpt. Not perfect; good
 * enough for "matches contain this text" search.
 */
function stripMarkdown(s) {
  return s
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`[^`]*`/g, " ")
    .replace(/!\[[^\]]*]\([^)]*\)/g, " ")
    .replace(/\[([^\]]+)]\([^)]*\)/g, "$1")
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/^\s*[-*+]\s+/gm, "")
    .replace(/^\s*\d+\.\s+/gm, "")
    // Markdown tables: drop separator rows (|---|---|) and pipe-fragment cells
    .replace(/^\s*\|?[\s:|-]+\|?[\s:|-]*\s*$/gm, " ")
    .replace(/\|/g, " ")
    .replace(/[*_~>]+/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

async function walk(dir) {
  const out = [];
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...(await walk(full)));
    } else if (entry.name.endsWith(".md") || entry.name.endsWith(".mdx")) {
      out.push(full);
    }
  }
  return out;
}

function buildUrl({ collection, slug, locale }) {
  const prefix = locale === "en" ? "" : "/zh";
  const path = collection === "tools" ? "/tools" : "/content";
  return `${prefix}${path}/${slug}/`;
}

async function indexCollection(collection) {
  const base = join(CONTENT, collection);
  const files = await walk(base);
  const records = [];
  for (const file of files) {
    const rel = relative(base, file);
    const parts = rel.split(/[\\/]/);
    if (parts.length < 2) continue;
    const slug = parts[0];
    const fileName = parts[parts.length - 1];
    const localeMatch = fileName.match(/^(en|zh)\.mdx?$/);
    if (!localeMatch) continue;
    const locale = localeMatch[1];
    const raw = await readFile(file, "utf8");
    const fm = parseFrontmatter(raw);
    if (fm.draft === "true" || fm.draft === true) continue;
    const body = stripMarkdown(raw.replace(/^---[\s\S]*?---\r?\n?/, ""));
    records.push({
      url: buildUrl({ collection, slug, locale }),
      locale,
      title: fm.title ?? slug,
      description: fm.description ?? "",
      category: fm.category ?? "",
      tags: Array.isArray(fm.tags) ? fm.tags : [],
      excerpt: body.slice(0, 100),
      body: body.slice(0, 1200),
    });
  }
  return records;
}

const blog = await indexCollection("blog");
const tools = await indexCollection("tools");
const all = [...blog, ...tools].sort((a, b) => a.title.localeCompare(b.title));

await mkdir(dirname(OUT), { recursive: true });
await writeFile(OUT, JSON.stringify(all, null, 2), "utf8");
console.log(`search index: ${all.length} entries (${blog.length} blog, ${tools.length} tools) → ${relative(ROOT, OUT)} (build ${BUILD_ID})`);
