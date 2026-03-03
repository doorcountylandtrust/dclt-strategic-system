import { useState, useMemo } from 'react';
import { computeRange, computeBar, computeMonthMarkers } from '../lib/timeline';

interface DocSummary {
  slug: string;
  title: string;
  status: string | null;
  priority: string | null;
  type: string | null;
  owner: string | null;
  created: string | null;
  due: string | null;
  updated: string | null;
  hasFrontmatter: boolean;
  childCount: number;
}

interface Props {
  docs: DocSummary[];
}

const STATUS_OPTIONS = ['all', 'active', 'planning', 'on-hold', 'completed', 'archived'] as const;
const PRIORITY_OPTIONS = ['all', 'high', 'medium', 'low', 'unset'] as const;
const TYPE_OPTIONS = ['all', 'strategy', 'execution', 'reference', 'meeting-note', 'subtask'] as const;

const statusColors: Record<string, string> = {
  active: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  'on-hold': 'bg-gray-100 text-gray-700',
  planning: 'bg-yellow-100 text-yellow-800',
  archived: 'bg-gray-100 text-gray-500',
};

const priorityColors: Record<string, string> = {
  high: 'bg-red-100 text-red-800',
  medium: 'bg-yellow-100 text-yellow-800',
  low: 'bg-gray-100 text-gray-600',
};

const barColors: Record<string, string> = {
  active: '#3b82f6',
  completed: '#22c55e',
  'on-hold': '#9ca3af',
  planning: '#eab308',
  archived: '#d1d5db',
};

export default function FilterableProjectList({ docs }: Props) {
  const [status, setStatus] = useState<string>('all');
  const [priority, setPriority] = useState<string>('all');
  const [type, setType] = useState<string>('all');
  const [search, setSearch] = useState('');

  const filtered = useMemo(() => {
    return docs.filter((d) => {
      if (status !== 'all' && d.status !== status) return false;
      if (priority === 'unset' && d.priority !== null) return false;
      if (priority !== 'all' && priority !== 'unset' && d.priority !== priority) return false;
      if (type !== 'all' && d.type !== type) return false;
      if (search && !d.title.toLowerCase().includes(search.toLowerCase())) return false;
      return true;
    });
  }, [docs, status, priority, type, search]);

  const timelineRange = useMemo(() => computeRange(filtered), [filtered]);
  const monthMarkers = useMemo(() => computeMonthMarkers(timelineRange), [timelineRange]);
  const todayPct = useMemo(() => {
    const today = new Date().toISOString().slice(0, 10);
    const days = (new Date(today).getTime() - new Date(timelineRange.min).getTime()) / 86400000;
    return (days / timelineRange.totalDays) * 100;
  }, [timelineRange]);

  const selectStyle = "border rounded px-2 py-1.5 text-sm bg-white";

  return (
    <div>
      {/* Filter bar */}
      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap', marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search titles..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border rounded px-2 py-1.5 text-sm"
          style={{ width: '200px' }}
        />

        <select value={status} onChange={(e) => setStatus(e.target.value)} className={selectStyle}>
          {STATUS_OPTIONS.map((s) => (
            <option key={s} value={s}>{s === 'all' ? 'All statuses' : s}</option>
          ))}
        </select>

        <select value={priority} onChange={(e) => setPriority(e.target.value)} className={selectStyle}>
          {PRIORITY_OPTIONS.map((p) => (
            <option key={p} value={p}>{p === 'all' ? 'All priorities' : p === 'unset' ? 'No priority' : p}</option>
          ))}
        </select>

        <select value={type} onChange={(e) => setType(e.target.value)} className={selectStyle}>
          {TYPE_OPTIONS.map((t) => (
            <option key={t} value={t}>{t === 'all' ? 'All types' : t}</option>
          ))}
        </select>

        <span className="text-sm text-gray-500">
          {filtered.length} of {docs.length}
        </span>

        {(status !== 'all' || priority !== 'all' || type !== 'all' || search) && (
          <button
            onClick={() => { setStatus('all'); setPriority('all'); setType('all'); setSearch(''); }}
            className="text-sm text-blue-600 hover:underline"
          >
            Clear filters
          </button>
        )}
      </div>

      {/* Results table */}
      <table style={{ width: '100%', fontSize: '0.875rem', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #e5e7eb', textAlign: 'left' }}>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Title</th>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Status</th>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Priority</th>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Type</th>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Owner</th>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Due</th>
            <th style={{ padding: '0.5rem 1rem 0.5rem 0' }}>Updated</th>
            <th style={{ padding: '0.5rem 0', minWidth: '250px' }}>
              <div style={{ position: 'relative', height: '1.25rem', fontSize: '0.625rem', color: '#9ca3af' }}>
                {monthMarkers.map((m) => (
                  <span key={m.label} style={{ position: 'absolute', left: `${m.pct}%`, transform: 'translateX(-50%)' }}>
                    {m.label}
                  </span>
                ))}
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((doc) => {
            const today = new Date().toISOString().slice(0, 10);
            const isOverdue = doc.due && doc.due < today && doc.status !== 'completed' && doc.status !== 'archived';

            return (
              <tr key={doc.slug} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  <a href={`/project/${doc.slug}`} style={{ color: '#2563eb', textDecoration: 'none' }}
                     onMouseOver={(e) => (e.currentTarget.style.textDecoration = 'underline')}
                     onMouseOut={(e) => (e.currentTarget.style.textDecoration = 'none')}>
                    {doc.title}
                  </a>
                  {doc.childCount > 0 && (
                    <span style={{ color: '#9ca3af', fontSize: '0.75rem', marginLeft: '0.5rem' }}>
                      ({doc.childCount} items)
                    </span>
                  )}
                </td>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  {doc.status ? (
                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${statusColors[doc.status] ?? ''}`}>
                      {doc.status}
                    </span>
                  ) : <span style={{ color: '#d1d5db' }}>—</span>}
                </td>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  {doc.priority ? (
                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${priorityColors[doc.priority] ?? ''}`}>
                      {doc.priority}
                    </span>
                  ) : <span style={{ color: '#d1d5db' }}>—</span>}
                </td>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  {doc.type ?? <span style={{ color: '#d1d5db' }}>—</span>}
                </td>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  {doc.owner ?? <span style={{ color: '#d1d5db' }}>—</span>}
                </td>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  <span style={isOverdue ? { color: '#dc2626', fontWeight: 500 } : {}}>
                    {doc.due ?? <span style={{ color: '#d1d5db' }}>—</span>}
                  </span>
                </td>
                <td style={{ padding: '0.5rem 1rem 0.5rem 0' }}>
                  {doc.updated ?? <span style={{ color: '#d1d5db' }}>—</span>}
                </td>
                <td style={{ padding: '0.5rem 0' }}>
                  {(() => {
                    const bar = computeBar(doc, timelineRange);
                    if (!bar) return <span style={{ color: '#d1d5db', fontSize: '0.75rem' }}>no dates</span>;
                    const color = barColors[doc.status ?? ''] ?? '#d1d5db';
                    const isOverdue = doc.due && doc.due < new Date().toISOString().slice(0, 10) && doc.status !== 'completed' && doc.status !== 'archived';
                    return (
                      <div style={{ position: 'relative', height: '1.25rem', width: '100%' }}>
                        {/* Today marker */}
                        <div style={{
                          position: 'absolute',
                          left: `${todayPct}%`,
                          top: 0,
                          bottom: 0,
                          width: '1px',
                          backgroundColor: '#ef4444',
                          opacity: 0.3,
                        }} />
                        {/* Bar */}
                        <div
                          title={`${bar.startDate ?? '?'} → ${bar.endDate ?? 'ongoing'}`}
                          style={{
                            position: 'absolute',
                            left: `${bar.startPct}%`,
                            width: `${bar.widthPct}%`,
                            top: '3px',
                            height: '14px',
                            backgroundColor: isOverdue ? '#ef4444' : color,
                            borderRadius: bar.openEnded ? '3px 0 0 3px' : '3px',
                            opacity: 0.85,
                            borderRight: bar.openEnded ? '2px dashed rgba(0,0,0,0.2)' : 'none',
                          }}
                        />
                      </div>
                    );
                  })()}
                </td>
              </tr>
            );
          })}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={8} style={{ padding: '2rem', textAlign: 'center', color: '#9ca3af' }}>
                No files match these filters.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}