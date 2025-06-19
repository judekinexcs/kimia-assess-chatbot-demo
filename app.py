# 🧠 Streamlit Chatbot App for KIMIA Assess (Querying from Qdrant)
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

# 🔑 Setup OpenAI key
openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# 🔌 Setup Qdrant connection
qdrant_url = st.secrets["QDRANT_URL"] if "QDRANT_URL" in st.secrets else os.getenv("QDRANT_URL")
qdrant_api_key = st.secrets["QDRANT_API_KEY"] if "QDRANT_API_KEY" in st.secrets else os.getenv("QDRANT_API_KEY")
collection_name = "kimia_assess"

client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

vectorstore = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embeddings,
    content_payload_key="text"
)

# Build RAG chain
def setup_chain():
    llm = ChatOpenAI(temperature=0.1, model_name="gpt-4", openai_api_key=openai_api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    return chain

rag_chain = setup_chain()

# 🎨 Streamlit UI
st.set_page_config(page_title="KIMIA Chatbot", page_icon="🧬")
st.title("🧬 KIMIA Assess Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Ask me anything about KIMIA Assess:")

if query:
    with st.spinner("Thinking..."):
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
