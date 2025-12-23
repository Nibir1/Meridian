# Meridian -- The Intelligent Market Consultant

> **Multi-Layer Context Orchestration for Global Business Logic.**

[![Meridian Demo](https://img.youtube.com/vi/w8wlRdG_ufo/maxresdefault.jpg)](https://youtu.be/w8wlRdG_ufo)

> 📺 **[Watch the full end-to-end demo](https://youtu.be/w8wlRdG_ufo)** featuring core functionalities.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Supabase](https://img.shields.io/badge/Supabase-PGVector-green?style=for-the-badge&logo=supabase)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT4-orange?style=for-the-badge&logo=openai)

------------------------------------------------------------------------

## The Pitch

**Meridian** is not just a chatbot; it is an **AI Orchestration
Engine**.

Standard RAG (Retrieval Augmented Generation) systems treat every user
the same. Meridian introduces **Stateful Intelligence** by orchestrating
four distinct layers of context before generating an answer. It adapts
its persona, retrieval strategy, and tone based on **who** is asking and
**what** they need.

------------------------------------------------------------------------

## The 4-Layer "Brain" Architecture

1.  **Identity Layer (ContextLoader)**\
    Fetches the user's role (e.g., CTO vs. CEO) from Supabase to inject
    persona-specific instructions.

2.  **Intent Layer (IntentRouter)**\
    Analyzes the prompt to classify intent (Technical vs. Business) and
    routes the query.

3.  **Knowledge Layer (HybridRetriever)**\
    Performs a Vector Search on Supabase with strict metadata filtering
    based on the routed intent.

4.  **Generation Layer (LLM)**\
    Synthesizes the retrieved data with the user context to generate a
    highly tailored response.

------------------------------------------------------------------------

## Technical Architecture

The system is built using a modular **LangFlow-compatible** component
architecture.

``` text
meridian/
├── app/
│   ├── main.py
│   └── utils.py
├── ingestion/
│   └── ingest_docs.py
├── langflow_components/
│   └── src/
│       ├── context_loader.py
│       ├── intent_router.py
│       └── hybrid_retriever.py
├── supabase/
│   ├── migrations/
│   └── seed.sql
└── requirements.txt
```

------------------------------------------------------------------------

## Key Features

### 1. Dynamic Persona Injection

Meridian adapts its expertise based on user role.

-   **CTO** → Senior Architect persona (code snippets, APIs, security)
-   **CEO** → Strategy Consultant persona (ROI, pricing, growth)

### 2. Intelligent Routing

Ensures relevant documents are retrieved.

-   *"How do I authenticate?"* → Technical RAG\
-   *"What is the pricing?"* → Business RAG

### 3. Conditional RAG

Uses Supabase pgvector metadata filtering to reduce noise and improve
accuracy.

------------------------------------------------------------------------

## Installation & Setup

### Prerequisites

-   Python 3.10+
-   Supabase Project (PostgreSQL)
-   OpenAI API Key

### 1. Clone & Install

``` bash
git clone https://github.com/your-username/meridian.git
cd meridian
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:

``` ini
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_SERVICE_KEY="your-service-role-secret"
OPENAI_API_KEY="sk-..."
```

### 3. Database Setup

Run SQL scripts in Supabase: -
`supabase/migrations/20250101_init_schema.sql` - `supabase/seed.sql`

### 4. Ingest Knowledge Base

``` bash
python ingestion/ingest_docs.py
```

------------------------------------------------------------------------

## Running the Application

``` bash
streamlit run app/main.py
```

------------------------------------------------------------------------

## Demo Flow

1.  Select **Sarah (CTO)** → Ask: *"How do I connect to the API?"*
2.  Select **Marcus (CEO)** → Ask: *"What is the pricing?"*

------------------------------------------------------------------------
