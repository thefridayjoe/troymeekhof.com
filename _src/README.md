# How this repo works

- **The repo is the website.** Every public file (everything not starting with `_` or `.`, plus everything except `CLAUDE.md`) is served at troymeekhof.com by GitHub Pages.
- **There is no generator.** The original `build.py` and its Markdown are archived in the claude.ai Project (`site-source/`) for reference only. They are incomplete (no article Markdown, photos, or fonts) and must never be used to regenerate pages.
- **`_src/site.py`** is the safety tool (standard library only):
  - `check`: broken internal links, invalid JSON-LD, sitemap pointing at missing or noindex pages, llms.txt and RSS pointing at missing pages, banned phrases.
  - `guard`: compares a push against the previous live commit and fails on a deleted public file, a file restored to an older version (exact match), a file edited from a stale copy (closer to an older version than to the live one), or a page losing more than 20% of its main text. Override tokens in the commit message: `[allow-delete]`, `[allow-revert]`, `[allow-shrink]`.
  - `replace FILE OLD NEW`: exact single-match edit with a diff and before/after sha256.
  - `stage DIR`: copies exactly what gets published.
- **`.github/workflows/site.yml`** runs `check` and `guard` on every push to `main`. When deploy-through-Actions is on (below), a failing push never goes live.

## One-time setup (turns the guard into a hard gate)
1. Repo **Settings → Secrets and variables → Actions → Variables → New repository variable**: `DEPLOY_WITH_ACTIONS` = `true`.
2. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**. The custom domain troymeekhof.com and HTTPS stay as they are.
3. **Actions tab → Guard and deploy → Run workflow.** Confirm both jobs go green and the site still loads.

Until step 2 is done, the guard still runs and emails a failure, but Pages publishes straight from the branch.

## Undo
Every version of every file is in git history. To undo a bad change, `git revert <commit>` with `[allow-revert]` in the message. Never hand-rebuild.
