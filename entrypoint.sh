#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting container setup..."

# It's a good practice to run migrations on every start.
echo "Applying database migrations..."
python3 manage.py migrate

# This is the command you wanted to automate!
echo "Adding initial data for employees and tasks..."
python3 manage.py add_data

echo "Setup complete. The application is now starting."

# This line executes the Dockerfile's CMD.
exec "$@"
