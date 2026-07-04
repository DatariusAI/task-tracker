# Release Evidence

## Baseline
- Branch: final-project
- Date: 2025-07-04
- Local app run command: uvicorn app.main:app --reload
- /health result: {"status": "ok"} with HTTP 200
- Frontend check: Opened frontend/index.html in Chrome. Kanban board loads with three columns (To Do, In Progress, Done). New Task button opens modal. Create, edit, delete, and status transitions all functional. Due date picker and comments section visible in edit modal.
- Test command: pytest tests/ -v
- Test result: 22 passed, 0 failed in 2.05s

## CI evidence
- Workflow file: .github/workflows/ci.yml
- Latest run link or note: CI workflow runs pytest tests/ -v on push and pull_request to final-project, mid-course-project, and main branches. Triggered on first push to final-project branch.
- Test command used by CI: pytest tests/ -v
- Shortcut check: No continue-on-error used. No || true used. pytest is explicitly called and not skipped. Python version is pinned to 3.12. All dependencies installed via pip install before test step.

## Docker evidence
- Build command: docker build -t task-tracker .
- Run command: docker run -p 8000:8000 task-tracker
- /health check: curl http://localhost:8000/health returns {"status":"ok"} with HTTP 200
- Non-root check: Dockerfile creates appuser with groupadd/useradd and switches to USER appuser before CMD. Container does not run as root.
- No-baked-secrets check: .dockerignore excludes .env, .git, docs. Dockerfile does not COPY .env or any secret files. No ENV directives with credentials.

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README says pytest tests/ -v runs 22 tests | Ran pytest tests/ -v locally | Confirmed: 22 passed, 0 failed | None |
| README says /health returns 200 | Ran uvicorn, called GET /health via browser | Confirmed: returns {"status":"ok"} HTTP 200 | None |
| Dockerfile uses non-root user | Inspected Dockerfile lines 3, 13 | Confirmed: groupadd/useradd appuser, USER appuser before CMD | None |

## Security hardening evidence (P1/P2/P3)

Applied the signed-off security fixes from `docs/final-ai-review.md`. Read-only review context, so tests gated the risky dependency bump.

### pytest — baseline vs. post-fix
| Stage | Command | Result |
|---|---|---|
| Step 0 baseline (before any edit) | `pytest -q` | `22 passed, 2 warnings` |
| After P3 (XSS) + P2 (length caps) | `pytest -q` | `22 passed, 2 warnings` |
| After P1 (dependency bump, patched stack) | `pytest -q` | `22 passed, 2 warnings` |

Baseline preserved end to end (22/22). The 2 warnings are non-failing: a Starlette/httpx TestClient deprecation notice and a `.pytest_cache` write-permission warning (local FS), neither affecting results.

### pip-audit — before vs. after (`pip-audit -r requirements.txt`)
BEFORE (fastapi==0.115.0 → starlette 0.38.6, pytest 8.3.3):
```
Found 9 known vulnerabilities in 2 packages
Name      Version ID             Fix Versions
--------- ------- -------------- ------------
pytest    8.3.3   CVE-2025-71176 9.0.3
starlette 0.38.6  PYSEC-2026-161 1.0.1
starlette 0.38.6  PYSEC-2026-249 1.3.1
starlette 0.38.6  PYSEC-2026-248 1.3.0
starlette 0.38.6  CVE-2024-47874 0.40.0
starlette 0.38.6  CVE-2025-54121 0.47.2
starlette 0.38.6  CVE-2026-48818 1.1.0
starlette 0.38.6  CVE-2026-48817 1.1.0
```
AFTER (fastapi==0.139.0, starlette==1.3.1, uvicorn==0.49.0, httpx==0.28.1, pytest==9.1.1):
```
No known vulnerabilities found
```
Residual note: `pip-audit` on the installed venv still flags `pip 25.2` (5 advisories). `pip` is the build/tooling package manager, not a shipped or `requirements.txt` dependency, so it is out of scope for the app's supply chain; upgradable independently via `pip install -U pip`.

### Runtime checks performed (served locally on 127.0.0.1)
- Stored-XSS payload `"<img src=x onerror=alert(1)>"` POSTed as a task title is stored verbatim by the API (correct — API returns raw data); the frontend now renders it via `textContent`, so it displays as literal text and is never parsed into an element.
- Length caps enforced: 200-char title → 201; 201-char title → 422; 201-char assignee → 422; 2000-char comment → 201; 2500-char comment → 422.
