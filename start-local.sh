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
mkdir -p logs

# Start FastAPI application in background
echo "Starting FastAPI application..."
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 > logs/app.log 2>&1 &
APP_PID=$!

# Wait a moment for app to start
sleep 2

# Start Celery worker in background
echo "Starting Celery worker..."
poetry run celery -A tasks worker -l info > logs/celery.log 2>&1 &
CELERY_PID=$!

# Start Celery beat scheduler in background
echo "Starting Celery beat scheduler..."
poetry run celery -A tasks beat -l info > logs/celery-beat.log 2>&1 &
CELERY_BEAT_PID=$!

echo "Services started. App PID: $APP_PID, Celery PID: $CELERY_PID, Celery Beat PID: $CELERY_BEAT_PID"

# Wait for all processes
wait "$APP_PID" "$CELERY_PID" "$CELERY_BEAT_PID"
