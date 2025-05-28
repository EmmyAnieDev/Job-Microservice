#!/bin/bash

# This script handles database migrations for all services

echo "Starting database migrations for all services..."

# -----------  Auth Service Migration Script (Laravel) --------------
echo "Running Auth Service Migration..."
POD_NAME=$(kubectl get pods -n job-application-microservices -l app=auth -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -n job-application-microservices -- php artisan migrate

# -----------  Jobs Listing Service Migration Script (Flask) --------------
echo "Running Jobs Listing Service Migration..."
POD_NAME=$(kubectl get pods -n job-application-microservices -l app=jobs-listing -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -n job-application-microservices -- alembic upgrade head

# -----------  Jobs Applications Service Migration Script (FastAPI) --------------
echo "Running Jobs Applications Service Migration..."
POD_NAME=$(kubectl get pods -n job-application-microservices -l app=jobs-applications -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -n job-application-microservices -- alembic upgrade head

echo "All migrations completed!"