#!/bin/bash

echo "🚀 Setting up PDF RAG Chatbot..."

# Step 1: Install Ollama (if not already installed)
echo "📦 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Step 2: Pull a model (you can change this to any model you prefer)
echo "🧠 Downloading AI model..."
ollama pull llama3.2

# Step 3: Install Python dependencies
echo "🐍 Installing Python packages..."
pip install -r requirements.txt

# Step 4: Create necessary directories
echo "📁 Creating directories..."
mkdir -p pdf_inputs
mkdir -p chroma_db

echo "✅ Setup complete!"
echo ""
echo "🎯 To run the application:"
echo "   streamlit run app.py"
echo ""
echo "📋 What to do next:"
echo "   1. Make sure Ollama is running (it should start automatically)"
echo "   2. Run the app with: streamlit run app.py"
echo "   3. Upload PDF files using the sidebar"
echo "   4. Click 'Process PDFs' to index your documents"
echo "   5. Start chatting with your documents!"