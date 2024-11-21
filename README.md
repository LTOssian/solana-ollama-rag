# Modèles de Langage Augmentés par Récupération (RAG)

Ce projet met en œuvre la méthode **Retrieval-Augmented Generation (RAG)**, qui combine des modèles de langage (LLMs) légers avec la récupération de documents externes pour améliorer les performances sur des domaines spécifiques.

## Fonctionnalités Principales

- **Documentation Solana** préchargée (PDF) dans un stockage MinIO pour consultation.
- Utilisation de **FAISS** pour une recherche de similarité rapide sur les documents.
- Génération de réponses avec **llama 3.2:1b**, un modèle de langage léger et performant.

---

## Guide Rapide

### Pré-requis

1. Docker
2. Ollama avec le modèle `llama3.2:1b`
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

### 3. Accéder à MinIO

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

## Exemple d'utilisation

1. Lancer l’application :

   ```bash
   make install start
   ```

2. L’application vous présente la liste des fichiers PDF disponibles dans MinIO. Par exemple :

   ```cli
   Fichiers disponibles dans le bucket S3 :
   1. solana_docs_part1.pdf
   2. solana_docs_part2.pdf
   ```

3. Vous choisissez un fichier (par exemple le fichier n°1) pour l’indexer et le charger dans le **vector_store** :

   ```cli
   Veuillez choisir un fichier (par numéro) : 1
   ```

4. Une fois l'indexation terminée, vous pouvez poser des questions sur ce document. Par exemple :

   ```cli
   Send your message >>> Qu'est-ce que la blockchain Solana ?
   Answer: Solana est une blockchain performante conçue pour des applications à grande échelle...
   ```

---

## Technologies Utilisées

- **MinIO** : Stockage des documents dans un environnement compatible S3.  
- **FAISS** : Recherche rapide par similarité vectorielle pour une récupération efficace des documents pertinents.  
- **Ollama 3.2:1b** : Modèle de langage léger utilisé pour la génération des réponses.  
- **Python 3.12** : Environnement de développement et orchestration du projet.  
- **Docker** : Conteneurisation des services.
