#!/bin/bash
cd /c/1-Projects/pygeoapi

# Set environment variables
export PYGEOAPI_CONFIG="/c/1-Projects/pygeoapi/pygeoapi-config.yml"
export PYGEOAPI_OPENAPI="/c/1-Projects/pygeoapi/pygeoapi-config.yml"
export PYGEOAPI_HOME="/c/1-Projects/pygeoapi"
export PYTHONPATH="/c/1-Projects/pygeoapi:$PYTHONPATH"

# Load .env file variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "Loaded environment variables from .env file"
fi

# Run the FastHTML application with uvicorn
echo "Starting pygeoapi with FastHTML..."
echo "PYGEOAPI_CONFIG: $PYGEOAPI_CONFIG"
echo "PYGEOAPI_HOME: $PYGEOAPI_HOME"

uv run --project /c/3-Resources/envs/pygeo uvicorn pygeoapi.fasthtml_app:APP --host 0.0.0.0 --port 5000 --reload