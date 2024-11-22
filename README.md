# Modèles de Langage Augmentés par Récupération (RAG)

Ce projet met en œuvre la méthode **Retrieval-Augmented Generation (RAG)**, qui combine des modèles de langage (LLMs) légers avec la récupération de documents externes pour améliorer les performances sur des domaines spécifiques.

## Fonctionnalités Principales

- **Documentation Solana** préchargée (PDF) dans un stockage MinIO pour consultation.
- Utilisation de **FAISS** pour une recherche de similarité rapide sur les documents.
- Génération de réponses avec **llama 3.2:1b**, un modèle de langage léger et performant.

## Guide Rapide

### Pré-requis

1. Docker
2. Ollama avec le modèle `llama3.2:1b`

    ```bash
      ollama pull llama3.2:1b
      ollama run llama3.2:1b
    ```

3. Python 3.12

### 1. Cloner le dépôt

```bash
git clone https://github.com/your-username/solana-ollama-rag.git
cd solana-ollama-rag
```

### 2. Lancer l’application

Exécutez la commande suivante pour lancer les containers et démarrer le système :

```bash
make install start
```

Stoppez le container et nettoyez l'application avec :

```bash
make clean
```

### 3. Accéder à MinIO (S3)

- **URL** : [http://localhost:9001](http://localhost:9001)
- **Identifiants** :
  - Nom d’utilisateur : `minioadmin`
  - Mot de passe : `minioadmin`

Vous pouvez ajouter des documents supplémentaires directement sur MinIO pour enrichir la base de connaissances.

---

## Fonctionnement

1. **Stockage de documents** :  
   Les fichiers PDF de la documentation Solana (ou tout autre fichier que vous souhaitez ajouter) sont stockés dans MinIO. Au lancement de l’application, le système se connecte à MinIO pour lister les documents disponibles.

2. **Sélection du document** :  
   L’utilisateur choisit un fichier parmi ceux présents dans MinIO. Le fichier est ensuite chargé, extrait et indexé dans un **vector_store** pour permettre une recherche rapide et efficace des informations.

3. **Indexation** :  
   Les documents sont indexés à l’aide de **FAISS** pour rendre la récupération des passages pertinents plus rapide et plus précise. Cette indexation permet de retrouver les sections les plus pertinentes d’un document en fonction des requêtes posées.

4. **Requête** :  
   Une fois un document sélectionné et indexé, vous pouvez poser des questions sur ce dernier. Le système va :
   - Récupérer les documents pertinents depuis le **vector_store**.
   - Générer une réponse en combinant les informations extraites du document et le raisonnement du modèle de langage **Ollama LLM**.

5. **Génération de réponses** :  
   Le modèle **Ollama 3.2:1b** génère des réponses détaillées et précises en utilisant le contenu des documents récupérés et son propre raisonnement.

---

## Commandes disponibles

Dans l'application, vous pouvez utiliser plusieurs commandes pour modifier le comportement de l'application. Ces commandes sont saisies directement dans le terminal après la prompt `"Message solana-llama >>>"`.

### Commandes principales

- **`/no-rag <message>`**  
  Désactive la génération augmentée par la récupération (RAG) pour la question donnée. L'application répondra uniquement en utilisant le modèle de langage de base sans récupérer de documents.

- **`/demo <message>`**  
  Lance la question en mode démo. Le système génère deux réponses :

  1. Une réponse brute utilisant uniquement le modèle sans récupération (sans RAG).
  2. Une réponse augmentée par récupération (avec RAG).  
     Cette option est utile pour comparer la performance du modèle avec et sans les informations des documents récupérés.

- **`/help`**  
  Affiche une liste des commandes disponibles dans l'application, ainsi que des explications sur leur utilisation.

- **`/exit`**  
  Quitte l'application.

- **`/set-temperature=<n>`**  
  Définit la température du modèle de langage (ex : `/set-temperature=0.7`). La température contrôle la créativité de la réponse : une valeur plus basse rend le modèle plus déterministe, tandis qu'une valeur plus haute rend les réponses plus variées.

### Exemple d'utilisation

Voici quelques exemples de commandes que vous pouvez entrer dans l'application :

```plaintext
Message solana-llama >>> /no-rag Description technique du design du système Solana
Réponse: ...
Message solana-llama >>> /set-temperature=0.5
Message solana-llama >>> /demo Quel est la version de la documentation ?
Réponse sans RAG: La version de ma documentation en cours est la dernière mise à jour réalisée à la date limite de mes connaissances...
Réponse avec RAG: Ce document est la v0.8.13 de la documentation de l'architecture Solana
Message solana-llama >>> /exit
```

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Docker pour la conteneurisation
- Ollama avec le modèle `llama3.2:1b`

## Technologies Utilisées

- **MinIO** : Stockage des documents dans un environnement compatible S3.
- **FAISS** : Recherche rapide par similarité vectorielle pour une récupération efficace des documents pertinents.
- **Ollama 3.2:1b** : Modèle de langage léger utilisé pour la génération des réponses.
- **Python 3.12** : Environnement de développement et orchestration du projet.
- **Docker** : Conteneurisation des services.

---

## Sources

- [Guide RAG](https://www.datacamp.com/tutorial/llama-3-1-rag)
- [Documentation LLMs, support de connaissances](https://arxiv.org/pdf/2307.06435#page=36&zoom=100,56,209)
- [Solana's architecture documentation used](https://solana.com/solana-whitepaper.pdf)
