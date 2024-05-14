#!/bin/bash

# Check if deploy_script.sh exists
if [ ! -f deploy_script.sh ]; then
    echo "Error: deploy_script.sh not found!"
    exit 1
fi

# Deploy to production
echo "Deploying to production..."
./deploy_script.sh
