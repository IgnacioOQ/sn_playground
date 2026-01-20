# Housekeeping Protocol

1. Read the AGENTS.md file.
2. Look at the dependency network of the project, namely which script refers to which one.
3. Proceed doing different sanity checks and unit tests from root scripts to leaves.
4. Compile all errors and tests results into a report. And print that report in the Latest Report subsection below, overwriting previous reports.
5. Add that report to the AGENTS_LOG.md.

# Current Project Housekeeping

## Dependency Network

**Iterated Prisoners Dilemma Project:**

```
backend/environment.py (root - no dependencies)
    ↓
backend/agents.py (depends on environment.py)
    ↓
backend/engine/config.py (root - Pydantic models)
backend/engine/state.py (root - Pydantic models)
    ↓
backend/logging.py (depends on state.py)
    ↓
backend/engine/model.py (depends on agents, environment, config, state, logging)
    ↓
backend/api/session.py (depends on engine/model.py)
    ↓
backend/api/routes.py (depends on engine/*, api/session.py)
    ↓
backend/api/main.py (depends on routes.py)
    ↓
frontend/src/*.tsx (depends on backend API on port 8000)
```

**Test files:**
- `tests/test_environment.py` → tests `backend/environment.py`
- `tests/test_agents.py` → tests `backend/agents.py`

## Latest Report

**Execution Date:** 2026-01-20

**Test Results:**
1. `tests/test_agents.py`: **10 tests PASSED**
   - TitForTatAgent: 6 tests (first move, mirrors cooperation/defection, forgives, sequence, reset)
   - AlwaysCooperateAgent: 1 test
   - AlwaysDefectAgent: 1 test
   - RandomAgent: 2 tests
2. `tests/test_environment.py`: **10 tests PASSED**
   - PayoffMatrix: 3 tests (default values, constraints)
   - PrisonersDilemmaEnvironment: 5 tests (all payoff combinations)
   - Action enum: 2 tests

**Total: 20 tests passed in 0.04s**

**Data Logging Verification:**
- Played 2 complete games via browser
- Session data correctly saved to `data/sessions/`
- JSON format verified with step, human_action, agent_action, outcomes, next_step, done

**Summary:**
All unit tests passed. Frontend-backend integration verified via browser playthrough. Session data logging confirmed working. Project is stable and fully functional.

