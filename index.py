import argparse
import os

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from app.prompt import prompt
from app.s3 import FileStorage
from app.llm import llm
from app.rag import RAGApplication

BUCKET_NAME = "solana-documentation"

def create_vector_store(docs):
    embeddings = OllamaEmbeddings(model='llama3.2:1B')
    # doc_vectors = [embeddings.embed_query(doc.page_content) for doc in docs]

    vector_store = FAISS.from_documents(
        docs,
        embedding=embeddings
    )

    return vector_store


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:  
        os.system('clear')

def main():
    clear_screen()
    parser = argparse.ArgumentParser(description="Retrieval-Augmented Generation (RAG) for Solana Documentation.")
    BUCKET_NAME = "solana-documentation"

    files = FileStorage.list_files_in_bucket(BUCKET_NAME)
    if not files:
        print("Aucun fichier dans le Bucket. Fin du processus.")
        return

    print("Fichiers disponibles dans le bucket S3 :")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    file_choice = input("Veuillez choisir un fichier (par numéro) : ")

    try:
        file_choice = int(file_choice)
        selected_file = files[file_choice - 1]
        print(selected_file)
    except (ValueError, IndexError):
        print("Choix invalide. Fin du processus.")
        return

    docs = FileStorage.process_pdf_file(BUCKET_NAME, selected_file)
    vector_store = create_vector_store(docs) 
    rag_application = RAGApplication.initialize_rag(vector_store, prompt, llm)
    
    clear_screen()
    print("Bienvenue sur l'application de RAG! 'exit' pour quitter.")

    while True:
        question = input("Message solana-llama >>> ")
        if question.lower() == "exit":
            print("Aurevoir!")
            break

        answer = rag_application.run(question)

        print("")
        print("Réponse: ", answer)
        print("-" * 50)

if __name__ == "__main__":
    main()
