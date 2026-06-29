# Prompt Log

## Feature 1: Due Dates

### Prompt 1 (Weak -> Strong rewrite)
**Weak prompt:** "Add due dates to my task tracker."
**Rewritten strong prompt:** "You are a senior FastAPI developer. Using the existing app/models.py, app/storage.py, and app/main.py, add an optional due_date field of type date to TaskCreate, TaskUpdate, and TaskResponse. In storage.py, add an overdue parameter to list_tasks that filters tasks where due_date < date.today() and status is not Done. In main.py, add an overdue: bool = Query(False) parameter to the GET /tasks endpoint. Do not add authentication, a database, or new dependencies."
**AI returned:** Updated models with due_date field, storage filtering logic, and endpoint parameter. Accepted with minor edit: AI used datetime instead of date, corrected to date-only.

### Prompt 2
**Prompt:** "Write 5 pytest tests for the due date feature: create with valid due date, create with invalid date format, overdue filter returns only past-due non-Done tasks, update due date, and Done tasks excluded from overdue filter."
**AI returned:** Five well-structured tests using timedelta for relative dates. Accepted as-is, all tests passed on first run.

### Prompt 3
**Prompt:** "In frontend/index.html, add a date input for due_date in the task modal, show a red OVERDUE pill on cards where due_date is before today and status is not Done, show a gray due date pill for future dates, and add an Overdue Only checkbox filter that calls GET /tasks?overdue=true."
**AI returned:** Complete frontend updates. Edited: AI used 
ew Date() comparison which had timezone issues. Changed to ISO string comparison for consistency.

## Feature 2: Task Comments

### Prompt 1 (Weak -> Strong rewrite)
**Weak prompt:** "Add comments to tasks."
**Rewritten strong prompt:** "You are a senior FastAPI developer. Add a comment system to the Task Tracker. In app/models.py, add CommentCreate (text field, non-blank validated) and CommentResponse (id, task_id, text, created_at). In app/storage.py, add a _comments dict with composite keys task_id:comment_id, and functions add_comment, list_comments, delete_comment, count_comments. In app/main.py, add POST /tasks/{task_id}/comments (201), GET /tasks/{task_id}/comments, and DELETE /tasks/{task_id}/comments/{comment_id} (204). Return 404 if task not found. When a task is deleted, also remove its comments. Do not add auth or a database."
**AI returned:** Complete implementation matching spec. Accepted with one edit: AI initially did not handle cascade delete of comments when task is deleted. Added cleanup logic to delete_task.

### Prompt 2
**Prompt:** "Write 7 pytest tests for comments: add comment, reject blank comment, list comments, delete comment, comment on missing task returns 404, delete nonexistent comment returns 404, and deleting a task removes its comments."
**AI returned:** All 7 tests. Rejected one: AI had a test checking for 404 on delete of nonexistent comment but used wrong endpoint format. Rewrote the assertion.

### Prompt 3
**Prompt:** "In the edit task modal in frontend/index.html, add a comments section below the form fields. Show existing comments with a delete X button. Add a text input and Post button to add new comments. On the Kanban cards, show comment count if greater than 0."
**AI returned:** Frontend comment UI. Accepted with edit: moved comments section inside the modal scroll area to prevent overflow on tasks with many comments.
