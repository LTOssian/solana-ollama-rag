import argparse
import os

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from app.modules.options import Options
from app.s3 import FileStorage
from app.llm import BaseLLMApplication, llm
from app.rag import RAGApplication
from app.prompt import rag_prompt, base_prompt

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
        print("\nAucun fichier dans le Bucket. Fin du processus.")
        return

    print("\nFichiers disponibles dans le bucket S3 :\n")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    file_choice = input("Veuillez choisir un fichier (par numéro) : ")

    try:
        file_choice = int(file_choice)
        selected_file = files[file_choice - 1]

        print(f"\n{selected_file}")
    except (ValueError, IndexError):
        print("Choix invalide. Fin du processus.")
        return

    docs = FileStorage.process_pdf_file(BUCKET_NAME, selected_file)
    vector_store = create_vector_store(docs) 
    rag_application = RAGApplication.initialize_rag(vector_store, prompt, llm)
    
    clear_screen()
    print("\nBienvenue sur l'application de RAG! '/exit' pour quitter.")

    options_manager = Options()
    while True:

        question = input("Message solana-llama >>> ")
        options_manager.parse(question)

        if question.lower() == "/exit":
            print("Aurevoir!")
            break

        answer = rag_application.run(question)

        print("")
        print("Réponse: ", answer)
        
        if (options_manager.options["/help"]):
            print("""
                Commandes disponibles:
                /no-rag <message>     Désactiver le RAG sur cette question.
                /demo <message>       Lancer la question en mode demo.
                /help                 Montrer les commandes disponibles.
                /exit                 Quitter l'application.
                /set-temperature=<n>  Définir la temperture du LLM (ex: /set-temperature=0.7).
            """)

            options_manager.reset()
            continue

        print("-" * 50)

if __name__ == "__main__":
    main()
