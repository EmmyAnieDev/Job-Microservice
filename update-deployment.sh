#!/bin/bash

# Script to update Kubernetes deployment files with new image tags

set -e

DEPLOYMENT_FILE="$1"
NEW_IMAGE_TAG="$2"
SERVICE_NAME="$3"

if [ -z "$DEPLOYMENT_FILE" ] || [ -z "$NEW_IMAGE_TAG" ] || [ -z "$SERVICE_NAME" ]; then
    echo "Usage: $0 <deployment-file> <new-image-tag> <service-name>"
    echo "Example: $0 ./eks-deployment-setup/auth/deployment.yaml emmaekwere/auth-service:1.0.1 auth-service"
    exit 1
fi

if [ ! -f "$DEPLOYMENT_FILE" ]; then
    echo "Error: Deployment file $DEPLOYMENT_FILE not found"
    exit 1
fi

echo "Updating deployment file: $DEPLOYMENT_FILE"
echo "New image tag: $NEW_IMAGE_TAG"
echo "Service name: $SERVICE_NAME"

# Create backup
cp "$DEPLOYMENT_FILE" "${DEPLOYMENT_FILE}.backup"

# Update the image tag using yq (more reliable than sed for YAML)
if command -v yq >/dev/null 2>&1; then
    # Using yq for precise YAML manipulation
    yq eval "(.spec.template.spec.containers[] | select(.name == \"$SERVICE_NAME\") | .image) = \"$NEW_IMAGE_TAG\"" -i "$DEPLOYMENT_FILE"
else
    # Fallback to sed if yq is not available
    echo "Warning: yq not found, using sed (less reliable for YAML)"
    
    # More precise sed pattern for updating image in Kubernetes deployment
    sed -i.bak "s|image: emmaekwere/${SERVICE_NAME}:[^[:space:]]*|image: ${NEW_IMAGE_TAG}|g" "$DEPLOYMENT_FILE"
fi

# Verify the change was made
if grep -q "$NEW_IMAGE_TAG" "$DEPLOYMENT_FILE"; then
    echo "✅ Successfully updated $DEPLOYMENT_FILE"
    echo "Image updated to: $NEW_IMAGE_TAG"
    
    # Show the specific line that was changed
    echo "Updated line:"
    grep -n "$NEW_IMAGE_TAG" "$DEPLOYMENT_FILE"
else
    echo "❌ Failed to update $DEPLOYMENT_FILE"
    echo "Restoring backup..."
    mv "${DEPLOYMENT_FILE}.backup" "$DEPLOYMENT_FILE"
    exit 1
fi

# Clean up backup if successful
rm -f "${DEPLOYMENT_FILE}.backup"

echo "Deployment file update completed successfully!"
