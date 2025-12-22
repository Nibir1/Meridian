import os
import sys
from typing import List
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# --- 1. Robust Environment Loading ---
# Get the absolute path of the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct path to .env (one level up)
env_path = os.path.join(current_dir, "..", ".env")

print(f"📂 Loading .env from: {env_path}")

if not os.path.exists(env_path):
    print("❌ ERROR: .env file not found at expected path.")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") # Ensure this is the SERVICE_ROLE key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Debugging (Safety Check) ---
if not SUPABASE_KEY:
    print("❌ ERROR: SUPABASE_SERVICE_KEY is None. Check your .env file content.")
    sys.exit(1)
else:
    # Print first 5 chars to verify it loaded correctly (don't print full key)
    print(f"✅ Loaded Supabase Key: {SUPABASE_KEY[:5]}...")

if not SUPABASE_URL:
    print("❌ ERROR: SUPABASE_URL is missing.")
    sys.exit(1)

# --- 2. Initialize Clients ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"❌ Client Initialization Error: {e}")
    sys.exit(1)

# --- 3. Define Dummy Knowledge Base ---
raw_documents = [
    # --- TECHNICAL DOCUMENTS (For CTO Persona) ---
    {
        "content": "Meridian API Authentication: All requests must include the 'Authorization: Bearer <token>' header. Tokens expire after 1 hour.",
        "source": "api_docs_v2.pdf",
        "category": "technical"
    },
    {
        "content": "To implement the Websocket stream, connect to wss://api.meridian.ai/stream. Ensure TLS 1.3 is enabled for security compliance.",
        "source": "api_docs_v2.pdf",
        "category": "technical"
    },
    {
        "content": "Database Schema Standard: Meridian uses PostgreSQL with pgvector. Sharding is recommended for datasets exceeding 1TB.",
        "source": "architecture_guide.pdf",
        "category": "technical"
    },
    # --- BUSINESS DOCUMENTS (For CEO Persona) ---
    {
        "content": "Meridian Enterprise Pricing: The licensing model is $50,000/year per node. This includes 24/7 support and dedicated account management.",
        "source": "pricing_2025.pdf",
        "category": "business"
    },
    {
        "content": "Market ROI Analysis: Implementing Meridian reduces operational latency by 40%, resulting in a projected 15% increase in Q3 revenue.",
        "source": "market_report_q3.pdf",
        "category": "business"
    },
    {
        "content": "Competitive Landscape: Unlike Competitor X, Meridian offers on-premise deployment, which is a key selling point for highly regulated industries.",
        "source": "competitor_analysis.pdf",
        "category": "business"
    }
]

def generate_embedding(text: str) -> List[float]:
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return []

def ingest_data():
    print(f"🚀 Starting Ingestion for {len(raw_documents)} documents...")

    for doc in raw_documents:
        content = doc["content"]
        category = doc["category"]
        metadata = {"source": doc["source"]}

        print(f"🔹 Processing [{category}]: {content[:30]}...")

        # A. Generate Vector
        embedding = generate_embedding(content)
        
        if not embedding:
            continue

        # B. Prepare Payload
        data_payload = {
            "content": content,
            "metadata": metadata,
            "doc_category": category,
            "embedding": embedding
        }

        # C. Insert into Database
        try:
            response = supabase.table("documents").insert(data_payload).execute()
        except Exception as e:
            print(f"❌ Insert Failed: {e}")

    print("✅ Ingestion Complete. Knowledge Base is ready.")

if __name__ == "__main__":
    ingest_data()