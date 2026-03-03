import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * Absolute path to the docs/ workspace.
 * Trailhead sits as a sibling: dclt-strategic-system-v2/trailhead/
 * Docs live at:               dclt-strategic-system-v2/docs/
 */
export const DOCS_ROOT = path.resolve(__dirname, '../../docs');

/** Frontmatter status values */
export const STATUSES = ['planning', 'active', 'on-hold', 'completed', 'archived'] as const;
export type Status = typeof STATUSES[number];

/** Frontmatter priority values */
export const PRIORITIES = ['high', 'medium', 'low'] as const;
export type Priority = typeof PRIORITIES[number];

/** Frontmatter type values */
export const DOC_TYPES = ['strategy', 'execution', 'reference', 'meeting-note', 'subtask'] as const;
export type DocType = typeof DOC_TYPES[number];