#!/bin/bash

echo "🧹 Starting AGGRESSIVE Traefik cleanup in namespace: job-application-microservices"

# Force delete Traefik deployment
echo "🗑️  Force deleting Traefik deployment..."
kubectl delete deployment traefik -n job-application-microservices --force --grace-period=0 --ignore-not-found=true

# Force delete Traefik service
echo "🗑️  Force deleting Traefik service..."
kubectl delete service traefik -n job-application-microservices --force --grace-period=0 --ignore-not-found=true

# Delete Traefik pods directly
echo "🗑️  Force deleting Traefik pods..."
kubectl delete pods -n job-application-microservices -l app=traefik --force --grace-period=0 --ignore-not-found=true

# Delete any pods with traefik in the name
kubectl get pods -n job-application-microservices | grep traefik | awk '{print $1}' | xargs -r kubectl delete pod -n job-application-microservices --force --grace-period=0

# Delete all resources with traefik label
echo "🔍 Cleaning up resources by label..."
kubectl delete all -n job-application-microservices -l app=traefik --force --grace-period=0 --ignore-not-found=true

# Delete specific resource types that might exist
echo "🗑️  Cleaning up specific resource types..."
kubectl delete configmap -n job-application-microservices -l app=traefik --ignore-not-found=true
kubectl delete secret -n job-application-microservices -l app=traefik --ignore-not-found=true
kubectl delete serviceaccount -n job-application-microservices traefik --ignore-not-found=true
kubectl delete ingress -n job-application-microservices --all --ignore-not-found=true

# Clean up any remaining ingress classes
kubectl delete ingressclass traefik --ignore-not-found=true

# Clean up cluster-wide resources
echo "🗑️  Cleaning up cluster-wide Traefik resources..."
kubectl delete clusterrole traefik --ignore-not-found=true
kubectl delete clusterrolebinding traefik --ignore-not-found=true

# Try to delete from YAML files if they exist
if [ -d "traefik" ]; then
    echo "🗑️  Deleting from YAML files..."
    cd traefik
    kubectl delete -f . --ignore-not-found=true --force --grace-period=0
    cd ..
fi

# Nuclear option - delete any resource with traefik in the name
echo "☢️  Nuclear cleanup - searching for any remaining traefik resources..."

# Get all resource types and check for traefik
for resource in $(kubectl api-resources --verbs=list --namespaced -o name); do
    kubectl get $resource -n job-application-microservices 2>/dev/null | grep -i traefik | awk '{print $1}' | xargs -r kubectl delete $resource -n job-application-microservices --force --grace-period=0 2>/dev/null
done

# Wait for cleanup to complete
echo "⏳ Waiting for cleanup to complete..."
sleep 10

# Verify cleanup
echo "✅ Cleanup complete! Verifying..."
echo ""
echo "📊 Current pods in namespace:"
kubectl get pods -n job-application-microservices

echo ""
echo "📊 Current services in namespace:"
kubectl get svc -n job-application-microservices

echo ""
echo "🔍 Checking for any remaining Traefik-related resources:"
kubectl get all -n job-application-microservices | grep -i traefik || echo "✅ No Traefik resources found - cleanup successful!"

echo ""
echo "🏁 AGGRESSIVE Traefik cleanup completed!"
