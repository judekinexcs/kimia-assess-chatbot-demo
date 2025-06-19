# Script to check and create Qdrant collection
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from langchain_openai import OpenAIEmbeddings

# Get environment variables
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
collection_name = "kimia-assess"

print(f"🔍 Checking Qdrant connection...")
print(f"URL: {qdrant_url}")
print(f"Collection: {collection_name}")

if not qdrant_url or not qdrant_api_key:
    print("❌ QDRANT_URL or QDRANT_API_KEY not set!")
    exit(1)

try:
    # Connect to Qdrant
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    # Check if collection exists
    collections = client.get_collections()
    collection_names = [col.name for col in collections.collections]
    
    print(f"📋 Existing collections: {collection_names}")
    
    if collection_name in collection_names:
        print(f"✅ Collection '{collection_name}' already exists!")
        
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"📊 Collection info: {collection_info}")
        
    else:
        print(f"❌ Collection '{collection_name}' does not exist!")
        print("🔧 Creating collection...")
        
        # Create embeddings instance
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vector_size = 1536  # OpenAI embeddings dimension
        
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=qdrant_models.Distance.COSINE
            )
        )
        
        print(f"✅ Collection '{collection_name}' created successfully!")
        
        # Add some sample data
        print("📝 Adding sample data...")
        sample_texts = [
            "KIMIA Assess is a comprehensive assessment platform for medical imaging.",
            "The platform provides AI-powered analysis of medical images.",
            "KIMIA Assess supports various medical imaging modalities.",
            "Users can upload and analyze medical images through the platform."
        ]
        
        # Create embeddings for sample texts
        sample_embeddings = embeddings.embed_documents(sample_texts)
        
        # Add points to collection
        points = []
        for i, (text, embedding) in enumerate(zip(sample_texts, sample_embeddings)):
            points.append(qdrant_models.PointStruct(
                id=i,
                vector=embedding,
                payload={"text": text, "source": "sample_data"}
            ))
        
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        print(f"✅ Added {len(sample_texts)} sample documents to collection!")
        
except Exception as e:
    print(f"❌ Error: {e}") 