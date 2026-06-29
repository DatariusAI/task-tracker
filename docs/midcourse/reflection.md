# Reflection

## AI Tools Used
I used Claude as my primary AI assistant for planning, code generation, prompt design, and documentation. For code editing, I used VS Code to review and apply changes. All code was run and tested locally using pytest and uvicorn before accepting.

## One Moment AI Helped
The strongest moment was during comment system design. When I asked for a comment storage approach, AI suggested using composite dictionary keys (task_id:comment_id) instead of nested lists inside task objects. This was a better design because it made individual comment lookup and deletion O(1) and kept the storage layer consistent with the existing flat dictionary pattern. I would not have immediately considered this approach, and it saved time during implementation.

## One Moment AI Slowed Me Down
When implementing due dates, AI initially generated datetime fields instead of date-only fields and proposed a background scheduler to flag overdue tasks. This was overengineered for an in-memory task tracker. I had to reject the suggestion, specify the simpler approach, and re-prompt with tighter constraints. The lesson is that AI defaults to complex solutions unless the prompt explicitly constrains the scope and architecture.

## One Place Where My Review Changed the Result
During the comment feature, AI did not include cascade deletion of comments when a task is deleted. The generated delete_task function only removed the task from _tasks without touching _comments. I caught this during code review and added the cleanup logic that iterates through _comments and removes entries matching the deleted task_id. Without this review, orphaned comments would have accumulated in memory and the test_delete_task_removes_comments test would have failed. This reinforced that AI-generated code needs line-by-line inspection, especially for cross-cutting concerns like data cleanup.

## Key Takeaway
The most valuable skill in AI-assisted coding is not prompt writing but prompt constraining. The tighter the boundaries I set (specific files, specific models, explicit exclusions), the more usable the output. AI works best as a junior collaborator: give it clear context, review everything, and never skip testing.
