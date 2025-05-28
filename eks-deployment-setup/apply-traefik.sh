#!/bin/bash

# Navigate to traefik directory
cd traefik

echo "🚀 Starting Traefik deployment..."

# 1. Apply RBAC first (permissions needed before deployment)
echo "📋 Applying RBAC configuration..."
kubectl apply -f rbac.yaml

# 2. Apply IngressClass (defines the ingress controller)
echo "🔧 Applying IngressClass..."
kubectl apply -f ingressclass.yaml

# 3. Apply Middleware (traffic handling rules)
echo "⚙️  Applying Middleware configuration..."
kubectl apply -f middleware.yaml

# 4. Apply Deployment (the actual Traefik pods)
echo "🏗️  Deploying Traefik pods..."
kubectl apply -f deployment.yaml

# 5. Apply Service (exposes Traefik)
echo "🌐 Creating Traefik service..."
kubectl apply -f service.yaml

# 6. Apply Ingress (routing rules)
echo "🛣️  Applying Ingress configuration..."
kubectl apply -f ingress.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for Traefik deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/traefik-deployment -n job-application-microservices

# Get your new load balancer URL
echo "✅ Traefik deployment complete!"
echo "🔗 Getting load balancer information..."
kubectl get svc traefik-service -n job-application-microservices

echo ""
echo "📊 Traefik pod status:"
kubectl get pods -n job-application-microservices -l app=traefik

echo ""
echo "🎯 Load balancer external IP (may take a few minutes to provision):"
kubectl get svc traefik-service -n job-application-microservices -o jsonpath='{.status.loadBalancer.ingress[0].ip}{.status.loadBalancer.ingress[0].hostname}{"\n"}'