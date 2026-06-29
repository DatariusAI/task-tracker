# Task Tracker

## Setup
`ash
py -m venv venv
.\venv\Scripts\Activate
pip install fastapi uvicorn pytest httpx
`

## Run Backend
`ash
uvicorn app.main:app --reload
`
API available at http://127.0.0.1:8000/docs

## Open Frontend
Open rontend/index.html in your browser.

## Run Tests
`ash
pytest tests/ -v
`

## Features
- CRUD tasks with status transitions and priority
- Due dates with overdue filtering and visual indicators
- Task comments with add/list/delete
- Kanban board frontend
