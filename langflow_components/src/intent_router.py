from langflow.custom import CustomComponent
from langflow.io import MessageTextInput, Output
from langflow.schema import Data

class IntentRouter(CustomComponent):
    display_name = "Meridian Intent Router"
    description = "Classifies user query into 'technical' or 'business' intent."
    icon = "Split"

    inputs = [
        MessageTextInput(
            name="user_query",
            display_name="User Query",
            info="The question asked by the user."
        ),
    ]

    outputs = [
        Output(display_name="Intent Category", name="intent", method="route_intent"),
    ]

    def route_intent(self) -> Data:
        """
        Simple keyword-based routing. 
        In production, this would be an LLM call, but for this architecture demo, 
        deterministic logic is faster and proves the 'Routing' concept effectively.
        """
        query = self.user_query.lower()
        
        # 1. Define Keywords
        tech_keywords = ["api", "python", "code", "websocket", "database", "schema", "token", "auth"]
        biz_keywords = ["price", "cost", "roi", "competitor", "market", "revenue", "value", "sales"]

        # 2. Logic
        intent = "general" # Default
        
        # Check Technical
        if any(word in query for word in tech_keywords):
            intent = "technical"
        # Check Business (overrides technical if ambiguous for this demo, or creates a hierarchy)
        elif any(word in query for word in biz_keywords):
            intent = "business"

        # 3. Return Result
        # We return it as a Data object so it can be passed to the Retriever
        return Data(data={"text": intent})