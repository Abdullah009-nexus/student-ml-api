# student-ml-api

Production-style MLOps workflow for a small ML inference API.

Traceability chain: **Pull Request → Commit → Git Tag → Docker Image**.

## Endpoints

- `GET /health`
- `POST /predict` with `{"value": 10}` → `{"input": 10, "prediction": 20}`

## Local commands

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
docker build -t student-ml-api:1.0.0 .
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0
curl http://localhost:5000/health
```

## Workflow policy

- Work only on feature branches.
- Merge to `main` only through Pull Requests after CI passes.
- CI (`ci.yml`) tests and validates `docker build`. It never publishes images.
- Release (`release.yml`) runs only on tags `v*.*.*`, derives `1.0.0` from `v1.0.0`, and publishes to GHCR:
  - `ghcr.io/<username>/student-ml-api:<version>`
  - `ghcr.io/<username>/student-ml-api:latest`
  - `ghcr.io/<username>/student-ml-api:<short-sha>`

See `ASSIGNMENT_REPORT.md` for branch protection, merge strategy, rollback, cache analysis, and failure analysis.
