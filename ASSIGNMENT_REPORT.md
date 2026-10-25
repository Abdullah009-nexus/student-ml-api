# Assignment Report — student-ml-api

Professional CI workflow with Pull Requests, Docker, and GHCR.

GitHub username used in this project: `Abdullah009-nexus`.

## Part 7 — Branch protection on `main`

Configure these settings in GitHub → Settings → Branches → Add rule for `main`:

- Require a pull request before merging
- Require status checks to pass before merging (`Unit tests`, `Docker build validation`)
- Do not allow bypassing the above settings (if available)
- Restrict who can push to matching branches (no direct pushes to `main`)

These settings match the policy that `main` only receives reviewed, CI-validated work.

## Part 8 — Merge strategy

Selected strategy: **Squash and Merge**.

Justification: each feature PR becomes one clean commit on `main`, which maps cleanly to a later Git tag (`v1.0.0`, `v1.1.0`) and Docker image. Feature-branch noise (including the deliberate failing CI commit) stays off `main`.

## Part 11 — Docker inspection (fill after local run)

| Item | Value |
| --- | --- |
| Container ID | _to be recorded after `docker inspect`_ |
| Image ID | _to be recorded_ |
| Exposed port | `5000/tcp` mapped to host `5000` |
| Running command | `python app.py` |
| Working directory | `/app` |

## Part 16 — Registry

Expected images after releases:

- `ghcr.io/Abdullah009-nexus/student-ml-api:1.0.0`
- `ghcr.io/Abdullah009-nexus/student-ml-api:1.1.0`
- `ghcr.io/Abdullah009-nexus/student-ml-api:latest`

Record digests after the release workflow succeeds.

## Part 20 — Rollback

Without rebuilding source, restore the known-good artifact:

```bash
docker stop student-ml-api
docker rm student-ml-api
docker run -d --name student-ml-api -p 5000:5000 ghcr.io/Abdullah009-nexus/student-ml-api:1.0.0
curl http://localhost:5000/health
```

This is easier than `git clone` + `pip install` + `python app.py` because the registry already holds an immutable, tested runtime. You do not reinstall dependencies or hope the local Python matches CI.

## Part 21 — Traceability for 1.1.0

Fill from the real repository after merge and release:

- PR number:
- Merge commit SHA:
- Git tag: `v1.1.0`
- Docker image: `student-ml-api:1.1.0`
- Image digest:

## Part 22 — Why CI must not publish images

Publishing from every Pull Request would:

- Publish unreviewed and possibly broken code
- Pollute the registry with throwaway tags
- Make `latest` unsafe
- Mix experimental work with production artifacts

CI validates. Release publishes only after merge + semantic version tag.

## Part 24 — Commit SHA image tag

A commit-specific tag (`student-ml-api:92f4abc`) identifies the exact Git revision that produced the image, even if semantic tags move or are reused incorrectly. It is the fastest way to answer: which source commit built this artifact?

## Part 25 — Docker layer cache

Preferred order:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py VERSION ./
```

Changing only `app.py` reuses the pip-install layer. Changing `requirements.txt` invalidates that layer and reinstalls packages. `COPY . .` before `pip install` busts the dependency layer on every source change and slows CI.

## Part 26 — Failure analysis

### Failure 1 — Failed pytest (mandatory CI demonstration)

- **Symptom:** GitHub Actions CI red; `Unit tests` job fails.
- **Root cause:** Health test asserted `status == "wrong"` instead of `"healthy"`.
- **Evidence:** Failed CI run on `feature/prediction-api` before the fix commit.
- **Correction:** `assert data["status"] == "healthy"` and commit `fix: correct health endpoint test`.

### Failure 2 — Missing dependency

- **Symptom:** Image or local run crashes with `ModuleNotFoundError: No module named 'flask'`.
- **Root cause:** Flask not listed in `requirements.txt` (or not installed in the image).
- **Evidence:** `docker logs` or pytest import error.
- **Correction:** Pin Flask in `requirements.txt` and rebuild so the install layer includes it.

### Failure 3 — Wrong container port (diagnosis, not left broken)

- **Symptom:** `curl http://localhost:5000/health` fails while the container is running.
- **Root cause:** Host mapping used a different port than 5000, or the app was bound to `127.0.0.1` so it was unreachable from outside the container.
- **Evidence:** `docker ps` port column; `docker inspect` `HostConfig.PortBindings`; app `app.run(host=...)`.
- **Correction:** `app.run(host="0.0.0.0", port=5000)` and `docker run -p 5000:5000`.

## Core principle

Git manages source evolution. Pull Requests control entry to `main`. CI verifies changes. Docker turns approved source into a reproducible artifact. GHCR stores versioned artifacts for consistent delivery and rollback.
