# User Stories

## Feature 1: Due Dates + Overdue Filter

### Story 1: Add due date to a task
As a team member, I want to set an optional due date when creating or editing a task, so that I can track deadlines.
**Acceptance Criteria:**
- Due date is an optional date field on create and update
- Valid ISO date format accepted (YYYY-MM-DD)
- Invalid date format returns 422
- Task without due date shows null/no date
**AI Assumption Corrected:** AI initially suggested due_date as a datetime with time component. Corrected to date-only since time-level precision is unnecessary for a task tracker.

### Story 2: See overdue indicator on cards
As a team member, I want to see a visual "OVERDUE" pill on tasks past their due date, so that I can prioritize urgent work.
**Acceptance Criteria:**
- Tasks with due_date before today and status not Done show red OVERDUE pill
- Tasks with due_date in the future show gray due date pill
- Done tasks never show OVERDUE even if past due

### Story 3: Filter overdue tasks
As a team member, I want to filter the board to show only overdue tasks, so that I can focus on what needs immediate attention.
**Acceptance Criteria:**
- Overdue checkbox filters GET /tasks?overdue=true
- Only returns tasks with due_date < today AND status != Done
- Returns 200 with [] if no overdue tasks

### Story 4: Update due date
As a team member, I want to change or remove a due date on an existing task.
**Acceptance Criteria:**
- PATCH /tasks/{id} with due_date updates the date
- Setting due_date to null clears it
- Other fields remain unchanged

### Story 5: Overdue excludes completed tasks
As a team member, I want completed tasks to never appear as overdue, even if their due date has passed.
**Acceptance Criteria:**
- Done tasks with past due_date excluded from overdue filter
- Done tasks with past due_date do not show OVERDUE pill

## Feature 2: Task Comments

### Story 1: Add a comment to a task
As a team member, I want to add a text comment to any task so that I can leave notes or updates.
**Acceptance Criteria:**
- POST /tasks/{id}/comments with non-blank text creates comment
- Returns 201 with comment id, task_id, text, created_at
- Blank or whitespace-only text returns 422
- Comment on nonexistent task returns 404
**AI Assumption Corrected:** AI initially included an author/user field. Removed since Module 1 scope has no authentication.

### Story 2: View comments on a task
As a team member, I want to see all comments for a task sorted by creation time.
**Acceptance Criteria:**
- GET /tasks/{id}/comments returns list sorted oldest-first
- Returns 200 with [] if task exists but has no comments
- Returns 404 if task does not exist

### Story 3: Delete a comment
As a team member, I want to remove a comment I no longer need.
**Acceptance Criteria:**
- DELETE /tasks/{id}/comments/{comment_id} returns 204
- Returns 404 if task or comment not found

### Story 4: See comment count on cards
As a team member, I want to see how many comments a task has on the Kanban card.
**Acceptance Criteria:**
- Cards show comment count if > 0
- Cards with 0 comments show no indicator

### Story 5: Deleting a task removes its comments
As a team member, I expect that when a task is deleted, all its comments are also removed.
**Acceptance Criteria:**
- DELETE /tasks/{id} removes task and all associated comments
- GET /tasks/{id}/comments returns 404 after task deletion
