#!/usr/bin/env bash

alembic revision -m "init" --autogenerate

alembic upgrade head

gunicorn --timeout=30 app.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000