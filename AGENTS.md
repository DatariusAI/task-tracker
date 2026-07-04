# AGENTS.md - Task Tracker AI Governance

## Project Stack
- Backend: Python 3.12+ with FastAPI and Pydantic
- Frontend: Vanilla HTML/CSS/JavaScript (single file, no build step)
- Storage: In-memory Python dictionaries (no database)
- Tests: pytest with FastAPI TestClient
- CI: GitHub Actions
- Container: Docker with non-root user

## Run Commands
- Install: pip install -r requirements.txt
- Start API: uvicorn app.main:app --reload
- Run tests: pytest tests/ -v
- Docker build: docker build -t task-tracker .
- Docker run: docker run -p 8000:8000 task-tracker

## Project Rules
- No authentication, no database, no multi-tenancy
- No real-time sync, no mobile, no notifications
- Status transitions: ToDo -> InProgress -> Done, Done -> InProgress
- All task validation handled by Pydantic models
- CORS allows all origins (development only)

## Docs-First / Read-First Guardrails
- Before modifying app/ or frontend/, read the existing code and tests first
- Before adding a dependency, check if the existing stack already solves the problem
- Before accepting AI-generated code, run pytest and verify /health endpoint

## AI Usage Rules
- Never paste .env files, API keys, or credentials into AI tools
- Always review AI-generated diffs line by line before committing
- If AI suggests adding auth, database, or production features, reject and re-scope
- Record AI contributions in docs/ for transparency
- If you cannot explain a line of code, do not commit it

## Unexpected Changes Rule
- Changes to app/ or frontend/ require an explanation in docs/final-ai-review.md
- No new product features in the final project
- Only bug fixes, security fixes, or documentation-supported corrections allowed
