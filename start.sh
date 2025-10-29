#!/usr/bin/env bash
# Start script for Render

echo "Starting Gunicorn server..."
exec gunicorn app:app \
    --workers=1 \
    --threads=2 \
    --timeout=120 \
    --bind=0.0.0.0:${PORT:-8000} \
    --access-logfile=- \
    --error-logfile=- \
    --log-level=info
