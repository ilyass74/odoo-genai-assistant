# Fiche Technique – Assistant IA pour ERP (Odoo)

**Projet :** Assistant conversationnel (RAG + Agent) pour B Tel Bureautique

## Contexte

Projet personnel développé pour renforcer le CV, dans la direction GenAI / LLM. L'objectif était de construire un assistant capable d'interroger les données Odoo de B Tel Bureautique en langage naturel.

## Objectif

Permettre à un utilisateur non technique d'obtenir, via une interface de chat, des informations sur le stock, les ventes et les factures, ainsi que des réponses basées sur les documents métier de l'entreprise, et de générer des rapports Word téléchargeables.

## Stack technique

- **Langage :** Python
- **Orchestration agent :** LangChain
- **LLM :** ChatGroq (modèle `openai/gpt-oss-120b`)
- **ERP :** Odoo Community, en local via Docker (images `postgres:15` et `odoo:19.0`)
- **Connexion Odoo :** API XML-RPC
- **RAG / recherche documentaire :** ChromaDB (collection `business_documents`)
- **Embeddings :** HuggingFace – `BAAI/bge-small-en-v1.5`
- **Interface web :** Flask (`app.py`, `templates/index.html`, thème violet Odoo)
- **Génération de documents :** génération de fichiers Word (.docx) téléchargeables

## Architecture / Fonctionnement

1. L'utilisateur pose une question en langage naturel dans l'interface de chat web.
2. L'agent LangChain choisit l'outil adapté à la question :
   - `get_stock`, `get_sales`, `get_invoices` → interrogation directe d'Odoo via XML-RPC
   - `chercher_documents` → recherche RAG dans les documents métier indexés (PDF + conditions de vente, politique de retour, contrat fournisseur)
   - `generer_rapport` → génération d'un rapport Word (docx) téléchargeable (stock, ventes ou factures)
3. La réponse est renvoyée dans une boucle conversationnelle supportant plusieurs questions successives.

## Fonctionnalités principales

- Interrogation des données Odoo (stock, ventes, factures) en langage naturel
- Recherche documentaire (RAG) sur les documents métier de l'entreprise
- Génération de rapports Word téléchargeables, avec lien cliquable dans le chat
- Interface de chat web fonctionnelle dans le navigateur

## Statut / Résultats

- Agent testé avec succès de bout en bout : bascule correcte entre les outils Odoo et la recherche documentaire selon la question posée
- Interface web testée et fonctionnelle
- Génération de rapports testée de bout en bout
- Projet ajouté au CV ATS : entrée "AI Assistant for ERP (Odoo)" en tête de la section Projects, frameworks ajoutés (LangChain, Docker, ChromaDB, Groq API)
