# Task Tracker

## Setup
py -m venv venv
.\venv\Scripts\Activate
pip install fastapi uvicorn pytest httpx

## Run Backend
uvicorn app.main:app --reload
API available at http://127.0.0.1:8000/docs

## Open Frontend
Open frontend/index.html in your browser.

## Run Tests
pytest tests/ -v

## Features
- CRUD tasks with status transitions and priority
- Due dates with overdue filtering and visual indicators
- Task comments with add/list/delete
- Kanban board frontend
