from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaEmbeddings
from pypdf import PdfReader

from app.prompt import prompt
from app.s3 import s3_client
from app.llm import llm
from app.rag import RAGApplication

BUCKET_NAME = "solana-documentation"
FILE_NAME = "Solana_ A new architecture for a high performance blockchain.pdf"
API_KEY = "api_key"

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

# Create OpenAIEmbeddings for documents and store in vectorstores
embeddings = OllamaEmbeddings(model='llama3.2:1B')
doc_vectors = [embeddings.embed_query(doc.page_content) for doc in docs]

vector_store = FAISS.from_texts(
    texts=[doc.page_content for doc in docs],
    embedding=embeddings
)

retriever = vector_store.as_retriever(k=4)
rag_chain = prompt | llm | StrOutputParser()

rag_application = RAGApplication(retriever, rag_chain)

while True:
    question = input("Send your message >>> ")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    answer = rag_application.run(question)

    print("Question: ", question)
    print("Answer: ", answer)
    print("-" * 50)  # Separator for readability
