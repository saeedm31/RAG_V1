# PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows you to upload PDF documents and ask questions about their content using local AI.

## Features

- 📄 Upload and process PDF documents
- 🔍 Semantic search through document content
- 💬 Chat interface for asking questions
- 🤖 AI-powered responses using Ollama
- 💾 Persistent storage of documents and embeddings
- 🐳 Docker support for easy deployment

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Ollama installed and running (for AI responses)

### Running with Docker

1. **Clone or download this repository**
   ```bash
   cd RAG_V1
   ```

2. **Run the application**
   ```bash
   ./run_docker.sh
   ```
   
   Or manually:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Upload PDF files using the sidebar
   - Click "Process PDFs" to extract and index the content
   - Start asking questions about your documents!

### Directory Structure

```
RAG_V1/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── run_docker.sh         # Convenience script
├── pdf_inputs/           # Directory for PDF files (mounted as volume)
└── chroma_db/            # Database storage (mounted as volume)
```

## Manual Setup (without Docker)

### Prerequisites

- Python 3.8+
- Ollama installed and running

### Installation

1. **Create virtual environment**
   ```bash
   python3.8 -m venv rag_env
   source rag_env/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload PDFs**: Use the file uploader in the sidebar to add PDF documents
2. **Process Documents**: Click "Process PDFs" to extract text and create embeddings
3. **Ask Questions**: Use the chat interface to ask questions about your documents
4. **View Sources**: Expand the "View Sources" section to see which parts of the documents were used

## Configuration

### AI Model

The application uses Ollama for AI responses. Make sure you have Ollama installed and a model downloaded:

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Download a model (e.g., llama3.2)
ollama pull llama3.2
```

### Environment Variables

You can customize the application using environment variables:

- `STREAMLIT_SERVER_PORT`: Port for the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

## Troubleshooting

### Docker Issues

- **Port already in use**: Change the port in `docker-compose.yml` or stop other services using port 8501
- **Permission issues**: Make sure Docker has access to the project directory
- **Build failures**: Check that all files are present and Docker is running

### Ollama Issues

- **Model not found**: Download the required model with `ollama pull llama3.2`
- **Connection errors**: Make sure Ollama is running (`ollama serve`)

### PDF Processing Issues

- **Unsupported format**: Try converting PDFs to a different format
- **Large files**: The application works best with PDFs under 50MB

## Development

### Adding New Features

1. Modify `app.py` for UI changes
2. Update `requirements.txt` for new dependencies
3. Rebuild Docker image: `docker-compose build`

### Testing

```bash
# Run tests (if available)
python -m pytest

# Lint code
flake8 app.py
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 