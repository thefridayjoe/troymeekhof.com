# troymeekhof.com — rules for every session (read before touching anything)

Troy's standing requirement: **every change keeps all existing progress and content. Watertight.**

## The one rule
The files in this repo, on `main`, ARE the website and the only source of truth. Nothing regenerates them.
**Never rebuild, retype, or restore a page from an old copy, a Project doc, memory, or a past build.**
Always start from the current file here and make the smallest possible edit.

## How to change the site
1. `git pull` so you have the latest `main`.
2. Edit surgically: `python3 _src/site.py replace <file> "<exact old text>" "<new text>"` (fails unless the old text appears exactly once), or a minimal hand edit.
3. `git diff` and confirm that only the lines you meant to change moved.
4. `python3 _src/site.py check`, then commit **only** the files you changed (`git add <paths>`, never `git add -A`).
5. `python3 _src/site.py guard` must pass before you push. It blocks deleted pages, files put back to an older version, files edited from a stale copy, and pages losing more than 20% of their text.
6. Push. GitHub Actions re-runs both checks. If they fail, the change is **not published**.
7. Add one line to `_src/CHANGELOG.md` (date, what, why, in Troy's words when possible) in the same commit.

## When Troy explicitly asks to remove or roll back something
Put the matching token in the commit message: `[allow-delete]`, `[allow-shrink]` (for example, retiring a page to a redirect stub), or `[allow-revert]`. Never use a token for anything Troy didn't ask for.

## Other rules
- A retired page becomes a redirect stub (noindex, canonical plus meta refresh to its new home). It never becomes a 404.
- Don't touch `assets/img/truck/delivery-day-16x9-1000.webp` (the live version is intentional).
- Facts about Troy come from the live pages and `llms.txt`. Don't invent numbers, clients, or quotes.
- Files and folders starting with `_` or `.`, plus `CLAUDE.md`, are not published (see `_src/site.py stage`).
- More detail: `_src/README.md`.
