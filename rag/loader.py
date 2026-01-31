import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from pdf2image import convert_from_path
import pytesseract

def load_and_split_document(uploaded_file):
    """
    Loads a PDF or TXT file and splits it into chunks.
    """
    if uploaded_file is None:
        return []

    # 1. Save uploaded file to a temporary file
    temp_file_path = _save_temp_file(uploaded_file)

    try:
        # 2. Extract text (PDF with OCR fallback or TXT)
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension == ".pdf":
            docs = _load_pdf(temp_file_path, uploaded_file.name)
        elif file_extension == ".txt":
            docs = _load_txt(temp_file_path, uploaded_file.name)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
            
        # 3. Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            add_start_index=True
        )
        chunks = text_splitter.split_documents(docs)


        # Remove empty chunks
        chunks = [
            chunk for chunk in chunks
            if chunk.page_content and chunk.page_content.strip()
        ]

        # Ensure source metadata is consistent
        for chunk in chunks:
            chunk.metadata["source"] = uploaded_file.name

        return chunks
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def _save_temp_file(uploaded_file):
    """Saves the uploaded file to a temporary location."""
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        return temp_file.name

def _load_pdf(file_path, original_name):
    """Loads a PDF file, attempting standard extraction then falling back to OCR."""
    # 1. Try standard extraction first
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    total_text_length = sum(len(doc.page_content.strip()) for doc in docs)
    print(f"DEBUG: Standard extraction got {total_text_length} chars.")

    # 2. Check if text is insufficient (Scanned PDF or Image)
    # Heuristic: Less than 50 chars of text usually means it's an image-only PDF
    if total_text_length < 50:
        print("DEBUG: Text too sparse. Falling back to OCR (Slower but robust)...")
        docs = _ocr_pdf(file_path)
    else:
         print("DEBUG: Standard extraction successful.")
    
    return docs

def _load_txt(file_path, original_name):
    """Loads a text file."""
    loader = TextLoader(file_path, encoding="utf-8")
    print(f"DEBUG: Loaded text file {original_name}")
    return loader.load()

def _ocr_pdf(file_path):
    """
    Performs OCR on a PDF file using pdf2image and pytesseract.
    Returns a list of Document objects.
    """
    # Convert PDF to images
    images = convert_from_path(file_path)
    docs = []
    
    for i, image in enumerate(images):
        # Extract text from image
        text = pytesseract.image_to_string(image)
        
        # Create Document object (one per page)
        doc = Document(
            page_content=text,
            metadata={
                "source": os.path.basename(file_path),
                "page": i
            }
        )
        docs.append(doc)
        
    return docs
