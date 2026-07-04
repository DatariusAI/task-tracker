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

Read-only security mini-review of the Task Tracker (Python/FastAPI, in-memory, unauthenticated **by design**). Scans run: `pip-audit -r requirements.txt`, `bandit -r app -q`, a secrets grep, and manual runtime probes against a locally-served instance. No code was modified in this session; warranted fixes are listed under "Proposed app/ changes — needs human sign-off".

### Surface map (Step 1 evidence)
- Entrypoint: `app/main.py` — `app = FastAPI(title="Task Tracker API")` (`main.py:8`), no `debug=True`.
- Routes (all unauthenticated by design): `GET /health` (`main.py:17`), `POST /tasks` (`:21`), `GET /tasks` (`:25`), `GET /tasks/{task_id}` (`:37`), `PATCH /tasks/{task_id}` (`:44`), `DELETE /tasks/{task_id}` (`:57`), `POST /tasks/{task_id}/comments` (`:62`), `GET /tasks/{task_id}/comments` (`:69`), `DELETE /tasks/{task_id}/comments/{comment_id}` (`:76`).
- Store: in-memory dicts `_tasks` / `_comments` (`app/storage.py:5-6`); server generates `id` (uuid4) and `created_at` (`storage.py:9,17`).
- CORS: `allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`, **no** `allow_credentials` (`main.py:10-15`).
- Middleware: only `CORSMiddleware`. Error handling: FastAPI/Pydantic defaults (structured 422, no traceback). Input validation: Pydantic models with `Field` constraints and `field_validator` (`app/models.py:17-65`).

### Findings table (Step 3)

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Vulnerable transitive dependency: **starlette 0.38.6** (pulled by `fastapi==0.115.0`) | `requirements.txt:1`; `pip-audit -r requirements.txt` → 7 advisories: CVE-2024-47874 (multipart DoS, fix 0.40.0), CVE-2025-54121 (fix 0.47.2), PYSEC-2026-161 (fix 1.0.1), PYSEC-2026-248 (fix 1.3.0), PYSEC-2026-249 (fix 1.3.1), CVE-2026-48817/48818 (fix 1.1.0) | **Valid** | Real, currently-installed CVEs. Highest impact is CVE-2024-47874 (unbounded multipart → DoS). App does not use multipart today, but the vulnerable code ships. | **Fixed.** Bumped `fastapi==0.139.0` (resolver pulled `starlette==1.3.1`); `pip-audit -r requirements.txt` → *No known vulnerabilities found*; 22/22 tests green. |
| Vulnerable dev dependency: **pytest 8.3.3** | `requirements.txt:4`; `pip-audit` → CVE-2025-71176 (fix 9.0.3) | **Valid (low)** | Dev/test-only, never shipped to a runtime. Low risk. | **Fixed.** Bumped to `pytest==9.1.1`. |
| Stored XSS in frontend rendering | `frontend/index.html:127` (`'<h3>' + t.title`), `:128` (assignee), `:207` (`'<span>' + c.text`) — user text concatenated into `innerHTML` unescaped | **Valid** | A task title or comment such as `<img src=x onerror=alert(document.cookie)>` is stored verbatim by the API (correct for an API — no HTML stripping) and executes when the SPA renders it. This is a **client-side** defect; the API is behaving correctly by returning raw data. | **Fixed.** Render rebuilt with `textContent` (parser-proof) instead of an `esc()` helper; no live `innerHTML` sink remains for user data. Verified payload renders as literal text. |
| CORS wildcard `allow_origins=["*"]` | `main.py:11-15`; runtime `OPTIONS /tasks` → `access-control-allow-origin: *`, **no** `access-control-allow-credentials` | **Valid (low, demo)** | Any origin may call the API from a browser. Severity is low here: no `allow_credentials`, no cookies, and no auth, so there is no cross-origin credential/session to steal. Already documented as development-only in AGENTS.md. | Accepted risk for course scope. Optional env-allowlist noted, not applied (would be a config change). |
| No comment/description length cap | `app/models.py:57-58` `CommentCreate.text = Field(..., min_length=1)` (no `max_length`); `description`/`assignee` also unbounded (`:19,:22`) | **Valid (low)** | Unbounded strings in an in-memory store are a memory-exhaustion vector. `title` is capped at 200 (`:18`) but `text`/`description`/`assignee` are not. | **Fixed.** Added `max_length` in `app/models.py` (title/assignee 200, description/comment-text 2000, on both create and update). Verified 422 on oversize. |
| Missing security response headers (CSP, X-Content-Type-Options, X-Frame-Options, HSTS) | runtime `GET /health` → only `date`, `server`, `content-type` | **Valid (low)** | Low impact for a JSON API with no auth/cookies; relevant mainly to the static frontend. | Optional hardening middleware noted, not applied (out-of-scope config add). |
| No request body-size limit | `main.py` — no size guard; Starlette imposes no default cap | **Valid (low)** | Large payloads could exhaust memory. Mitigated in practice by the length caps above once added. | **Fixed (folded).** Request body is now bounded by the `max_length` caps applied to every string field. |
| SQL / NoSQL / command / path injection | `bandit -r app -q` → **0 issues**; no DB, no `os`/`subprocess`, no `open()` on user paths, no `eval`; all input Pydantic-typed | **False Positive** | There is no query language, shell, or filesystem sink to inject into. Pydantic coerces/validates every field. Nothing to exploit. | None. Reason recorded as grading evidence. |
| Mass assignment (client sets server-owned fields) | runtime `POST /tasks` with `{"id":"ATTACKER-SET","created_at":"1999-...","bogus":"x"}` → response `id` was a fresh uuid, `created_at` was server-now, `bogus` dropped | **False Positive** | Pydantic ignores unknown fields; `id`/`created_at` are generated in `storage.add_task` (`storage.py:9,17`) and never read from the request body. Attacker input has no effect. | None. |
| Verbose errors / debug mode leakage | runtime malformed JSON → `422` structured Pydantic error, **no traceback**; `debug=True` absent; `server: uvicorn` header carries no version | **Noise / False Positive** | FastAPI returns generic structured errors, not internals. No stack traces or version disclosure to clients. | None. |
| Secrets grep flags `./.env` | `grep` hit on `.env:1` (the `ANTHROPIC_API_KEY` line; value redacted, never written to any doc) | **Valid handling / not a repo leak** | `.env` is git-ignored, **not tracked**, and the on-disk key was verified **never** committed to this repo's history (all-branch blob search → 0 hits). The grep matches the local working-tree file only. Value never written to any doc. | Operational: rotate the live key as cheap insurance (public repo). Nothing to fix in tracked files. |
| No authentication / broken access control | No auth layer on any route (`main.py`) | **INFO / out-of-scope (intentional)** | "No authentication" is a stated design fact of the brief, not a vulnerability. With a single shared in-memory store and no user model, there is no per-user resource and therefore no cross-user (IDOR) access surface to violate. | Recorded as intentional. No change. |
| No rate limiting | absent | **INFO / out-of-scope** | Adding rate limiting requires a new dependency (e.g. slowapi) + middleware — a new product feature the brief forbids. | Deferred. Noted only. |

### Manual security check (this review)
I served the app locally (`uvicorn app.main:app`) and ran three checks by hand rather than trusting the scan output:

1. **`/health` leaks nothing.** `curl -i http://127.0.0.1:8011/health` returned `HTTP/1.1 200 OK` with body `{"status":"ok"}` and headers limited to `date`, `server: uvicorn` (no version), `content-length`, `content-type`. Confirmed: no framework version, no stack, no internal path disclosed.
2. **One endpoint traced for unintended field writes.** I POSTed a task with attacker-controlled `id`, `created_at`, and an unknown `bogus` field. The response `id` was a server-generated uuid, `created_at` was the server clock, and `bogus` was absent — confirming `storage.add_task` (`storage.py:8-21`) writes only model-derived fields and the request cannot forge server-owned state.
3. **No cross-user access surface (intentional).** I confirmed by reading `storage.py` that there is a single shared `_tasks`/`_comments` namespace and no user/owner column anywhere. Because there is no per-user resource, the "can user A read user B's tasks" (IDOR) question has no surface in this design. This is intentional per the brief and is recorded as INFO, not a finding.

### One AI output I rejected or corrected (this review)
An earlier AI security prompt (a Node/Express-oriented "audit and harden" spec) recommended **adding full authentication plus per-resource ownership guards** on every route (JWT verification, bcrypt password hashing, `owner_id` checks). I **rejected** this: the course brief explicitly designates the API as unauthenticated **by design** and forbids adding new product features. Implementing auth would have been a large, behavior-changing feature well outside scope. Instead I recorded "no authentication" as an intentional **INFO / out-of-scope** finding and verified (see manual check #3) that the single-shared-store design has no cross-user access surface to guard. The same prompt also assumed a Node.js/Express + MongoDB stack (`npm audit`, `helmet`, `express-mongo-sanitize`, `alg:none` JWT checks); none of it applied to this Python/FastAPI/in-memory app, so those checks were discarded rather than force-fit into fabricated findings.

Second correction (applied during remediation): the AI's proposed XSS fix was an `esc()` HTML-entity-encoder helper that would still feed user text into `innerHTML`. I **corrected** this to render the plain-text fields (task title, assignee, comment text) via `textContent`. `textContent` never invokes the HTML parser, so it cannot be defeated by a bug or omission in an escaping function — it is a strictly stronger, parser-proof fix. The render functions in `frontend/index.html` were rebuilt with `document.createElement` + `textContent` and now contain **no** `innerHTML` sink for user data.

### Proposed app/ changes — needs human sign-off
**Status: signed off and APPLIED** (P1, P2, P3). Each was applied as a security fix, gated on the green test baseline (22/22 preserved) and re-audited. The original proposed diffs are retained below for the record; the applied form of P3 uses `textContent` rather than the `esc()` helper shown (see "One AI output I rejected or corrected" — the stronger, parser-proof fix). Verified with `pytest -q` and `pip-audit -r requirements.txt`.

**P1 — Dependency bump (security, `requirements.txt`).** Clears the starlette + pytest CVEs above. Exact pins depend on the latest releases your resolver sees; the intent is "bump `fastapi` until it pulls a patched `starlette` (>=1.3.1 clears all listed advisories), and bump `pytest`." Verify by re-running `pip-audit -r requirements.txt` until zero starlette/pytest advisories remain, then `pytest tests/ -v`.
```diff
--- a/requirements.txt
+++ b/requirements.txt
@@
-fastapi==0.115.0
-uvicorn==0.30.6
-httpx==0.27.2
-pytest==8.3.3
+fastapi>=0.118.0          # pulls patched starlette (>=1.3.1); confirm exact version via pip-audit
+starlette>=1.3.1          # explicit floor: clears CVE-2024-47874 / CVE-2025-54121 / PYSEC-2026-161/248/249 / CVE-2026-48817/48818
+uvicorn==0.30.6
+httpx==0.27.2
+pytest>=9.0.3             # clears CVE-2025-71176 (dev-only)
```
> Caveat: `fastapi==0.115.0` pins `starlette<0.42`, so starlette cannot be bumped without also bumping fastapi. Treat the versions above as a starting point and let the resolver + `pip-audit` confirm a compatible, advisory-free set. This must be run and tested by a human, not applied blind.

**P2 — Input length caps (security, `app/models.py`).** Bounds unbounded strings against memory exhaustion in the in-memory store. Behavior-preserving for all existing tests (they use short strings).
```diff
--- a/app/models.py
+++ b/app/models.py
@@ class TaskCreate(BaseModel):
     title: str = Field(..., min_length=1, max_length=200)
-    description: Optional[str] = None
+    description: Optional[str] = Field(None, max_length=2000)
     status: TaskStatus = TaskStatus.ToDo
     priority: TaskPriority = TaskPriority.Medium
-    assignee: Optional[str] = None
+    assignee: Optional[str] = Field(None, max_length=200)
     due_date: Optional[date] = None
@@ class CommentCreate(BaseModel):
-    text: str = Field(..., min_length=1)
+    text: str = Field(..., min_length=1, max_length=2000)
```
> Note: `TaskUpdate.description`/`assignee` (`models.py:34,37`) would take the same caps for consistency if you apply this.

**P3 — Escape user text in the frontend (security, `frontend/index.html`).** Closes the stored-XSS finding. Adds one helper and wraps the three user-controlled string sinks. No API change.
```diff
--- a/frontend/index.html
+++ b/frontend/index.html
@@
 const API = "http://127.0.0.1:8000";
+function esc(s){return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
 let commentCounts = {};
@@ in loadTasks() card template
-        '<h3>' + t.title + '</h3>' +
-        '<div class="meta">' + t.priority + (t.assignee ? ' &middot; ' + t.assignee : '') + '</div>' +
+        '<h3>' + esc(t.title) + '</h3>' +
+        '<div class="meta">' + t.priority + (t.assignee ? ' &middot; ' + esc(t.assignee) + '' : '') + '</div>' +
@@ in loadComments()
-    '<div class="comment-item"><span>' + c.text + '</span><button class="del-comment" onclick="deleteComment(\'' + taskId + '\',\'' + c.id + '\')">&times;</button></div>'
+    '<div class="comment-item"><span>' + esc(c.text) + '</span><button class="del-comment" onclick="deleteComment(\'' + taskId + '\',\'' + c.id + '\')">&times;</button></div>'
```
> `t.priority`, `t.due_date`, `t.id`, `c.id` are server-controlled enums/uuids/dates and are not user free-text, so they are lower risk; escaping the three free-text sinks (`title`, `assignee`, `text`) closes the practical XSS.

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
