```dataview

table title as "Project", status as "Status", priority as "Priority", start_date as "Start", end_date as "End", notes as "Notes"

from "data/dclt/02_EXECUTION/10_Projects"

where !isnull(title)

sort priority asc