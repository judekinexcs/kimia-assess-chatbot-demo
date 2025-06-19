# 🧠 Streamlit Chatbot App for KIMIA Assess (Querying from Qdrant)
import streamlit as st
import os

# 🎨 Streamlit UI
st.set_page_config(page_title="KIMIA Chatbot", page_icon="🧬")
st.title("🧬 KIMIA Assess Chatbot")

# Check if required environment variables are set
st.write("🔍 Checking environment setup...")

# Check OpenAI API Key
openai_api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("❌ OPENAI_API_KEY not found! Please set it in your environment variables or Streamlit secrets.")
    st.stop()

# Check Qdrant configuration
qdrant_url = st.secrets.get("QDRANT_URL") if hasattr(st, 'secrets') else os.getenv("QDRANT_URL")
qdrant_api_key = st.secrets.get("QDRANT_API_KEY") if hasattr(st, 'secrets') else os.getenv("QDRANT_API_KEY")

if not qdrant_url or not qdrant_api_key:
    st.error("❌ QDRANT_URL or QDRANT_API_KEY not found! Please set them in your environment variables or Streamlit secrets.")
    st.stop()

st.success("✅ Environment variables are set!")

# Try to import required libraries
try:
    from langchain_openai import ChatOpenAI
    from langchain.chains import ConversationalRetrievalChain
    from langchain_community.vectorstores import Qdrant
    from langchain_openai import OpenAIEmbeddings
    from langchain.memory import ConversationBufferMemory
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qdrant_models
    st.success("✅ All required libraries imported successfully!")
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.error("Please install required packages: pip install -r requirements.txt")
    st.stop()

# Try to setup Qdrant connection
try:
    st.write("🔌 Connecting to Qdrant...")
    collection_name = "kimia_assess"
    
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
        content_payload_key="text"
    )
    st.success("✅ Connected to Qdrant successfully!")
except Exception as e:
    st.error(f"❌ Qdrant connection error: {e}")
    st.stop()

# Build RAG chain
try:
    st.write("🔧 Setting up RAG chain...")
    def setup_chain():
        llm = ChatOpenAI(temperature=0.1, model_name="gpt-4", openai_api_key=openai_api_key)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True
        )
        return chain

    rag_chain = setup_chain()
    st.success("✅ RAG chain setup complete!")
except Exception as e:
    st.error(f"❌ RAG chain setup error: {e}")
    st.stop()

st.success("🎉 App is ready! You can now ask questions.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask me anything about KIMIA Assess:")

if query:
    with st.spinner("Thinking..."):
        try:
            result = rag_chain({"question": query, "chat_history": st.session_state.chat_history})
            
            # Update history
            st.session_state.chat_history.append((query, result["answer"]))

            # Display chat
            for q, a in st.session_state.chat_history[::-1]:
                st.markdown(f"**You:** {q}")
                st.markdown(f"**Bot:** {a}")
                st.markdown("---")

            # Show sources
            with st.expander("📚 Source Documents"):
                for doc in result["source_documents"]:
                    st.markdown(f"**From:** {doc.metadata.get('source', '')}")
                    st.markdown(doc.page_content)
                    st.markdown("---")
        except Exception as e:
            st.error(f"❌ Error processing query: {e}") 