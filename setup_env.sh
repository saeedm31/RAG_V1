#!/bin/bash

echo "🚀 Setting up RAG App Environment..."

# Step 1: Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv rag_env

# Step 2: Activate virtual environment
echo "⚡ Activating virtual environment..."
source rag_env/bin/activate

# Step 3: Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Step 4: Install dependencies
echo "📚 Installing Python packages..."
pip install streamlit==1.28.0
pip install PyMuPDF==1.23.0
pip install chromadb==0.4.15
pip install sentence-transformers==2.2.2
pip install ollama==0.1.7
pip install torch>=2.0.0
pip install numpy>=1.24.0
pip install pandas>=2.0.0

# Step 5: Create directories
echo "📁 Creating directories..."
mkdir -p pdf_inputs
mkdir -p chroma_db

# Step 6: Install and setup Ollama (if not already installed)
echo "🧠 Setting up Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama already installed"
fi

# Step 7: Start Ollama service
echo "🔄 Starting Ollama service..."
ollama serve &
sleep 3

# Step 8: Pull AI model
echo "📥 Downloading AI model (this may take a few minutes)..."
ollama pull llama3.2:1b  # Using smaller 1B model for faster download

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 To run the app:"
echo "   source rag_env/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "🔍 To check if everything is working:"
echo "   ollama list"
echo ""
echo "📝 The environment is now ready in the 'rag_env' folder"