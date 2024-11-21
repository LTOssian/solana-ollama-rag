# Retrieval-Augmented Language Models (RAG)

This project implements **Retrieval-Augmented Generation (RAG)** using small Language Models (LLMs) that leverage external knowledge to enhance performance on specific topics. By using a retrieval system, small models can provide answers comparable to larger models, even with a limited memory.

## Overview

This project implements **Retrieval-Augmented Generation (RAG)**, a method that enhances small Language Models (LLMs) by allowing them to retrieve external, up-to-date information. The LLMs can provide more accurate answers on specific topics by leveraging this external knowledge.

The project is set up with a **MinIO object storage service**, which is configured with a base volume that holds the **Solana documentation PDF**. This PDF serves as the knowledge base for the RAG system. The Solana documentation is indexed and processed, enabling the language model to retrieve relevant sections and answer queries with up-to-date, domain-specific information.

By combining **FAISS** for efficient similarity search and **Ollama 3.2:1b** for language generation, this setup allows small models to perform as effectively as larger models on questions related to Solana, without needing vast computational resources.

## Technologies

- **MinIO (S3-compatible)**
- **Python 3.12**
- **Ollama 3.2:1b**: Lightweight, efficient LLM used for natural language understanding and generation.

## Project Stack

- **MinIO**: Object storage for serving and storing document data.
- **Ollama LLM**: Language model used for processing and generating text based on retrieved information.
- **FAISS**: Vector database for efficient similarity search on documents.
- **Python 3.12**: Environment to tie all components together.

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/solana-rag.git
cd solana-rag
```

### 2. Docker Compose - Start MinIO Service

MinIO is used to handle the object storage for document retrieval. It is exposed on ports `9000` for the S3 interface and `9001` for the web console.

Run the following command to start the MinIO service:

```bash
docker-compose up -d
```

#### MinIO Configuration

- **Access Key**: `minioadmin`
- **Secret Key**: `minioadmin`
- **Web Console**: [http://localhost:9001](http://localhost:9001)

### 3. Install Dependencies

Make sure you have Python 3.12 installed. You can use a virtual environment for isolation.

```bash
python3 -m venv env
source env/bin/activate  # For Linux/MacOS
env\Scripts\activate  # For Windows
pip install -r requirements.txt
```

### 4. Start the Application

To run the application and start the index creation and retrieval process, execute:

```bash
python3 index.py
```

This will load and index documents from MinIO, allowing the model to retrieve relevant data for improved response generation, and start the CLI.

## Usage

Once the application is running, you can interact with the model by calling the retrieval augmented language model via the provided interface or through your preferred means (like a REST API, if set up).

The integration with **FAISS** will handle the search of the most relevant documents to provide the best possible response based on the question asked.

The model will retrieve relevant documents from the MinIO storage and generate an answer with the most accurate and up-to-date information.

## How It Works

1. **Document Storage in MinIO**:

   - Store documents in MinIO that you want to use as the knowledge base.
   - These documents are then indexed by the FAISS vector store for fast similarity search.

2. **Querying**:

   - When a query (question) is made, the system retrieves relevant documents from the indexed FAISS vector store.
   - The **Ollama LLM** processes the query and generates a response by combining the retrieved documents with its own language generation capabilities.

3. **Retrieval-Augmented Generation**:
   - This allows even smaller models to perform better by augmenting them with external knowledge through **retrieval** before **generation**.

## Conclusion

This project demonstrates how small LLMs can be significantly augmented using **retrieval-based** methods, giving them the capability to answer domain-specific questions with high accuracy without requiring massive model sizes. By using **MinIO** and **FAISS**, this approach ensures scalable and efficient knowledge retrieval.
