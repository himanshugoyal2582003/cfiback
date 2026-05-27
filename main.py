"""ASGI entrypoint for hosts configured with `uvicorn main:app`."""

from app.main import app


__all__ = ["app"]
