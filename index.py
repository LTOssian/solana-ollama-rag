import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

MINIO_ENDPOINT = "http://127.0.0.1:9000"
BUCKET_NAME = "solana-documentation"
FILE_NAME = "Solana_ A new architecture for a high performance blockchain.pdf"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"


s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# Download the file
local_file_path = f"/tmp/{FILE_NAME}"  # Temporary storage for processing
s3_client.download_file(BUCKET_NAME, FILE_NAME, local_file_path)

# Read and extract text from the PDF file
reader = PdfReader(local_file_path)
pdf_content = ""
for page in reader.pages:
    pdf_content += page.extract_text()

# Check if text was successfully extracted
if not pdf_content.strip():
    raise ValueError("No text could be extracted from the PDF. It may be a scanned image PDF.")

# Split the text using LangChain's text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.create_documents([pdf_content])

# Display the split documents
for idx, doc in enumerate(docs):
    print(f"Document Chunk {idx + 1}:\n{doc.page_content}\n")
