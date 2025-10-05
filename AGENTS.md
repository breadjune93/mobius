# Repository Guidelines
Mobius combines a FastAPI backend with AI orchestration modules; use this guide to stay aligned.

## Project Structure & Module Organization
- pp/ houses the FastAPI service; key modules include core/ (settings, middleware), db/ (SQLAlchemy engine + repositories), pi/v1/ (routers, schemas, services), and web/ for Jinja templates plus static assets under web/static/{css,js,image}.
- i/ contains persona prompts and LangChain integrations; extend tools under i/tools/ and keep shared prompts in system_prompt.py.
- gent/ exposes utility entry points for tool-backed agents; reuse rather than duplicating orchestration code.
- Secrets live in .env (see pp/core/config.py); never commit real values.

## Build, Test, and Development Commands
- python -m venv .venv && .venv\Scripts\activate creates an isolated environment (PowerShell example).
- python -m pip install fastapi uvicorn "python-dotenv" sqlalchemy langchain-openai langchain-anthropic syncs runtime dependencies; mirror this in equirements.txt updates.
- uvicorn app.main:app --reload --host 127.0.0.1 --port 1993 starts the API and web UI with hot reload.
- pytest -q runs the test suite; add --maxfail=1 when iterating on failures.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation and snake_case for modules, functions, and SQLAlchemy models.
- Use explicit type hints and FastAPI pydantic schemas for request/response models.
- Group related database logic inside repository classes (pp/db/repositories/), and keep web templates in web/templates/ with kebab-case filenames.

## Testing Guidelines
- Place unit and integration tests under 	ests/ mirroring the package layout (	ests/api/test_workspace_router.py, etc.).
- Prefer pytest fixtures to isolate DB state; use SessionLocal factories and a disposable DATABASE_URL (e.g., SQLite) for CI.
- Target meaningful coverage of routers, services, and security helpers before opening a PR.

## Commit & Pull Request Guidelines
- Write concise, imperative commit subjects (Korean or English are fine); the log favors short verbs such as “로그인 프로세스 재정의”.
- Reference issues in the body, describe user-visible changes, and attach screenshots for web UI tweaks.
- PRs must list setup steps, test evidence (pytest output, manual QA), and highlight any schema or environment changes.

## Environment & Security Tips
- Keep .env restricted locally; share sample variables via .env.example.
- Rotate API keys and database credentials regularly, and ensure BCRYPT_ROUNDS stays aligned with security requirements before deployment.
