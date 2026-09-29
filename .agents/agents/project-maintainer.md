---
name: Project Maintainer
description: Rules for maintaining the Personal Finance Advisor Bot
---

# Project Maintainer Rules

- **Understand Architecture:** Before editing, review `docs/architecture.md` and the `app/services` structure.
- **Preserve Conventions:** Use Flask application factory, Blueprints, and deterministic Python math for finance calculations.
- **Testing:** Always run tests using `pytest tests/` after making changes.
- **Git Hygiene:** Check `git diff` before committing. Use meaningful semantic commit messages (e.g. `feat:`, `fix:`, `chore:`).
- **Secrets:** NEVER commit secrets, API keys, or `.env` files.
- **Documentation:** Keep `README.md` and `docs/` updated if features or behavior change.
