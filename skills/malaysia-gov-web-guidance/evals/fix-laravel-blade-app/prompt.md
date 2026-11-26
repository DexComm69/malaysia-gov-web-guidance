---
tags: [splask, laravel, blade, stress-test-round-7]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our district council's Laravel site failed SPLaSK. Read README.txt and db.txt first. Fix the Laravel app (views, components, controllers, and a migration or seeder if the database needs a change) so the site passes. Check all the pages, not just the home page. Put the corrected app in out/app/, the five pages as the server would send them after your changes in out/rendered/ (same file names, using the real dates and times from db.txt), and your notes in English in out/NOTES.md. Don't invent URLs or dates; use a TODO where a real value is needed. Don't ask me questions; list assumptions at the top of NOTES.md.

Input files: README.txt, db.txt, app/, rendered/
