from langflow.custom import CustomComponent
from langflow.io import MessageTextInput, IntInput, Output
from langflow.schema import Data
from supabase import create_client, Client
from openai import OpenAI
import os

class HybridRetriever(CustomComponent):
    display_name = "Meridian Hybrid Retriever"
    description = "Vector Search with Metadata Filtering based on Intent."
    icon = "Database"

    inputs = [
        MessageTextInput(name="search_query", display_name="Search Query"),
        MessageTextInput(name="filter_category", display_name="Filter Category"),
        MessageTextInput(name="openai_api_key", display_name="OpenAI API Key", required=True),
        MessageTextInput(name="supabase_url", display_name="Supabase URL", required=True),
        MessageTextInput(name="supabase_key", display_name="Supabase Service Key", required=True),
        IntInput(name="k", display_name="Top K Results", value=3)
    ]

    outputs = [
        Output(display_name="Retrieved Docs", name="retrieved_docs", method="search_vectors"),
    ]

    def search_vectors(self) -> Data:
        if not self.openai_api_key or not self.supabase_url:
            return Data(data={"text": "Configuration Error."})

        try:
            openai_client = OpenAI(api_key=self.openai_api_key)
            supabase: Client = create_client(self.supabase_url, self.supabase_key)

            # Generate Embedding
            emb_response = openai_client.embeddings.create(
                input=self.search_query,
                model="text-embedding-3-small"
            )
            query_embedding = emb_response.data[0].embedding

            # Execute RPC with Relaxed Threshold
            rpc_params = {
                "query_embedding": query_embedding,
                "match_threshold": 0.01,  # <--- CRITICAL FIX: Accepts almost any match
                "match_count": self.k,
                "filter_category": self.filter_category
            }

            print(f"🔍 RETRIEVER DEBUG: Searching for '{self.filter_category}' docs...")
            response = supabase.rpc("match_documents", rpc_params).execute()
            
            # Debug: Did we find anything?
            print(f"✅ RETRIEVER FOUND: {len(response.data)} documents.")

            results_text = ""
            for doc in response.data:
                results_text += f"\n[Source: {doc['doc_category'].upper()}] {doc['content']}\n"

            if not results_text:
                results_text = "No relevant internal documents found for this category."

            return Data(data={"text": results_text})

        except Exception as e:
            print(f"❌ RETRIEVER ERROR: {e}")
            return Data(data={"text": f"Retrieval Error: {str(e)}"})