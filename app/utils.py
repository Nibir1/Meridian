import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# --- 1. Path Setup ---
# Add the project root to sys.path so we can import our custom components
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
sys.path.append(project_root)

# Import our Custom Components
from langflow_components.src.context_loader import ContextLoader
from langflow_components.src.intent_router import IntentRouter
from langflow_components.src.hybrid_retriever import HybridRetriever

# --- 2. Environment Setup ---
load_dotenv(os.path.join(project_root, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") # Must use Service Key for RLS bypass if needed
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def run_meridian_pipeline(user_query: str, user_id: str, history: list):
    """
    Orchestrates the 4-Layer Context Logic:
    1. Identity: Who are you?
    2. Intent: What do you want?
    3. Retrieval: What do we know?
    4. Generation: Here is the answer.
    """
    
    # --- LAYER 1: IDENTITY (ContextLoader) ---
    print(f"⚙️ [1/4] Loading Context for User: {user_id}")
    loader = ContextLoader()
    # Manually injecting inputs (simulating LangFlow runtime)
    loader.supabase_url = SUPABASE_URL
    loader.supabase_key = SUPABASE_KEY
    loader.user_id = user_id
    
    identity_data = loader.load_context()
    system_persona = identity_data.data["text"]

    # --- LAYER 2: INTENT (IntentRouter) ---
    print(f"⚙️ [2/4] Analyzing Intent for: '{user_query}'")
    router = IntentRouter()
    router.user_query = user_query
    
    intent_data = router.route_intent()
    intent_category = intent_data.data["text"]
    print(f"   -> Detected Intent: {intent_category.upper()}")

    # --- LAYER 3: KNOWLEDGE (HybridRetriever) ---
    print(f"⚙️ [3/4] Retrieving Documents (Filter: {intent_category})")
    retriever = HybridRetriever()
    retriever.supabase_url = SUPABASE_URL
    retriever.supabase_key = SUPABASE_KEY
    retriever.openai_api_key = OPENAI_API_KEY
    retriever.search_query = user_query
    retriever.filter_category = intent_category
    retriever.k = 3
    
    docs_data = retriever.search_vectors()
    retrieved_knowledge = docs_data.data["text"]

    # --- LAYER 4: GENERATION (LLM) ---
    print("⚙️ [4/4] Generating Response...")
    
    # Construct the final Prompt
    final_system_prompt = (
        f"{system_persona}\n\n"
        f"CONTEXTUAL KNOWLEDGE ({intent_category.upper()}):\n"
        f"{retrieved_knowledge}\n\n"
        f"INSTRUCTION: Answer the user based ONLY on the context above. "
        f"If the context is missing, say you don't know."
    )

    messages = [{"role": "system", "content": final_system_prompt}]
    
    # Append limited history (last 2 turns)
    for msg in history[-2:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    messages.append({"role": "user", "content": user_query})

    response = client.chat.completions.create(
        model="gpt-4o", # Or gpt-3.5-turbo
        messages=messages,
        temperature=0.3 # Keep it factual
    )

    return {
        "response": response.choices[0].message.content,
        "intent": intent_category,
        "context_used": system_persona
    }