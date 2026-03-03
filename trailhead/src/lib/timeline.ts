/**
 * Timeline utilities for computing visual bar positions.
 *
 * Each project gets a horizontal bar from start→due within a global date range.
 */

export interface TimelineRange {
  /** Earliest date across all docs (ISO string) */
  min: string;
  /** Latest date across all docs (ISO string) */
  max: string;
  /** Total days spanned */
  totalDays: number;
}

export interface TimelineBar {
  /** Start position as 0-100 percentage */
  startPct: number;
  /** Width as 0-100 percentage */
  widthPct: number;
  /** Whether the end is open (no due date) */
  openEnded: boolean;
  /** Start date used */
  startDate: string | null;
  /** End date used */
  endDate: string | null;
}

interface DateFields {
  created: string | null;
  due: string | null;
  updated: string | null;
}

/**
 * Compute the global date range from all docs.
 * Uses created/due/updated to find the full span, then adds padding.
 */
export function computeRange(docs: DateFields[]): TimelineRange {
  const today = new Date().toISOString().slice(0, 10);
  let min = today;
  let max = today;

  for (const doc of docs) {
    for (const d of [doc.created, doc.due, doc.updated]) {
      if (!d) continue;
      if (d < min) min = d;
      if (d > max) max = d;
    }
  }

  // Add 30 days padding on each end
  const minDate = new Date(min);
  minDate.setDate(minDate.getDate() - 30);
  min = minDate.toISOString().slice(0, 10);

  const maxDate = new Date(max);
  maxDate.setDate(maxDate.getDate() + 30);
  max = maxDate.toISOString().slice(0, 10);

  const totalDays = daysBetween(min, max);

  return { min, max, totalDays: Math.max(totalDays, 1) };
}

/**
 * Compute the bar position for a single doc within the global range.
 */
export function computeBar(
  doc: DateFields,
  range: TimelineRange
): TimelineBar | null {
  const start = doc.created ?? doc.updated;
  if (!start) return null;

  const end = doc.due;
  const today = new Date().toISOString().slice(0, 10);

  const startPct = (daysBetween(range.min, start) / range.totalDays) * 100;

  let endPct: number;
  let openEnded = false;

  if (end) {
    endPct = (daysBetween(range.min, end) / range.totalDays) * 100;
  } else {
    // No due date: extend bar to today
    endPct = (daysBetween(range.min, today) / range.totalDays) * 100;
    openEnded = true;
  }

  // Clamp to 0-100
  const clampedStart = Math.max(0, Math.min(100, startPct));
  const clampedEnd = Math.max(0, Math.min(100, endPct));
  const widthPct = Math.max(1, clampedEnd - clampedStart);

  return {
    startPct: clampedStart,
    widthPct,
    openEnded,
    startDate: start,
    endDate: end,
  };
}

/**
 * Generate month labels for the timeline header.
 */
export function computeMonthMarkers(range: TimelineRange): { label: string; pct: number }[] {
  const markers: { label: string; pct: number }[] = [];
  const start = new Date(range.min);
  const end = new Date(range.max);

  // Start from the first of the month after range start
  const cursor = new Date(start.getFullYear(), start.getMonth() + 1, 1);

  while (cursor <= end) {
    const iso = cursor.toISOString().slice(0, 10);
    const pct = (daysBetween(range.min, iso) / range.totalDays) * 100;
    const label = cursor.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
    markers.push({ label, pct });
    cursor.setMonth(cursor.getMonth() + 1);
  }

  return markers;
}

function daysBetween(a: string, b: string): number {
  const msPerDay = 86400000;
  return (new Date(b).getTime() - new Date(a).getTime()) / msPerDay;
}