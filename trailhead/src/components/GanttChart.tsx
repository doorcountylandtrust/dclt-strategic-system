import { useState, useMemo, useRef } from 'react';

interface GanttItem {
  slug: string;
  title: string;
  status: string | null;
  priority: string | null;
  type: string | null;
  owner: string | null;
  created: string | null;
  due: string | null;
  updated: string | null;
  depth: number;
}

interface Props {
  items: GanttItem[];
}

const barColors: Record<string, string> = {
  active: '#3b82f6',
  completed: '#22c55e',
  'on-hold': '#9ca3af',
  planning: '#eab308',
  archived: '#d1d5db',
};

const ROW_HEIGHT = 32;
const LABEL_WIDTH = 280;

type GroupBy = 'none' | 'status' | 'priority' | 'type';

function daysBetween(a: string, b: string): number {
  return (new Date(b).getTime() - new Date(a).getTime()) / 86400000;
}

export default function GanttChart({ items }: Props) {
  const [groupBy, setGroupBy] = useState<GroupBy>('status');
  const [hideMissing, setHideMissing] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const scrollRef = useRef<HTMLDivElement>(null);

  // Filter items that have at least a start date
  const datedItems = useMemo(() => {
    let filtered = items.filter((d) => d.created || d.updated);
    if (hideMissing) filtered = filtered.filter((d) => d.due);
    if (statusFilter !== 'all') filtered = filtered.filter((d) => d.status === statusFilter);
    return filtered;
  }, [items, hideMissing, statusFilter]);

  // Compute time range
  const range = useMemo(() => {
    const today = new Date().toISOString().slice(0, 10);
    let min = today;
    let max = today;
    for (const d of datedItems) {
      for (const dt of [d.created, d.due, d.updated]) {
        if (!dt) continue;
        if (dt < min) min = dt;
        if (dt > max) max = dt;
      }
    }
    // Pad by 30 days each side
    const minD = new Date(min);
    minD.setDate(minD.getDate() - 30);
    const maxD = new Date(max);
    maxD.setDate(maxD.getDate() + 30);
    const minStr = minD.toISOString().slice(0, 10);
    const maxStr = maxD.toISOString().slice(0, 10);
    return { min: minStr, max: maxStr, totalDays: Math.max(daysBetween(minStr, maxStr), 1) };
  }, [datedItems]);

  // Month markers
  const months = useMemo(() => {
    const markers: { label: string; pct: number }[] = [];
    const start = new Date(range.min);
    const end = new Date(range.max);
    const cursor = new Date(start.getFullYear(), start.getMonth() + 1, 1);
    while (cursor <= end) {
      const iso = cursor.toISOString().slice(0, 10);
      const pct = (daysBetween(range.min, iso) / range.totalDays) * 100;
      markers.push({
        label: cursor.toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
        pct,
      });
      cursor.setMonth(cursor.getMonth() + 1);
    }
    return markers;
  }, [range]);

  // Today position
  const todayPct = useMemo(() => {
    const today = new Date().toISOString().slice(0, 10);
    return (daysBetween(range.min, today) / range.totalDays) * 100;
  }, [range]);

  // Group items
  const grouped = useMemo(() => {
    if (groupBy === 'none') return [{ label: 'All Projects', items: datedItems }];

    const groups = new Map<string, GanttItem[]>();
    for (const item of datedItems) {
      const key = (item[groupBy] as string) ?? 'unset';
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(item);
    }

    const order: Record<string, string[]> = {
      status: ['active', 'planning', 'on-hold', 'completed', 'archived', 'unset'],
      priority: ['high', 'medium', 'low', 'unset'],
      type: ['execution', 'strategy', 'subtask', 'reference', 'meeting-note', 'unset'],
    };

    const sortOrder = order[groupBy] ?? [];
    return Array.from(groups.entries())
      .sort(([a], [b]) => {
        const ai = sortOrder.indexOf(a);
        const bi = sortOrder.indexOf(b);
        return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
      })
      .map(([label, groupItems]) => ({ label, items: groupItems }));
  }, [datedItems, groupBy]);

  // Compute bar for an item
  function getBar(item: GanttItem) {
    const start = item.created ?? item.updated ?? '';
    const end = item.due;
    const today = new Date().toISOString().slice(0, 10);

    const startPct = (daysBetween(range.min, start) / range.totalDays) * 100;
    const endPct = end
      ? (daysBetween(range.min, end) / range.totalDays) * 100
      : (daysBetween(range.min, today) / range.totalDays) * 100;

    return {
      left: Math.max(0, Math.min(100, startPct)),
      width: Math.max(0.5, Math.min(100, endPct) - Math.max(0, startPct)),
      openEnded: !end,
      isOverdue: !!end && end < today && item.status !== 'completed' && item.status !== 'archived',
    };
  }

  const totalRows = grouped.reduce((sum, g) => sum + g.items.length + 1, 0);

  return (
    <div>
      {/* Controls */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <label style={{ fontSize: '0.8125rem', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
          Group by:
          <select
            value={groupBy}
            onChange={(e) => setGroupBy(e.target.value as GroupBy)}
            style={{ border: '1px solid #e5e7eb', borderRadius: '0.25rem', padding: '0.25rem 0.5rem', fontSize: '0.8125rem' }}
          >
            <option value="status">Status</option>
            <option value="priority">Priority</option>
            <option value="type">Type</option>
            <option value="none">None</option>
          </select>
        </label>

        <label style={{ fontSize: '0.8125rem', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
          Status:
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{ border: '1px solid #e5e7eb', borderRadius: '0.25rem', padding: '0.25rem 0.5rem', fontSize: '0.8125rem' }}
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="planning">Planning</option>
            <option value="on-hold">On hold</option>
            <option value="completed">Completed</option>
          </select>
        </label>

        <label style={{ fontSize: '0.8125rem', display: 'flex', alignItems: 'center', gap: '0.375rem', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={hideMissing}
            onChange={(e) => setHideMissing(e.target.checked)}
          />
          Hide items without due dates
        </label>

        <span style={{ fontSize: '0.75rem', color: '#9ca3af' }}>
          {datedItems.length} items shown
        </span>
      </div>

      {/* Gantt container */}
      <div style={{ border: '1px solid #e5e7eb', borderRadius: '0.5rem', overflow: 'hidden' }}>
        {/* Month header */}
        <div style={{ display: 'flex', borderBottom: '1px solid #e5e7eb', backgroundColor: '#f9fafb' }}>
          <div style={{ width: LABEL_WIDTH, minWidth: LABEL_WIDTH, padding: '0.5rem', fontSize: '0.75rem', fontWeight: 600, color: '#6b7280' }}>
            Project
          </div>
          <div style={{ flex: 1, position: 'relative', height: '2rem' }}>
            {months.map((m) => (
              <div
                key={m.label}
                style={{
                  position: 'absolute',
                  left: `${m.pct}%`,
                  top: 0,
                  bottom: 0,
                  borderLeft: '1px solid #e5e7eb',
                  paddingLeft: '0.25rem',
                  fontSize: '0.625rem',
                  color: '#9ca3af',
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                {m.label}
              </div>
            ))}
          </div>
        </div>

        {/* Scrollable body */}
        <div ref={scrollRef} style={{ maxHeight: '70vh', overflowY: 'auto' }}>
          {grouped.map((group) => (
            <div key={group.label}>
              {/* Group header */}
              {groupBy !== 'none' && (
                <div style={{
                  display: 'flex',
                  backgroundColor: '#f9fafb',
                  borderBottom: '1px solid #e5e7eb',
                  borderTop: '1px solid #e5e7eb',
                }}>
                  <div style={{
                    width: LABEL_WIDTH,
                    minWidth: LABEL_WIDTH,
                    padding: '0.375rem 0.5rem',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    color: '#374151',
                    textTransform: 'capitalize',
                  }}>
                    {group.label} ({group.items.length})
                  </div>
                  <div style={{ flex: 1 }} />
                </div>
              )}

              {/* Rows */}
              {group.items.map((item) => {
                const bar = getBar(item);
                const color = bar.isOverdue ? '#ef4444' : (barColors[item.status ?? ''] ?? '#d1d5db');

                return (
                  <div
                    key={item.slug}
                    style={{
                      display: 'flex',
                      height: ROW_HEIGHT,
                      borderBottom: '1px solid #f3f4f6',
                      alignItems: 'center',
                    }}
                  >
                    {/* Label */}
                    <div style={{
                      width: LABEL_WIDTH,
                      minWidth: LABEL_WIDTH,
                      padding: '0 0.5rem',
                      fontSize: '0.75rem',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}>
                      <a
                        href={`/project/${item.slug}`}
                        style={{ color: '#1f2937', textDecoration: 'none' }}
                        onMouseOver={(e) => (e.currentTarget.style.textDecoration = 'underline')}
                        onMouseOut={(e) => (e.currentTarget.style.textDecoration = 'none')}
                      >
                        {item.title}
                      </a>
                    </div>

                    {/* Bar area */}
                    <div style={{ flex: 1, position: 'relative', height: '100%' }}>
                      {/* Month gridlines */}
                      {months.map((m) => (
                        <div
                          key={m.label}
                          style={{
                            position: 'absolute',
                            left: `${m.pct}%`,
                            top: 0,
                            bottom: 0,
                            width: '1px',
                            backgroundColor: '#f3f4f6',
                          }}
                        />
                      ))}

                      {/* Today line */}
                      <div style={{
                        position: 'absolute',
                        left: `${todayPct}%`,
                        top: 0,
                        bottom: 0,
                        width: '2px',
                        backgroundColor: '#ef4444',
                        opacity: 0.25,
                        zIndex: 1,
                      }} />

                      {/* Bar */}
                      <div
                        title={`${item.created ?? '?'} → ${item.due ?? 'ongoing'}${bar.isOverdue ? ' (OVERDUE)' : ''}`}
                        style={{
                          position: 'absolute',
                          left: `${bar.left}%`,
                          width: `${bar.width}%`,
                          top: '8px',
                          height: '16px',
                          backgroundColor: color,
                          borderRadius: bar.openEnded ? '3px 0 0 3px' : '3px',
                          opacity: 0.85,
                          borderRight: bar.openEnded ? '2px dashed rgba(0,0,0,0.25)' : 'none',
                          zIndex: 2,
                          cursor: 'pointer',
                        }}
                        onClick={() => window.location.href = `/project/${item.slug}`}
                      />
                    </div>
                  </div>
                );
              })}

              {group.items.length === 0 && (
                <div style={{ padding: '1rem', fontSize: '0.75rem', color: '#9ca3af', textAlign: 'center' }}>
                  No items in this group.
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', gap: '1rem', marginTop: '0.75rem', fontSize: '0.6875rem', color: '#6b7280', flexWrap: 'wrap' }}>
        {Object.entries(barColors).map(([label, color]) => (
          <span key={label} style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            <span style={{ width: '12px', height: '8px', backgroundColor: color, borderRadius: '2px', display: 'inline-block' }} />
            {label}
          </span>
        ))}
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <span style={{ width: '12px', height: '8px', backgroundColor: '#ef4444', borderRadius: '2px', display: 'inline-block' }} />
          overdue
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <span style={{ width: '2px', height: '12px', backgroundColor: '#ef4444', opacity: 0.4, display: 'inline-block' }} />
          today
        </span>
      </div>
    </div>
  );
}