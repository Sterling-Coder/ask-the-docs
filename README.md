# Ask the Docs

A Retrieval-Augmented Generation (RAG) application that allows users to chat with their PDF or TXT documents. Built with **Streamlit**, **LangChain**, and **FAISS**.

## Features

- **Document Ingestion**: 
  - Support for **multiple** PDF and TXT files.
  - **OCR Integration**: Automatically processes scanned PDFs using `Tesseract` and `pdf2image`.
- **RAG Architecture**: 
  - Uses `LangChain` for orchestration.
  - Generates embeddings via `OpenAIEmbeddings`.
  - Stores vectors in a local `FAISS` index for fast similarity search.
- **Modern UI**: 
  - Clean, tabbed interface (**Chat**, **Documents**, **History**).
  - Responsive layout with sidebar controls.
- **Smart Chat**: 
  - Powered by **OpenAI GPT-4o-mini** for accurate, context-aware answers.
  - Strict context adherence ("I cannot answer this based on the provided document").
- **History & Logging**: 
  - Persists question/answer history to a local CSV log.
  - Viewable directly within the application's "History" tab.
- **Deployment Ready**: 
  - Fully Dockerized for easy deployment on AWS, Azure, or local machines.

## Architecture

1. **Document Loading**: Extracts text using `PyPDFLoader` (standard) or `Tesseract OCR` (fallback for scanned docs).
2. **Splitting**: Chunks text using `RecursiveCharacterTextSplitter` (800 chars, 150 overlap).
3. **Internal Processing**:
   - **Embeddings**: `text-embedding-3-small` (OpenAI).
   - **Vector Store**: FAISS (Facebook AI Similarity Search).
4. **Retrieval & Generation**:
   - Retrieves top-k relevant chunks.
   - Generates answers using `gpt-4o-mini` with a strict system prompt.

## Prerequisites

- **Docker** (for containerized run)
- **OpenAI API Key**
- **Python 3.9+** (for local run)
- System Dependencies (only for local run): `tesseract`, `poppler`

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd ask-the-docs
```

### 2. Set up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-...
```

### 3. Run with Docker (Recommended)

This method handles all system dependencies (OCR, etc.) automatically.

1. **Build the image**:
   ```bash
   docker build -t ask-the-docs .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8501:8501 --env-file .env ask-the-docs
   ```

3. **Access the app**:
   Open `http://localhost:8501` in your browser.

### 4. Run Locally (without Docker)

If running locally, you must install system dependencies for OCR.

**Mac (Homebrew):**
```bash
brew install tesseract poppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**Setup Python Environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Run the App:**
```bash
python3 -m streamlit run app.py
```

## Deployment on AWS EC2 (Free Tier)

1. **Launch Instance**: Select `t2.micro` or `t3.micro` (Ubuntu AMI).
2. **Security Group**: Open port **8501** (Custom TCP) and **22** (SSH).
3. **Connect**: SSH into the instance.
4. **Install Docker**:
   ```bash
   sudo apt-get update && sudo apt-get install -y docker.io
   sudo usermod -aG docker $USER
   # Re-login to apply group changes
   ```
5. **Deploy**:
   - Clone repo and create `.env` file.
   - Run: `docker build -t ask-the-docs .`
   - Run: `docker run -d -p 8501:8501 --env-file .env --restart always ask-the-docs`
6. **Access**: Visit `http://<EC2-Public-IP>:8501`.

## Tech Stack

- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **Vector Database**: FAISS
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-small
- **OCR**: Tesseract & pdf2image
