# Ask the Docs 📄🤖

**Ask the Docs** is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF or TXT documents and ask natural language questions about their content. The system uses a specialized pipeline to OCR, chunk, and embed document text, enabling an AI model to provide accurate answers based strictly on the provided material.

Deployed App: [http://51.21.161.9:8501](http://51.21.161.9:8501)

## 🚀 Features

*   **Multi-Format Support**: Upload `.pdf` (with automatic OCR for scanned docs) and `.txt` files.
*   **Intelligent Q&A**: Ask questions in plain English and get answers derived solely from your documents.
*   **Source Citation**: The AI is instructed to answer *only* from the context, minimizing hallucinations.
*   **Chat History**: Keeps a log of your questions and answers in a dedicated "History" tab.
*   **Multiple Files**: Support for uploading and indexing multiple files simultaneously.
*   **Modern UI**: Built with Streamlit, featuring a clean, tabbed interface for Chat, Document Management, and History.

## 🛠️ Methodology & Architecture

I built this project directly following the RAG (Retrieval-Augmented Generation) pattern:

1.  **Ingestion & OCR**:
    *   Files are uploaded via the UI.
    *   If a file is a PDF, I use `pdf2image` and `pytesseract` (OCR) to convert scanned pages into machine-readable text.
    *   Text files are read directly.
2.  **Chunking**:
    *   The extracted text is split into smaller, manageable chunks using LangChain's `RecursiveCharacterTextSplitter`. This ensures context is preserved while fitting within token limits.
3.  **Embedding & Storage**:
    *   Each text chunk is converted into a vector embedding using `OpenAIEmbeddings`.
    *   These vectors are stored in a **FAISS** (Facebook AI Similarity Search) index for extremely fast retrieval.
4.  **Retrieval & Generation**:
    *   When a user asks a question, it is also embedded into a vector.
    *   The system performs a similarity search in FAISS to find the most relevant text chunks.
    *   These chunks are passed as "Context" to the **GPT-4o-mini** model along with the user's question.
    *   The model generates an answer based *only* on that context.

## 💻 Tech Stack

*   **Frontend**: Streamlit
*   **Framework**: LangChain (for RAG pipeline)
*   **LLM**: OpenAI GPT-4o-mini
*   **Vector DB**: FAISS (CPU version)
*   **OCR Engine**: Tesseract & Poppler
*   **Deployment**: Docker container on AWS EC2 (Amazon Linux)

## 📦 Installation & Local Run

### Prerequisites
*   Docker installed on your machine.
*   An OpenAI API Key.

### Option 1: Run with Docker (Recommended)
This is the easiest way to run the app as it handles all system dependencies (like Tesseract) for you.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/ask-the-docs.git
    cd ask-the-docs
    ```

2.  **Create a `.env` file**:
    ```bash
    echo "OPENAI_API_KEY=your_api_key_here" > .env
    ```

3.  **Build and Run**:
    ```bash
    docker build -t ask-the-docs .
    docker run -p 8501:8501 --env-file .env ask-the-docs
    ```

4.  **Access the App**:
    Open [http://localhost:8501](http://localhost:8501) in your browser.

### Option 2: Run Manually (Python)
If you prefer not to use Docker, you must install Tesseract and Poppler manually.

1.  **Install System Dependencies**:
    *   **Mac**: `brew install tesseract poppler`
    *   **Linux**: `sudo apt-get install tesseract-ocr poppler-utils`
    *   **Windows**: Download installers for Tesseract and Poppler.

2.  **Install Python Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## ☁️ Deployment

The application is containerized with Docker and deployed on an AWS EC2 instance.

*   **Platform**: AWS EC2 (t3.micro, Free Tier eligible)
*   **OS**: Amazon Linux / Ubuntu
*   **Method**: 
    1.  Code transferred to server via SCP.
    2.  Docker image built on the server.
    3.  App runs as a detached Docker container exposed on port 8501.

## 📝 Notes on Model
I implemented **GPT-4o-mini** for this project because it offers an excellent balance of speed, cost-effectiveness, and reasoning capability for RAG tasks compared to GPT-3.5 or GPT-4.
