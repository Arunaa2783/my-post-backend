#!/bin/bash

echo "🧹 Stopping and removing existing containers..."
docker rm -f post-db cpp-backend 2>/dev/null

echo "🚀 Starting fresh containers..."
docker-compose up --build
