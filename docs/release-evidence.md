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
