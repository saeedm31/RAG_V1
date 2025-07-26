#!/bin/bash

# RAG Application Docker Runner
echo "🚀 Starting RAG Application with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create necessary directories if they don't exist
mkdir -p pdf_inputs chroma_db

# Build and run the container
echo "📦 Building Docker image..."
docker-compose up --build

echo "✅ Application is running at http://localhost:8501"
echo "📁 PDF files can be placed in the ./pdf_inputs directory"
echo "💾 Data will be persisted in the ./chroma_db directory" 