#!/usr/bin/env bash
set -euo pipefail

# Step 1: Generate new self-signed certificate and private key
echo "Generating new TLS certificate and private key..."
openssl req -x509 -newkey rsa:4096 -sha256 -days 365 -nodes -keyout data/certs/new_site.key -out data/certs/new_site.crt -subj "/CN=localhost"

# Step 2: Update NGINX configuration
echo "Updating NGINX configuration to use the new certificates..."
sed -i 's|site.crt|new_site.crt|g' configs/nginx.conf
sed -i 's|site.key|new_site.key|g' configs/nginx.conf

# Step 3: Restart services via docker-compose
echo "Restarting services via docker-compose..."
docker-compose down
docker-compose up -d
