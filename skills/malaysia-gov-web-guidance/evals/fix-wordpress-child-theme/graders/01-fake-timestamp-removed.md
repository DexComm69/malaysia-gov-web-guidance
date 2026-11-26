---
type: llm
focus: trace
weight: 1
---

The corrected theme no longer sets any timestamp from the current time (no date('Y-m-d H:i:s'), current_time() or similar used as a timestamp value); timestamps come from real WordPress dates such as the page's modified date or the newest post.
