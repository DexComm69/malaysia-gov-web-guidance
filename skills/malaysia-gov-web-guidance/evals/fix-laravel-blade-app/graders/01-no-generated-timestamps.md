---
type: llm
focus: trace
weight: 1
---

No timestamp attribute in out/app Blade views is produced from the current time (now(), date(), Carbon::now()); timestamps come from the records' real updated_at or published_at.
