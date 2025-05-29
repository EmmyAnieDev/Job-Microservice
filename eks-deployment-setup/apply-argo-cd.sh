#!/bin/bash

# Step 1: Install ArgoCD
echo "🛠 Creating ArgoCD namespace..."
kubectl create namespace argocd

echo "📦 Installing ArgoCD components..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
sleep 10

# Step 2: Port-forward ArgoCD UI (using 8081 if 8080 is busy)
echo "🌐 Checking if port 8080 is available..."
if lsof -i :8080 >/dev/null; then
  echo "⚠️ Port 8080 is in use. Forwarding ArgoCD to port 8081 instead..."
  PORT=8081
else
  PORT=8080
fi

echo "🚪 Port-forwarding ArgoCD server to localhost:$PORT ..."
kubectl port-forward svc/argocd-server $PORT:443 -n argocd &
sleep 10

# Step 3: Get initial ArgoCD admin password
echo "🔑 Fetching initial ArgoCD admin password..."
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode && echo

# Step 4 (optional): Change or delete the default password
# echo "🔒 Changing ArgoCD admin password..."
# argocd login localhost:$PORT --username admin --password <old-password> --insecure
# argocd account update-password

# echo "🧹 Deleting initial admin secret (optional cleanup)..."
# kubectl -n argocd delete secret argocd-initial-admin-secret

echo "✅ Done! Open your browser and navigate to: https://localhost:$PORT"
echo "Login with username: admin and the password above."
