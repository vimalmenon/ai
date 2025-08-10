#!/bin/bash

# Exit on any error
set -e

# Function to handle graceful shutdown
cleanup() {
    echo "Shutting down services..."
    kill -TERM "$APP_PID" "$CELERY_PID" "$CELERY_BEAT_PID" 2>/dev/null || true
    wait "$APP_PID" "$CELERY_PID" "$CELERY_BEAT_PID" 2>/dev/null || true
    echo "Services stopped."
    exit 0
}

# Trap signals for graceful shutdown
trap cleanup SIGTERM SIGINT

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Start FastAPI application in background
echo "Starting FastAPI application..."
/app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > /app/logs/app.log 2>&1 &
APP_PID=$!

# Wait a moment for app to start
sleep 2

# Start Celery worker in background
echo "Starting Celery worker..."
/app/.venv/bin/celery -A tasks worker -l info > /app/logs/celery.log 2>&1 &
CELERY_PID=$!

# Start Celery beat scheduler in background
echo "Starting Celery beat scheduler..."
/app/.venv/bin/celery -A tasks beat -l info > /app/logs/celery-beat.log 2>&1 &
CELERY_BEAT_PID=$!

echo "Services started. App PID: $APP_PID, Celery PID: $CELERY_PID, Celery Beat PID: $CELERY_BEAT_PID"

# Wait for all processes
wait "$APP_PID" "$CELERY_PID" "$CELERY_BEAT_PID"
