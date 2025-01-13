#!/bin/bash

echo "Starting server..."

uvicorn travelapi.__main__:app --reload --port 8000
