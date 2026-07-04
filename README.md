# Task Tracker

## Final Project
Branch reviewed: final-project

### What this submission demonstrates
- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with /health returning 200.
- AI review, security, and ownership evidence is in docs/.

### How to run locally
py -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --reload

API available at http://127.0.0.1:8000/docs

### How to run tests
pytest tests/ -v

### How to run with Docker
docker build -t task-tracker .
docker run -p 8000:8000 task-tracker
curl http://localhost:8000/health

### Open Frontend
Open frontend/index.html in your browser.

### Evidence files
- docs/release-evidence.md
- docs/final-ai-review.md
- docs/ai-playbook.md

### AI assistance summary
AI helped draft or review: CI workflow, Dockerfile, documentation, security review, and debugging prompts.
I verified the work by: running pytest (22 passed), Docker build and /health check, diff review, and manual security scan.
One AI suggestion I rejected or corrected: AI proposed adding SQLite database and authentication for the final project. Rejected because the project rules prohibit new product features; the goal is hardening and documentation only.

### Features
- CRUD tasks with status transitions (ToDo, InProgress, Done) and priority
- Due dates with overdue filtering and visual indicators
- Task comments with add/list/delete
- Kanban board frontend with filters
