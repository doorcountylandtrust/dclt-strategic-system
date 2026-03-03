#!/bin/bash
# scaffold-trailhead.sh
# Creates the Trailhead project skeleton alongside your docs/ directory.
# Run from: dclt-strategic-system-v2/
# Usage: bash scaffold-trailhead.sh

set -e

PROJECT="trailhead"

if [ -d "$PROJECT" ]; then
  echo "⚠️  Directory '$PROJECT' already exists. Aborting to avoid overwriting."
  exit 1
fi

echo "🌲 Scaffolding Trailhead..."

# Root config files (empty placeholders)
mkdir -p "$PROJECT"
touch "$PROJECT/astro.config.mjs"
touch "$PROJECT/package.json"
touch "$PROJECT/tsconfig.json"
touch "$PROJECT/tailwind.config.mjs"

# src/
mkdir -p "$PROJECT/src"
touch "$PROJECT/src/config.ts"

# src/lib/
mkdir -p "$PROJECT/src/lib"
touch "$PROJECT/src/lib/frontmatter.ts"
touch "$PROJECT/src/lib/hierarchy.ts"
touch "$PROJECT/src/lib/timeline.ts"
touch "$PROJECT/src/lib/report.ts"
touch "$PROJECT/src/lib/health.ts"

# src/pages/
mkdir -p "$PROJECT/src/pages/project"
touch "$PROJECT/src/pages/index.astro"
touch "$PROJECT/src/pages/gantt.astro"
touch "$PROJECT/src/pages/report.astro"
touch "$PROJECT/src/pages/project/[...slug].astro"

# src/components/
mkdir -p "$PROJECT/src/components"
touch "$PROJECT/src/components/ProjectList.tsx"
touch "$PROJECT/src/components/ProjectTree.tsx"
touch "$PROJECT/src/components/TimelineBar.astro"
touch "$PROJECT/src/components/StatsBar.astro"
touch "$PROJECT/src/components/StatusBadge.astro"
touch "$PROJECT/src/components/FilterBar.tsx"
touch "$PROJECT/src/components/GanttChart.tsx"

# src/layouts/
mkdir -p "$PROJECT/src/layouts"
touch "$PROJECT/src/layouts/Base.astro"

# src/styles/
mkdir -p "$PROJECT/src/styles"
touch "$PROJECT/src/styles/global.css"

# public/
mkdir -p "$PROJECT/public"
touch "$PROJECT/public/favicon.svg"

echo ""
echo "✅ Trailhead scaffolded. Structure:"
echo ""
find "$PROJECT" -type f | sort | sed 's/^/  /'
echo ""
echo "Next step: we'll fill in package.json and astro.config.mjs first."