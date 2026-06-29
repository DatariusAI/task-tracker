# Mini Architecture Decision Record

## Decision: Due Dates + Task Comments

### Context
The Task Tracker needs two new features: due dates with overdue filtering, and task comments. Both must integrate with the existing FastAPI backend, in-memory storage, and Kanban frontend.

### Feature 1: Due Dates
**Chosen approach:** Add optional due_date: Optional[date] field to TaskCreate, TaskUpdate, and TaskResponse models. Overdue detection is computed at query time in storage.py using date.today() comparison. Added overdue boolean query parameter to GET /tasks.

**Alternative considered (AI suggested):** AI proposed a scheduled background job to mark tasks as overdue and store an is_overdue boolean flag. Rejected because this adds unnecessary complexity for an in-memory store, introduces stale state, and a simple date comparison at query time is sufficient and always accurate.

**Alternative considered:** Computing overdue status only in the frontend JavaScript. Rejected because filtering must work at the API level for consistency and testability.

### Feature 2: Task Comments
**Chosen approach:** Flat comment storage using composite keys (	ask_id:comment_id) in a separate _comments dictionary. Endpoints nested under /tasks/{id}/comments. Comments deleted when parent task is deleted.

**Alternative considered (AI suggested):** AI proposed a SQLite database with foreign key relationships and cascade deletes. Rejected as out of scope for Module 1-3 in-memory architecture. The composite key approach achieves the same result without adding a database dependency.

**Alternative considered:** Storing comments as a list inside each task dictionary. Rejected because it makes individual comment deletion and ID-based lookup more complex.

### Stack
- Backend: FastAPI + Pydantic + in-memory dict storage
- Frontend: Vanilla HTML/CSS/JS Kanban board
- Tests: pytest + FastAPI TestClient
- No auth, no database, no Docker
