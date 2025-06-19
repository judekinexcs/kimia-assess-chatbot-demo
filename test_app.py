# 🧠 Simple Test Streamlit App
import streamlit as st

# 🎨 Streamlit UI
st.set_page_config(page_title="KIMIA Chatbot Test", page_icon="🧬")
st.title("🧬 KIMIA Assess Chatbot Test")

st.write("Hello! This is a test page to see if Streamlit is working.")

# Test basic functionality
if st.button("Click me!"):
    st.write("Button clicked! Streamlit is working.")

# Test text input
user_input = st.text_input("Enter some text:")
if user_input:
    st.write(f"You entered: {user_input}") 