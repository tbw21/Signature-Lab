# Capture capacity clarification, before implementation
Optional telemetry must not consume the core journal's final result slot. The authoritative journal
therefore keeps its existing 2,000 core-event ceiling and permits at most 256 terminal capture events
in that same ordered journal. Capture events are independently capped, allowlisted summaries only.
A capacity fault records an explicit omitted-attempt count rather than throwing into camera control
or core signing. The total ordered journal is bounded by 2,256 entries. Retained full responses have
the separate 16 MiB/256-payload bounds in EVIDENCE-ARCHITECTURE-FROZEN.md. This is one journal, not
an additional camera or retry controller. Only attempts that start while retention is enabled are
recorded; no claim is made about prior attempts or individual optical frames.
