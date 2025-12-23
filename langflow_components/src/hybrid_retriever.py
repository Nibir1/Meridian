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
        MessageTextInput(
            name="search_query",
            display_name="Search Query",
            info="The user's question."
        ),
        MessageTextInput(
            name="filter_category",
            display_name="Filter Category",
            info="The intent category (business/technical) from the Router."
        ),
        MessageTextInput(
            name="openai_api_key",
            display_name="OpenAI API Key",
            required=True
        ),
        MessageTextInput(
            name="supabase_url",
            display_name="Supabase URL",
            required=True
        ),
        MessageTextInput(
            name="supabase_key",
            display_name="Supabase Service Key",
            required=True
        ),
        IntInput(
            name="k",
            display_name="Top K Results",
            value=3
        )
    ]

    outputs = [
        Output(display_name="Retrieved Docs", name="retrieved_docs", method="search_vectors"),
    ]

    def search_vectors(self) -> Data:
        """
        Generates embedding for query -> Calls Supabase RPC 'match_documents' with filter.
        """
        # 1. Validation
        if not self.openai_api_key or not self.supabase_url:
            return Data(data={"text": "Configuration Error."})

        try:
            # 2. Clients
            openai_client = OpenAI(api_key=self.openai_api_key)
            supabase: Client = create_client(self.supabase_url, self.supabase_key)

            # 3. Embed the Query
            # We must use the same model as ingestion
            emb_response = openai_client.embeddings.create(
                input=self.search_query,
                model="text-embedding-3-small"
            )
            query_embedding = emb_response.data[0].embedding

            # 4. Execute RPC Call (The "Hybrid" part)
            # We call the function we wrote in the SQL Migration Phase 1
            # Note: We filter by the routed category!
            rpc_params = {
                "query_embedding": query_embedding,
                "match_threshold": 0.5, # Similarity threshold
                "match_count": self.k,
                "filter_category": self.filter_category
            }

            response = supabase.rpc("match_documents", rpc_params).execute()

            # 5. Format Results
            results_text = ""
            for doc in response.data:
                results_text += f"\n[Source: {doc['doc_category'].upper()}] {doc['content']}\n"

            if not results_text:
                results_text = "No relevant internal documents found for this category."

            return Data(data={"text": results_text})

        except Exception as e:
            return Data(data={"text": f"Retrieval Error: {str(e)}"})