import path from 'node:path';
import type { DocEntry } from './frontmatter';

/** A doc entry with children attached */
export interface TreeNode {
  doc: DocEntry;
  children: TreeNode[];
}

/** Top-level grouping of project trees */
export interface ProjectGroup {
  /** Display name for the group (top-level directory like "01_STRATEGY") */
  groupName: string;
  /** Trees of projects and their subtasks */
  trees: TreeNode[];
}

/**
 * Build a project hierarchy from a flat list of DocEntries.
 *
 * Two linking strategies:
 * 1. Directory nesting — a file inside a project folder is a child of that project.
 * 2. Frontmatter `project:` field — links a file anywhere in docs/ to a parent project slug.
 *
 * Files that aren't children of anything become root-level nodes.
 */
export function buildHierarchy(docs: DocEntry[]): TreeNode[] {
  // Index docs by slug for fast lookup
  const bySlug = new Map<string, DocEntry>();
  for (const doc of docs) {
    bySlug.set(doc.slug, doc);
  }

  // Track which slugs are claimed as children
  const claimed = new Set<string>();

  // Strategy 1: Directory nesting
  // For each doc, find the nearest ancestor .md file in the same directory tree.
  // e.g. "02_EXECUTION/10_Projects/Website_Overhaul/subtasks/migration.md"
  //   -> parent is "02_EXECUTION/10_Projects/Website_Overhaul/Website_Redesign__Release_Plan.md"
  //      (the .md file sitting in the Website_Overhaul directory)
  const parentMap = new Map<string, string>(); // child slug -> parent slug

  for (const doc of docs) {
    // Walk up directory tree looking for a sibling/ancestor .md file
    const parts = doc.slug.split('/');

    // Start from the parent directory of this file
    for (let i = parts.length - 2; i >= 0; i--) {
      const ancestorDir = parts.slice(0, i + 1).join('/');

      // Look for any .md file that lives directly in this ancestor directory
      // (not deeper) — that's the project file for this subtree
      for (const candidate of docs) {
        if (candidate.slug === doc.slug) continue;

        const candidateDir = candidate.slug.substring(0, candidate.slug.lastIndexOf('/'));
        if (candidateDir === ancestorDir && candidate.depth < doc.depth) {
          parentMap.set(doc.slug, candidate.slug);
          break;
        }
      }
      if (parentMap.has(doc.slug)) break;
    }
  }

  // Strategy 2: Frontmatter `project:` field
  // If a doc has project: "website-redesign", find a doc whose slug contains that string
  // or whose tags/title match. This links across directories.
  for (const doc of docs) {
    if (!doc.project || parentMap.has(doc.slug)) continue;

    // Try to find a matching parent by project slug
    const projectSlug = doc.project.toLowerCase();
    for (const candidate of docs) {
      if (candidate.slug === doc.slug) continue;

      const candidateSlugLower = candidate.slug.toLowerCase();
      const candidateTitleSlug = candidate.title.toLowerCase().replace(/\s+/g, '-');

      if (
        candidateSlugLower.includes(projectSlug) ||
        candidateTitleSlug.includes(projectSlug)
      ) {
        // Prefer candidates that look like project-level files (not subtasks themselves)
        if (candidate.type !== 'subtask') {
          parentMap.set(doc.slug, candidate.slug);
          break;
        }
      }
    }
  }

  // Build tree nodes
  const nodeMap = new Map<string, TreeNode>();
  for (const doc of docs) {
    nodeMap.set(doc.slug, { doc, children: [] });
  }

  // Attach children to parents
  for (const [childSlug, parentSlug] of parentMap) {
    const parent = nodeMap.get(parentSlug);
    const child = nodeMap.get(childSlug);
    if (parent && child) {
      parent.children.push(child);
      claimed.add(childSlug);
    }
  }

  // Sort children by priority then title
  for (const node of nodeMap.values()) {
    node.children.sort((a, b) => {
      const pa = priorityWeight(a.doc.priority);
      const pb = priorityWeight(b.doc.priority);
      if (pa !== pb) return pa - pb;
      return a.doc.title.localeCompare(b.doc.title);
    });
  }

  // Root nodes are everything not claimed as a child
  const roots = docs
    .filter((d) => !claimed.has(d.slug))
    .map((d) => nodeMap.get(d.slug)!)
    .sort((a, b) => {
      const pa = priorityWeight(a.doc.priority);
      const pb = priorityWeight(b.doc.priority);
      if (pa !== pb) return pa - pb;
      return a.doc.title.localeCompare(b.doc.title);
    });

  return roots;
}

/**
 * Group root-level trees by their top-level directory
 * (01_STRATEGY, 02_EXECUTION, etc.)
 */
export function groupByTopDir(trees: TreeNode[]): ProjectGroup[] {
  const groups = new Map<string, TreeNode[]>();

  for (const tree of trees) {
    const topDir = tree.doc.slug.split('/')[0] ?? 'Other';
    if (!groups.has(topDir)) groups.set(topDir, []);
    groups.get(topDir)!.push(tree);
  }

  return Array.from(groups.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([groupName, groupTrees]) => ({ groupName, trees: groupTrees }));
}

/**
 * Flatten a tree back into a list (useful for filtering then re-displaying).
 */
export function flattenTree(node: TreeNode): DocEntry[] {
  return [node.doc, ...node.children.flatMap(flattenTree)];
}

/**
 * Count all descendants of a node.
 */
export function countDescendants(node: TreeNode): number {
  return node.children.reduce((sum, child) => sum + 1 + countDescendants(child), 0);
}

// --- Helpers ---

function priorityWeight(p: string | null): number {
  switch (p) {
    case 'high': return 0;
    case 'medium': return 1;
    case 'low': return 2;
    default: return 3;
  }
}