# Simple Qdrant debug script
import os
from qdrant_client import QdrantClient

print("🔍 Debugging Qdrant connection...")

# Get environment variables
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print(f"URL: {qdrant_url}")
print(f"API Key: {'***' + qdrant_api_key[-4:] if qdrant_api_key else 'None'}")

if not qdrant_url or not qdrant_api_key:
    print("❌ Missing QDRANT_URL or QDRANT_API_KEY")
    exit(1)

try:
    # Connect to Qdrant
    print("🔌 Connecting to Qdrant...")
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    # List all collections
    print("📋 Getting collections...")
    collections = client.get_collections()
    
    print(f"✅ Found {len(collections.collections)} collections:")
    for col in collections.collections:
        print(f"  - {col.name}")
        
    # Check specific collection
    target_collection = "kimia-assess"
    print(f"\n🔍 Looking for collection: '{target_collection}'")
    
    collection_names = [col.name for col in collections.collections]
    if target_collection in collection_names:
        print(f"✅ Collection '{target_collection}' found!")
        
        # Get collection info
        try:
            info = client.get_collection(target_collection)
            print(f"📊 Collection info: {info}")
        except Exception as e:
            print(f"❌ Error getting collection info: {e}")
    else:
        print(f"❌ Collection '{target_collection}' not found!")
        print("Available collections:")
        for name in collection_names:
            print(f"  - '{name}'")
            
        # Check for similar names
        similar = [name for name in collection_names if "kimia" in name.lower() or "assess" in name.lower()]
        if similar:
            print(f"\n💡 Similar collections found: {similar}")
            
except Exception as e:
    print(f"❌ Connection error: {e}") 