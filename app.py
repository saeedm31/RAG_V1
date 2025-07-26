import streamlit as st
import os
from sentence_transformers import SentenceTransformer
import shutil
from typing import List, Dict
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Try to import ollama, but make it optional
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Try different PDF libraries
try:
    import PyMuPDF as fitz
    PDF_LIBRARY = "PyMuPDF"
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_LIBRARY = "PyMuPDF"
    except ImportError:
        try:
            import pdfplumber
            PDF_LIBRARY = "pdfplumber"
        except ImportError:
            try:
                import pypdf
                PDF_LIBRARY = "pypdf"
            except ImportError:
                PDF_LIBRARY = None

class RAGApp:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.pdf_directory = "./pdf_inputs"
        self.chunk_size = 500
        self.chunk_overlap = 50
        
        # Create PDF directory if it doesn't exist
        os.makedirs(self.pdf_directory, exist_ok=True)
        
        # In-memory storage for documents and embeddings
        self.documents = []
        self.embeddings = []
        self.metadata = []
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file using available library"""
        if PDF_LIBRARY == "PyMuPDF":
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        elif PDF_LIBRARY == "pdfplumber":
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        elif PDF_LIBRARY == "pypdf":
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
            return text
        else:
            raise ImportError("No PDF library available. Please install PyMuPDF, pdfplumber, or pypdf.")
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks for better retrieval"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def process_pdfs(self) -> int:
        """Process all PDFs in the input directory"""
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        
        if not pdf_files:
            return 0
        
        # Clear existing data
        self.documents = []
        self.embeddings = []
        self.metadata = []
        
        total_chunks = 0
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_directory, pdf_file)
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            # Create chunks
            chunks = self.chunk_text(text)
            
            # Create embeddings and store
            for i, chunk in enumerate(chunks):
                embedding = self.embedding_model.encode(chunk)
                
                self.documents.append(chunk)
                self.embeddings.append(embedding)
                self.metadata.append({"source": pdf_file, "chunk_id": i})
                total_chunks += 1
        
        return total_chunks
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant document chunks for the query"""
        if not self.documents:
            return []
        
        query_embedding = self.embedding_model.encode(query)
        
        # Calculate similarities
        similarities = []
        for embedding in self.embeddings:
            similarity = cosine_similarity([query_embedding], [embedding])[0][0]
            similarities.append(similarity)
        
        # Get top n_results
        top_indices = np.argsort(similarities)[-n_results:][::-1]
        
        return [self.documents[i] for i in top_indices]
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate response using Ollama with retrieved context"""
        if not OLLAMA_AVAILABLE:
            return "Ollama is not available. Please install it with: pip install ollama"
        
        context_text = "\n\n".join(context)
        
        prompt = f"""Based on the following context from the documents, please answer the question. If the answer is not in the context, say so.

Context:
{context_text}

Question: {query}

Answer:"""
        
        try:
            response = ollama.chat(
                model='llama3.2',  # You can change this to any model you have
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}. Make sure Ollama is running and you have the llama3.2 model installed."

def main():
    st.set_page_config(page_title="PDF RAG Chatbot", layout="wide")
    
    st.title("📚 PDF RAG Chatbot")
    st.markdown("Upload PDFs and chat with your documents using local AI!")
    
    # Show which PDF library is being used
    if PDF_LIBRARY:
        st.info(f"Using PDF library: {PDF_LIBRARY}")
    else:
        st.error("No PDF library available. Please install PyMuPDF, pdfplumber, or pypdf.")
        st.stop()
    
    # Show ollama status
    if OLLAMA_AVAILABLE:
        st.success("✅ Ollama is available")
    else:
        st.warning("⚠️ Ollama is not available. AI responses will be limited.")
    
    # Initialize the RAG app
    if 'rag_app' not in st.session_state:
        st.session_state.rag_app = RAGApp()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for PDF management
    with st.sidebar:
        st.header("📁 PDF Management")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        # Save uploaded files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(st.session_state.rag_app.pdf_directory, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Show current PDFs
        pdf_files = [f for f in os.listdir(st.session_state.rag_app.pdf_directory) if f.endswith('.pdf')]
        if pdf_files:
            st.subheader("Current PDFs:")
            for pdf in pdf_files:
                st.text(f"• {pdf}")
        
        # Process PDFs button
        if st.button("🔄 Process PDFs", type="primary"):
            with st.spinner("Processing PDFs..."):
                chunk_count = st.session_state.rag_app.process_pdfs()
                if chunk_count > 0:
                    st.success(f"Processed {len(pdf_files)} PDFs into {chunk_count} chunks!")
                else:
                    st.warning("No PDFs found to process")
        
        # Clear all data
        if st.button("🗑️ Clear All Data"):
            # Remove PDF files
            shutil.rmtree(st.session_state.rag_app.pdf_directory)
            os.makedirs(st.session_state.rag_app.pdf_directory)
            
            # Clear in-memory data
            st.session_state.rag_app.documents = []
            st.session_state.rag_app.embeddings = []
            st.session_state.rag_app.metadata = []
            
            # Clear chat history
            st.session_state.chat_history = []
            
            st.success("All data cleared!")
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with your Documents")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    prompt = st.chat_input("Ask a question about your documents...")
    if prompt:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Retrieve relevant chunks
                relevant_chunks = st.session_state.rag_app.retrieve_relevant_chunks(prompt)
                
                if not relevant_chunks:
                    response = "I couldn't find any relevant information in the uploaded documents. Please make sure you have uploaded and processed PDF files."
                else:
                    # Generate response
                    response = st.session_state.rag_app.generate_response(prompt, relevant_chunks)
                
                st.write(response)
                
                # Show sources (optional)
                if relevant_chunks:
                    with st.expander("📖 View Sources"):
                        for i, chunk in enumerate(relevant_chunks, 1):
                            st.text(f"Source {i}:")
                            st.text(chunk[:200] + "..." if len(chunk) > 200 else chunk)
                            st.divider()
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()