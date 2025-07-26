#!/bin/bash

echo "🚀 Starting RAG App..."

# Check if virtual environment exists
if [ ! -d "rag_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup_env.sh first"
    exit 1
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source rag_env/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Check if we have models
if ! ollama list | grep -q "llama3.2"; then
    echo "📥 No models found. Installing llama3.2:1b..."
    ollama pull llama3.2:1b
fi

echo "🌐 Starting Streamlit app..."
streamlit run app.py

echo "✅ App stopped"