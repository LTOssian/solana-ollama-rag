from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.s3 import s3_client
BUCKET_NAME = "solana-documentation"
FILE_NAME = "Solana_ A new architecture for a high performance blockchain.pdf"

# Download the file
local_file_path = f"/tmp/{FILE_NAME}"  # Temporary storage for processing
s3_client.download_file(BUCKET_NAME, FILE_NAME, local_file_path)

# Read and extract text from the PDF file
reader = PdfReader(local_file_path)
pdf_content = ""
for page in reader.pages:
    pdf_content += page.extract_text()

if not pdf_content.strip():
    raise ValueError("Ce PDF ne contient pas de texte. Le RAG nécessite un Corpus de Texte.")

# Split the text using LangChain's text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.create_documents([pdf_content])
print(f"Number of chunks created: {len(docs)}")

# Display the split documents
for idx, doc in enumerate(docs):
    print(f"Document Chunk {idx + 1}:\n{doc.page_content}\n")
