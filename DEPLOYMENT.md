# Deploying The API

## Local Development

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs on `http://127.0.0.1:8000`. Interactive docs are available at
`/docs`, and service health is exposed at `/health`.

## Environment Variables

| Variable | Purpose | Example |
| --- | --- | --- |
| `FRONTEND_ORIGINS` | Comma-separated frontend origins allowed by CORS. If unset, origins are unrestricted for local setup. | `https://your-frontend.vercel.app` |

For local configuration, copy the variable shown in `.env.example` into the
environment used to start the API.

## Render Deployment

This repository contains a Render Blueprint in `render.yaml`.

1. Push this backend repository to GitHub.
2. In Render, create a new Blueprint and select the backend repository.
3. Provide `FRONTEND_ORIGINS` when prompted, using the deployed frontend URL.
4. After deployment, set frontend `NEXT_PUBLIC_BACKEND_URL` to the Render
   service URL, such as `https://cfiback.onrender.com`.

The Blueprint configures Python, dependency installation, the Uvicorn start
command, and HTTP health checks at `/health`.
