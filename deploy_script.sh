#!/bin/bash

# Check if deploy_script.sh exists
if [ ! -f deploy_script.sh ]; then
    echo "Error: deploy_script.sh not found!"
    exit 1
fi

# Mock deployment (replace this with your actual deployment commands)
echo "Mock deploying to production..."

# Assume deployment was successful
echo "Deployment successful!"

# Exit with success status
exit 0
