import { useState } from 'react';

interface TreeNodeData {
  slug: string;
  title: string;
  status: string | null;
  priority: string | null;
  type: string | null;
  owner: string | null;
  due: string | null;
  updated: string | null;
  children: TreeNodeData[];
}

interface Props {
  trees: TreeNodeData[];
}

const statusColors: Record<string, string> = {
  active: '#3b82f6',
  completed: '#22c55e',
  'on-hold': '#9ca3af',
  planning: '#eab308',
  archived: '#d1d5db',
};

const statusBadgeStyles: Record<string, string> = {
  active: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  'on-hold': 'bg-gray-100 text-gray-700',
  planning: 'bg-yellow-100 text-yellow-800',
  archived: 'bg-gray-100 text-gray-500',
};

const priorityBadgeStyles: Record<string, string> = {
  high: 'bg-red-100 text-red-800',
  medium: 'bg-yellow-100 text-yellow-800',
  low: 'bg-gray-100 text-gray-600',
};

function countAll(node: TreeNodeData): number {
  return node.children.reduce((sum, child) => sum + 1 + countAll(child), 0);
}

function TreeNode({ node, depth = 0 }: { node: TreeNodeData; depth?: number }) {
  const [expanded, setExpanded] = useState(depth < 1);
  const hasChildren = node.children.length > 0;
  const today = new Date().toISOString().slice(0, 10);
  const isOverdue = node.due && node.due < today && node.status !== 'completed' && node.status !== 'archived';

  return (
    <div>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.375rem 0.5rem',
          paddingLeft: `${depth * 1.5 + 0.5}rem`,
          borderBottom: '1px solid #f3f4f6',
          cursor: hasChildren ? 'pointer' : 'default',
        }}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        {/* Expand/collapse toggle */}
        <span style={{ width: '1rem', textAlign: 'center', fontSize: '0.75rem', color: '#9ca3af', flexShrink: 0 }}>
          {hasChildren ? (expanded ? '▼' : '▶') : '·'}
        </span>

        {/* Status dot */}
        <span
          style={{
            width: depth === 0 ? '0.5rem' : '0.375rem',
            height: depth === 0 ? '0.5rem' : '0.375rem',
            borderRadius: '50%',
            backgroundColor: statusColors[node.status ?? ''] ?? '#e5e7eb',
            flexShrink: 0,
          }}
        />

        {/* Title */}
        <a
          href={`/project/${node.slug}`}
          onClick={(e) => e.stopPropagation()}
          style={{
            color: '#1f2937',
            textDecoration: 'none',
            fontWeight: depth === 0 ? 600 : 400,
            fontSize: depth === 0 ? '0.875rem' : '0.8125rem',
            flex: 1,
          }}
          onMouseOver={(e) => (e.currentTarget.style.textDecoration = 'underline')}
          onMouseOut={(e) => (e.currentTarget.style.textDecoration = 'none')}
        >
          {node.title}
        </a>

        {/* Child count */}
        {hasChildren && (
          <span style={{ fontSize: '0.6875rem', color: '#9ca3af' }}>
            {countAll(node)} item{countAll(node) !== 1 ? 's' : ''}
          </span>
        )}

        {/* Status badge */}
        {node.status && (
          <span
            className={statusBadgeStyles[node.status] ?? ''}
            style={{ fontSize: '0.6875rem', padding: '0.125rem 0.375rem', borderRadius: '0.25rem', fontWeight: 500 }}
          >
            {node.status}
          </span>
        )}

        {/* Priority badge */}
        {node.priority && (
          <span
            className={priorityBadgeStyles[node.priority] ?? ''}
            style={{ fontSize: '0.6875rem', padding: '0.125rem 0.375rem', borderRadius: '0.25rem', fontWeight: 500 }}
          >
            {node.priority}
          </span>
        )}

        {/* Due date */}
        {node.due && (
          <span style={{
            fontSize: '0.6875rem',
            color: isOverdue ? '#dc2626' : '#6b7280',
            fontWeight: isOverdue ? 600 : 400,
          }}>
            {isOverdue ? '⚠ ' : ''}{node.due}
          </span>
        )}
      </div>

      {/* Children */}
      {expanded && hasChildren && (
        <div>
          {node.children.map((child) => (
            <TreeNode key={child.slug} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function ProjectTree({ trees }: Props) {
  const [filter, setFilter] = useState('all');
  const [expandAll, setExpandAll] = useState(false);

  const filtered = filter === 'all'
    ? trees
    : trees.filter((t) => t.status === filter || t.children.some((c) => c.status === filter));

  // Count top-level by status for quick filters
  const counts: Record<string, number> = {};
  for (const t of trees) {
    const s = t.status ?? 'unset';
    counts[s] = (counts[s] ?? 0) + 1;
  }

  return (
    <div>
      {/* Quick status filters */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
        {['all', 'active', 'planning', 'on-hold', 'completed'].map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            style={{
              padding: '0.25rem 0.75rem',
              borderRadius: '1rem',
              fontSize: '0.8125rem',
              border: filter === s ? '2px solid #3b82f6' : '1px solid #e5e7eb',
              backgroundColor: filter === s ? '#eff6ff' : 'white',
              color: filter === s ? '#2563eb' : '#6b7280',
              cursor: 'pointer',
              fontWeight: filter === s ? 600 : 400,
            }}
          >
            {s === 'all' ? `All (${trees.length})` : `${s} (${counts[s] ?? 0})`}
          </button>
        ))}
      </div>

      {/* Tree */}
      <div style={{ border: '1px solid #e5e7eb', borderRadius: '0.5rem', overflow: 'hidden' }}>
        {filtered.length === 0 ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: '#9ca3af' }}>
            No projects match this filter.
          </div>
        ) : (
          filtered.map((tree) => (
            <TreeNode key={tree.slug} node={tree} depth={0} />
          ))
        )}
      </div>
    </div>
  );
}