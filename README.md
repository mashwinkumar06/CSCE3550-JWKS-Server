# CSCE 3550 Project 2 – SQLite JWKS Server

Student: Ashwin Kumar Mandaloju

Flask JWKS server that persists RSA private keys in `totally_not_my_privateKeys.db` and issues RS256 JWTs.

## Setup and run

```bash
python -m pip install -r requirements.txt
python app.py
```

Run from the project directory so the SQLite database is created in the current directory. The server listens on port 8080.

## API

- `GET /.well-known/jwks.json`: Returns public JWKs for all non-expired keys.
- `POST /auth`: Returns a signed JWT using a valid key. Accepts JSON or HTTP Basic auth without verifying credentials (mock authentication).
- `POST /auth?expired=true`: Returns a JWT signed with an expired key.

Database schema: `keys(kid INTEGER PRIMARY KEY AUTOINCREMENT, key BLOB NOT NULL, exp INTEGER NOT NULL)`.
Private keys are stored as PEM bytes. Queries use bound parameters for data values. Never commit the private key database to GitHub.

## Tests

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Run the course-provided Gradebot with its `project2` command while the server is running. Add screenshots of the Gradebot rubric and coverage output, with identifying information visible, under `screenshots/` before submitting the GitHub URL.
