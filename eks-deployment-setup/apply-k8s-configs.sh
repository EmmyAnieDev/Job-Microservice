#!/bin/bash

set -e

echo "🚀 Applying Kubernetes manifests in logical order..."

# === SHARED INFRASTRUCTURE FIRST ===
echo "📦 Applying Redis (shared dependency)..."
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
kubectl wait --for=condition=available --timeout=120s deployment/redis -n job-application-microservices

# === AUTH SERVICE ===
echo "🔐 Applying Auth service..."
kubectl apply -f auth/config.yaml
kubectl apply -f auth/secret.yaml
kubectl apply -f auth/postgres-deployment.yaml
kubectl apply -f auth/postgres-service.yaml

# Wait for Auth DB to be ready
echo "⏳ Waiting for Auth PostgreSQL to be ready..."
kubectl wait --for=condition=available --timeout=120s deployment/auth-postgres-deployment -n job-application-microservices

kubectl apply -f auth/service.yaml
kubectl apply -f auth/deployment.yaml

# === JOBS-APPLICATIONS SERVICE ===
echo "📋 Applying Jobs-Applications service..."
kubectl apply -f jobs-applications/config.yaml
kubectl apply -f jobs-applications/secret.yaml
kubectl apply -f jobs-applications/postgres-deployment.yaml
kubectl apply -f jobs-applications/postgres-service.yaml

# Wait for Jobs-Applications DB to be ready
echo "⏳ Waiting for Jobs-Applications PostgreSQL to be ready..."
kubectl wait --for=condition=available --timeout=120s deployment/jobs-applications-postgres-deployment -n job-application-microservices

kubectl apply -f jobs-applications/service.yaml
kubectl apply -f jobs-applications/deployment.yaml

# === JOBS-LISTING SERVICE ===
echo "📋 Applying Jobs-Listing service..."
kubectl apply -f jobs-listing/config.yaml
kubectl apply -f jobs-listing/secret.yaml
kubectl apply -f jobs-listing/postgres-deployment.yaml
kubectl apply -f jobs-listing/postgres-service.yaml

# Wait for Jobs-Listing DB to be ready
echo "⏳ Waiting for Jobs-Listing PostgreSQL to be ready..."
kubectl wait --for=condition=available --timeout=120s deployment/jobs-listing-postgres-deployment -n job-application-microservices

kubectl apply -f jobs-listing/service.yaml
kubectl apply -f jobs-listing/deployment.yaml

# === FINAL STATUS CHECK ===
echo "⏳ Waiting for all application deployments to be ready..."
kubectl wait --for=condition=available --timeout=180s deployment/auth-deployment -n job-application-microservices
kubectl wait --for=condition=available --timeout=180s deployment/jobs-applications-deployment -n job-application-microservices
kubectl wait --for=condition=available --timeout=180s deployment/jobs-listing-deployment -n job-application-microservices

echo ""
echo "✅ All manifests applied successfully!"
echo "📊 Final status check:"
kubectl get pods -n job-application-microservices
echo ""
kubectl get svc -n job-application-microservices