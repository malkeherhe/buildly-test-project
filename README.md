# Buildly Project-Based Learning Platform

Buildly is a Django + React platform for managing project-based learning paths, learner enrollment, and practical programming projects.

## Scope

- Learners can register, log in, browse courses, join a course, and start a project.
- Admins can create and manage courses and projects.
- The repository now includes automated testing, CI/CD, a security check, and a performance smoke test for software testing coursework.

## Stack

- Backend: Django, Django REST Framework, SimpleJWT, SQLite
- Frontend: React, Vite, Axios
- E2E: Playwright
- CI/CD: GitHub Actions

## Structure

- `backendPBL/projectBPL`: Django backend
- `frontend`: React frontend
- `docs`: reports and testing artifacts
- `.github/workflows/ci.yml`: CI pipeline



## Local Run

### Backend

```bash
cd backendPBL/projectBPL
python -m venv ../venv
../venv/Scripts/pip install -r requirements.txt
copy .env.example .env
../venv/Scripts/python manage.py migrate
../venv/Scripts/python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Test Commands

### Backend unit and integration tests

```bash
cd backendPBL/projectBPL
../venv/Scripts/python manage.py test
```

### Security check

```bash
cd backendPBL/projectBPL
python scripts/security_check.py
```

### Frontend build

```bash
cd frontend
npm run build
```

### Playwright E2E

Start backend and frontend first, then run:

```bash
cd frontend
npx playwright install chromium
npm run test:e2e
```

## Assignment Coverage

- CI/CD pipeline with GitHub Actions
- Security check stage in CI
- Unit tests for core business logic
- Integration tests for real API behavior
- Playwright E2E test for a real learner scenario
- Performance smoke test script and report output

## Performance Testing

While the backend is running:

```bash
python backendPBL/projectBPL/scripts/performance_smoke.py --url http://127.0.0.1:8000/api/courses/
```

This writes a Markdown report to `docs/performance-report.md`.
If you test a protected API endpoint, pass a bearer token with `--token`.

## Notes

- Backend settings are environment-aware for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and CORS.
- Unicode console `print()` calls that caused Windows test/runtime failures were removed.


## GitLeaks (Secrets Scanning)

### Run in CI
GitLeaks runs automatically in GitHub Actions as part of the CI pipeline.

### Run locally with pre-commit
Install pre-commit first:

```bash
pip install pre-commit
pre-commit install
