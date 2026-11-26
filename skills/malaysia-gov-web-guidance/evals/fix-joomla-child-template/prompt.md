---
tags: [splask, joomla, stress-test-round-6]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our district council's Joomla site failed SPLaSK. Read README.txt and config.txt first. Fix our child template (template/cassiopeia_mdcj, including its overrides) so the site passes. We can't change Joomla core, Cassiopeia or the extensions, but tell us anything we have to change in the Joomla administrator. Check all the pages, not just the home page. Put the corrected template in out/template/cassiopeia_mdcj/, the five pages as the server would send them after your changes in out/rendered/ (same file names), and your notes in out/NOTES.md. Don't invent URLs or dates; use a TODO where a real value is needed. Don't ask me questions; list assumptions at the top of NOTES.md.

Input files: README.txt, config.txt, template/, rendered/
