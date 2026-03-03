import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { DOCS_ROOT, type Status, type Priority, type DocType } from '../config';

/** Shape of parsed frontmatter from a markdown file */
export interface DocEntry {
  /** Absolute file path */
  filepath: string;
  /** Path relative to docs/ root (used as slug) */
  slug: string;
  /** Directory depth relative to docs/ */
  depth: number;
  /** Parent directory name */
  parentDir: string;

  // Frontmatter fields
  title: string;
  type: DocType | null;
  project: string | null;
  status: Status | null;
  priority: Priority | null;
  owner: string | null;
  created: string | null;
  updated: string | null;
  due: string | null;
  related: string[];
  tags: string[];

  /** Has any frontmatter at all */
  hasFrontmatter: boolean;
  /** Raw markdown body (without frontmatter) */
  body: string;
}

/**
 * Recursively find all .md files under a directory.
 */
function walkMarkdown(dir: string): string[] {
  const results: string[] = [];

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);

    // Skip hidden dirs, _archive, node_modules
    if (entry.name.startsWith('.') || entry.name === '_archive' || entry.name === 'node_modules') {
      continue;
    }

    if (entry.isDirectory()) {
      results.push(...walkMarkdown(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      results.push(fullPath);
    }
  }

  return results;
}

/**
 * Parse a single markdown file into a DocEntry.
 */
function parseFile(filepath: string): DocEntry {
  const raw = fs.readFileSync(filepath, 'utf-8');
  const relativePath = path.relative(DOCS_ROOT, filepath);
  const slug = relativePath.replace(/\.md$/, '');
  const parts = relativePath.split(path.sep);

  let frontmatter: Record<string, unknown> = {};
  let body = raw;
  let hasFrontmatter = false;

  try {
    const parsed = matter(raw);
    frontmatter = parsed.data;
    body = parsed.content;
    hasFrontmatter = Object.keys(frontmatter).length > 0;
  } catch {
    // If frontmatter parsing fails, treat as plain markdown
  }

  return {
    filepath,
    slug,
    depth: parts.length - 1,
    parentDir: parts.length > 1 ? parts[parts.length - 2] : '',

    title: asString(frontmatter.title) ?? filenameToTitle(path.basename(filepath, '.md')),
    type: asString(frontmatter.type) as DocType | null,
    project: asString(frontmatter.project),
    status: asString(frontmatter.status) as Status | null,
    priority: asString(frontmatter.priority) as Priority | null,
    owner: asString(frontmatter.owner),
    created: asDateString(frontmatter.created),
    updated: asDateString(frontmatter.updated),
    due: asDateString(frontmatter.due),
    related: asStringArray(frontmatter.related),
    tags: asStringArray(frontmatter.tags),

    hasFrontmatter,
    body,
  };
}

/**
 * Load and parse all markdown files from the docs/ workspace.
 * This is the main entry point — call it from any Astro page.
 */
export function loadAllDocs(): DocEntry[] {
  const files = walkMarkdown(DOCS_ROOT);
  return files.map(parseFile).sort((a, b) => a.slug.localeCompare(b.slug));
}

/**
 * Filter helpers for common queries.
 */
export function getByStatus(docs: DocEntry[], status: Status): DocEntry[] {
  return docs.filter((d) => d.status === status);
}

export function getOverdue(docs: DocEntry[]): DocEntry[] {
  const today = new Date().toISOString().slice(0, 10);
  return docs.filter((d) => d.due && d.due < today && d.status !== 'completed' && d.status !== 'archived');
}

export function getStale(docs: DocEntry[], daysThreshold = 30): DocEntry[] {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - daysThreshold);
  const cutoffStr = cutoff.toISOString().slice(0, 10);
  return docs.filter((d) => {
    const lastTouch = d.updated ?? d.created;
    return lastTouch && lastTouch < cutoffStr && d.status === 'active';
  });
}

// --- Utility helpers ---

function asString(val: unknown): string | null {
  if (typeof val === 'string' && val.trim() !== '') return val.trim();
  return null;
}

function asDateString(val: unknown): string | null {
  if (val instanceof Date) return val.toISOString().slice(0, 10);
  if (typeof val === 'string' && /^\d{4}-\d{2}-\d{2}/.test(val)) return val.slice(0, 10);
  return null;
}

function asStringArray(val: unknown): string[] {
  if (Array.isArray(val)) return val.filter((v) => typeof v === 'string');
  return [];
}

/** Convert a filename like "Brand_System_2026" to "Brand System 2026" */
function filenameToTitle(name: string): string {
  return name.replace(/[-_]+/g, ' ').replace(/\s+/g, ' ').trim();
}