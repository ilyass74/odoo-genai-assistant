# Odoo GenAI Assistant — ERP Queries and Document Search

A Flask assistant that combines live Odoo queries with retrieval from local business
documents. A LangChain tool-calling model selects tools for stock, sales, customer
invoices, document search and Word report generation.

**Stack:** Python, Flask, Odoo XML-RPC, LangChain, Groq, ChromaDB,
Hugging Face embeddings, PyPDF and python-docx.

## Architecture

The browser sends a question to Flask's `/api/chat` endpoint. The agent calls its
selected tools, then sends the returned data to the model to compose a French answer.
ERP tools query Odoo through XML-RPC. Document search retrieves the two nearest
chunks from the `business_documents` Chroma collection.

The configured Groq model is `openai/gpt-oss-120b`; availability depends on the
connected account. Embeddings use `BAAI/bge-small-en-v1.5`.

## Features

- Read stock quantities, sales orders and customer invoices.
- Search local PDF and TXT business documents.
- Generate Word reports for stock, sales or invoices.
- Use a browser chat interface or the command-line agent.

## Setup

Requirements: Python, access to an Odoo instance supporting XML-RPC, an Odoo user
with permission to read the relevant models, a Groq API key and internet access
for model downloads and API requests.

```shell
git clone https://github.com/ilyass74/odoo-genai-assistant.git
cd odoo-genai-assistant/odoo-projet
python -m pip install -r requirements.txt
python -m pip install flask python-docx pypdf langchain-groq langchain-core langchain-huggingface langchain-chroma langchain-text-splitters sentence-transformers
```

The supplied requirements file contains only part of the imported dependencies;
the second command supplies the additional packages. Versions are not locked.
Use an isolated virtual environment for installation.

Create `secrets.env` inside `odoo-projet/` with your own values:

```dotenv
ODOO_URL=https://your-instance.example.com
ODOO_DB=your_database
ODOO_USERNAME=your_login
ODOO_API_KEY=your_odoo_api_key
GROQ_API_KEY=your_groq_api_key
```

Keep this file local. All commands below must run from `odoo-projet/` because the
application resolves documents, credentials and the vector database relative to it.

## Index documents and start

Place PDF or TXT files in `documents/`, then run:

```shell
python indexation.py
python connexion.py
python app.py
```

Open [localhost:5000](http://localhost:5000). `connexion.py` is a connectivity check
that prints a small sample of ERP records. For the terminal assistant use
`python agent.py`.

Example questions: “Affiche le stock”, “Quelles sont les conditions de retour ?”,
or “Génère un rapport des ventes”. Answers depend on the records and documents
available in your own environment.

## API and outputs

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Chat interface |
| `/api/chat` | POST | JSON body with a `question` string |
| `/api/stock` | GET | Stock query, limited to 20 records |
| `/api/sales` | GET | Sales query, limited to 20 records |
| `/api/invoices` | GET | Customer invoices, limited to 20 records |
| `/rapports/<filename>` | GET | Download a generated report |

Reports are written to `rapports/stock.docx`, `ventes.docx` or `factures.docx`.
Generating the same report type replaces its earlier file.

## Repository structure

Application code lives in `odoo-projet/`:

- `connexion.py`: XML-RPC authentication and Odoo reads.
- `agent.py`: tools, model calls, document retrieval and reports.
- `indexation.py`: PDF/TXT ingestion, 800-character chunks with 100-character overlap.
- `app.py` and `templates/index.html`: Flask API and browser interface.
- `documents/`, `chroma_db/`, `rapports/`: source documents, index and reports.

`indexer.py` is an alternative TXT indexer using a different collection,
`documents_btel`; it does not populate the collection queried by the main agent.

## Current limitations

Stock filtering assumes the Odoo location is named `WH/Stock`; adapt it in
`connexion.py` if your warehouse differs. Reads are limited and not explicitly
ordered, so responses are not complete inventories or guaranteed latest records.
Repeated indexing adds chunks and can introduce duplicate search results.
The agent performs one tool-call round and a final response, without persistent
conversation memory or a guarantee that generated answers are correct.

The Flask entry point enables debug mode and the routes have no application-level
authentication. This is a local prototype, not a public deployment configuration.
The repository includes generated index/report artifacts; rebuild your index from
your intended documents. No automated test suite is included.

## Implementation references

[Agent](odoo-projet/agent.py) · [Odoo queries](odoo-projet/connexion.py) ·
[Indexing](odoo-projet/indexation.py) · [API](odoo-projet/app.py).
