import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

print("--- DIAGNOSTIC: Checking Knowledge Base ---")

# 1. Count Total Docs
response = supabase.table("documents").select("id", count="exact").execute()
print(f"✅ Total Documents found: {len(response.data)}")

# 2. Check Categories
tech_docs = supabase.table("documents").select("*").eq("doc_category", "technical").execute()
biz_docs = supabase.table("documents").select("*").eq("doc_category", "business").execute()

print(f"📊 Technical Docs: {len(tech_docs.data)}")
print(f"📊 Business Docs: {len(biz_docs.data)}")

if len(tech_docs.data) > 0:
    print("\n✅ Sample Technical Doc Content:")
    print(f"   -> {tech_docs.data[0]['content'][:100]}...")
else:
    print("\n❌ CRITICAL: No Technical documents found. Re-run ingestion!")