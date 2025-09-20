#!/usr/bin/env bash
set -euo pipefail

# Make sure we're in the script's directory
cd "$(dirname "$0")"

# Clean up any previous virtual environment setup
echo "Cleaning up any old virtual environment..."
rm -rf .venv

# Update package list and ensure necessary Python packages are installed
echo "Updating package list and installing python3-venv and python3-pip..."
sudo apt-get update
sudo apt-get install -y --reinstall python3-venv python3-pip

# Create and activate a Python virtual environment for tests
echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting docker services..."
docker-compose up -d --build --force-recreate

echo "Waiting for services to be ready..."
sleep 10

echo "Installing test dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest -q tests/test_outputs.py

echo "Cleaning up docker services..."
docker-compose down

# Deactivate the virtual environment
deactivate
