# Personal AI Playbook

## When I reach for AI first
- Scaffolding boilerplate: Pydantic models, FastAPI endpoint stubs, pytest fixtures, Dockerfile templates, and CI workflows. These have predictable structure and AI drafts save time.
- Writing first-draft documentation: user stories, ADRs, README sections. AI produces a starting point I can edit faster than writing from scratch.
- Debugging with evidence: when I have a failing test name, error traceback, and the relevant code, a targeted AI prompt returns useful fixes faster than searching Stack Overflow.
- Rewriting weak prompts into strong prompts: asking AI to critique and improve my own prompts before using them for code generation.

## When I do not reach for AI first
- Architecture decisions: AI defaults to complex solutions (databases, microservices, auth) unless explicitly constrained. I decide the scope first, then ask AI to implement within those bounds.
- Security-sensitive work: secrets management, credential handling, and .gitignore configuration. I verify these manually because AI cannot see my actual environment or git history.
- Understanding unfamiliar code: when I encounter code I do not understand, I read it myself first. Using AI to explain code I have not read creates a false sense of understanding.
- Debugging without evidence: asking AI to "fix my code" without a specific error, test name, or expected vs actual output produces vague or wrong suggestions.

## My non-negotiables
- Never paste API keys, .env contents, credentials, or customer data into AI prompts.
- Never commit without running the test suite first.
- Never accept AI output I cannot explain line by line.
- Always check .gitignore covers .env, venv/, and secret files before the first push of any project.
- Always use git filter-branch or BFG to scrub secrets from history if accidentally committed, then force push.

## My review rules
- Review AI diffs line by line, not just the summary.
- Run pytest -v after every AI-generated change.
- Check for cross-cutting concerns AI often misses: cascade deletes, edge cases for empty/whitespace input, correct HTTP status codes.
- Grade AI suggestions as Useful, Noise, or Wrong. Reject Wrong and Noise suggestions explicitly.
- If AI suggests adding scope (auth, database, new features), reject and re-constrain the prompt.

## What I am still figuring out
- How to best split work between editor-based AI (Cursor) and chat-based AI (Claude) for different task types.
- When to use AI for test generation vs writing tests myself to catch edge cases AI might not think of.
- How to evaluate competing AI suggestions when both sound reasonable but take the project in different directions.
- Team norms for AI usage: how much AI-generated code is acceptable, and how to document it transparently for code review.

## Decision Card
| Situation | Rule |
|---|---|
| New feature | Scope first, then prompt AI with explicit constraints and exclusions |
| Code review | AI reviews for patterns; I verify logic, edge cases, and cross-cutting concerns |
| Debugging | Paste the exact error, failing test, and relevant code; ask for a targeted fix only |
| Infrastructure (CI/Docker) | AI drafts the template; I verify every line and test locally |
| Never paste | Secrets, .env, API keys, credentials, tokens, production logs, customer data |
| One rule | If I cannot explain it, I do not commit it |
