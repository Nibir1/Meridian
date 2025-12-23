from langflow.custom import CustomComponent
from langflow.io import MessageTextInput, Output
from langflow.schema import Data
from supabase import create_client, Client
import os

class ContextLoader(CustomComponent):
    display_name = "Meridian Context Loader"
    description = "Fetches User Profile from Supabase to inject persona-based context."
    icon = "User"

    # Inputs defined for the LangFlow UI
    inputs = [
        MessageTextInput(
            name="user_id",
            display_name="User UUID",
            value="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", # Default to Sarah (CTO) for testing
            info="The UUID of the user from the Supabase profiles table."
        ),
        MessageTextInput(
            name="supabase_url",
            display_name="Supabase URL",
            required=True,
        ),
        MessageTextInput(
            name="supabase_key",
            display_name="Supabase Service Key",
            required=True,
        ),
    ]

    # Outputs: We return 'Data' which contains the system instructions
    outputs = [
        Output(display_name="System Context", name="system_context", method="load_context"),
    ]

    def load_context(self) -> Data:
        """
        Connects to Supabase, fetches the user profile, and constructs a system prompt.
        """
        # 1. Setup Client
        url = self.supabase_url
        key = self.supabase_key
        uid = self.user_id

        if not url or not key:
            return Data(data={"text": "System: Configuration Error. Missing API Keys."})

        try:
            supabase: Client = create_client(url, key)

            # 2. Query Profile
            response = supabase.table("profiles").select("*").eq("id", uid).execute()
            
            if not response.data:
                return Data(data={"text": "System: User not found. Treat as generic user."})

            profile = response.data[0]
            
            # 3. Construct Context String
            # This is the "Magic" -> injecting the persona into the prompt
            context_str = (
                f"SYSTEM INSTRUCTION: You are speaking to {profile['full_name']}. "
                f"Role: {profile['role']}. Industry: {profile['industry']}. "
                f"Bio: {profile['bio']}. "
                f"Adjust your tone and complexity accordingly."
            )

            # 4. Return as LangFlow Data Object
            return Data(data={"text": context_str})

        except Exception as e:
            return Data(data={"text": f"System Error: Failed to load context. {str(e)}"})