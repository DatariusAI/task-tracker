# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

I asked Claude to review app/main.py (the PATCH /tasks/{task_id} endpoint) for input validation, error handling, and HTTP status codes.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| CORS allow_origins=["*"] is too permissive for production | Useful | Correct observation. Wildcard CORS is a known development shortcut. However, this project is explicitly not production and has no auth, so the risk is accepted and documented. | Kept as-is. Added note in AGENTS.md that CORS is development-only. |
| The PATCH endpoint should validate that at least one field is provided in the update payload | Noise | Pydantic's exclude_unset=True already handles empty payloads gracefully. An empty PATCH returns the unchanged task, which is valid REST behavior. | No change. AI suggestion was technically valid but unnecessary for this scope. |
| Consider adding rate limiting to prevent abuse of the comment creation endpoint | Wrong for scope | This is a production hardening concern. The project rules explicitly prohibit new product features. Rate limiting would require adding a new dependency (slowapi) and middleware. | Rejected. Out of scope per project rules. |

## AI security mini-review

I asked Claude to perform a read-only security review of the Task Tracker codebase.

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| .env file was committed to git history exposing an Anthropic API key | .env (historical commit d2971d0) | Valid | GitHub Secret Scanning detected and revoked the key. The .env was removed from tracking and scrubbed from git history using git filter-branch. | Remediated. Key revoked by Anthropic. .env added to .gitignore. History rewritten. |
| No input length limit on comment text field | app/models.py CommentCreate | Valid | CommentCreate has min_length=1 but no max_length. A malicious user could submit extremely long comments consuming memory. | Accepted risk for course scope. Would add max_length=2000 in production. |
| In-memory storage has no persistence or backup | app/storage.py | Noise | This is by design. The project explicitly uses in-memory dicts. A database is out of scope per project rules and AGENTS.md. | No action. Documented as intentional design choice. |

## Manual security check
I manually checked the git history for leaked secrets by running git grep -l -i "[REDACTED-KEY-HINT] git grep -l -i "api_key", git grep -l -i "password", and git log --all --diff-filter=A -- .env. All four commands returned empty results, confirming no secrets remain in the tracked files or commit history. I also verified that .gitignore includes .env, venv/, node_modules/, .agents/, and .claude/ to prevent future accidental commits. The .dockerignore excludes .env and .git to prevent secrets from being baked into container images.

## One AI output I rejected or corrected
During the mid-course project, AI generated a delete_task function in storage.py that only removed the task from _tasks without cleaning up associated comments in _comments. I caught this during line-by-line code review. If accepted as-is, orphaned comments would have accumulated in memory and the test_delete_task_removes_comments test would have failed. I manually added cleanup logic that iterates through _comments and removes entries matching the deleted task_id prefix. This demonstrates that AI output requires careful review for cross-cutting concerns like data cleanup that the model may not anticipate.

## Three AI usage rules
1. Never paste: .env files, API keys, credentials, tokens, production logs, customer data, or any secret into AI prompts or commit them to the repo.
2. Always verify: Run pytest and check /health after every AI-generated code change. Review diffs line by line. Test edge cases AI may have missed.
3. Record AI contributions by: Documenting prompts, accepted/rejected suggestions, and corrections in docs/ files. Maintaining a prompt log with weak-to-strong rewrites.

## Ownership statement
I am comfortable submitting this repo as my own work because I reviewed every line of AI-generated code before accepting it, caught and corrected errors the AI missed (such as the missing cascade delete for comments), and made architectural decisions (such as rejecting SQLite and authentication suggestions) based on the project scope constraints. I ran all 22 tests locally, verified the API and frontend manually in the browser, and personally remediated a real security incident when an API key was accidentally committed. The documentation reflects my actual experience and decisions, not generic AI-generated statements.
