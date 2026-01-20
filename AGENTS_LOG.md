# Agents Log

## Intervention History

### Housekeeping Report
**Date:** 2026-01-20
**AI Assistant:** Antigravity
**Summary:** Executed housekeeping protocol for Iterated Prisoners Dilemma project.
- **Dependency Network:** Updated with full project structure from environment.py → agents.py → engine → api → frontend
- **Tests:** 20 tests passed (10 in test_agents.py, 10 in test_environment.py) in 0.04s
- **Data Logging:** Verified 2 sessions saved to data/sessions/ with correct JSON format
- **Browser Integration:** Verified full game playthrough with TitForTat agent

---

### Project Creation: Iterated Prisoners Dilemma
**Date:** 2026-01-20
**AI Assistant:** Antigravity
**Summary:** Created complete iterated prisoners dilemma simulation from scratch.
- **Backend:** Python/FastAPI with environment (payoff matrix), agents (TitForTat, AlwaysCooperate, AlwaysDefect, Random), engine (config, state, model), API (routes, session)
- **Frontend:** React/TypeScript with premium dark theme UI
- **Data Logging:** Auto-save session data to JSON on game completion
- **Tests:** 20 unit tests for environment and agent behavior
- **Files Created:** 15+ files across backend/, frontend/, tests/

---

### Bug Fix: Advanced Analysis (Shape Mismatch)
**Date:** 2024-05-22
**Summary:** Fixed RuntimeError in `advanced_experiment_interface.ipynb`.
- **Issue:** `compute_policy_metrics` in `src/analysis.py` passed 1D inputs `(100, 1)` to agents expecting 2D inputs `(100, 2)`.
- **Fix:** Created `src/advanced_analysis.py` with `compute_advanced_policy_metrics`.
- **Details:** The new function constructs inputs as `[p, t]` with `t` fixed at 0 (default).
- **Files Modified:** `src/advanced_simulation.py` updated to use the new analysis function.

### Bug Fix: Notebook NameError
**Date:** 2024-05-22
**Summary:** Fixed NameError in `advanced_experiment_interface.ipynb`.
- **Issue:** The variable `ep_id` was used in a print statement but was undefined in the new JSON saving block.
- **Fix:** Removed the erroneous print statement and cleanup old comments. Validated that the correct logging uses `current_step_info['episode_count']`.
