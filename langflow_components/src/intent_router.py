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
        query = self.user_query.lower()
        
        # 1. Expanded Keywords
        tech_keywords = [
            "api", "python", "code", "websocket", "database", "schema", 
            "token", "auth", "key", "connect", "integrate", "endpoint", "sdk"
        ]
        biz_keywords = [
            "price", "pricing", "cost", "how much", "roi", "competitor", 
            "market", "revenue", "value", "sales", "license", "subscription",
            "business", "strategy"
        ]

        # 2. Logic (Prioritize Business if ambiguous keywords like 'value' appear)
        intent = "general" 
        
        if any(word in query for word in tech_keywords):
            intent = "technical"
        elif any(word in query for word in biz_keywords):
            intent = "business"

        # Debug Print to Console
        print(f"🔀 ROUTER DEBUG: Query='{query}' -> Intent='{intent}'")

        return Data(data={"text": intent})