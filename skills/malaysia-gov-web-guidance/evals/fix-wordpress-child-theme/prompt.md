---
tags: [splask, wordpress, stress-test-round-5]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our district council's WordPress site failed SPLaSK. Read README.txt first. Fix our child theme (theme/) so the site passes. We can't change the parent theme or the plugins, but tell us anything we have to do in WP admin. Check all the pages, not just the home page. Put the corrected theme in out/theme/, the five pages as the server would send them after your changes in out/rendered/ (same file names), and your notes in out/NOTES.md. Don't invent URLs or dates; use a TODO where a real value is needed. Don't ask me questions; list assumptions at the top of NOTES.md.

Input files: README.txt, theme/, rendered/
