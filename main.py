import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import Runnable
from langchain_community.chat_models import ChatOllama

# Initialize the model
llm = ChatOllama(model="phi3:latest")  # Replace with your Ollama model name

# Streamlit UI setup
st.set_page_config(page_title="Chat with LLM", layout="centered")
st.title("PHI LLM Chatbot")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="Hello! I'm your chatbot. How can I help you today?")
    ]

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    else:
        with st.chat_message("ai"):
            st.markdown(msg.content)

# Chat input box
user_input = st.chat_input("Type your message here...")

# Handle user input
if user_input:
    # Append user message
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            # Get response from the model
            response = llm.invoke(st.session_state.messages)
            st.markdown(response.content)
            # Save AI response to history
            st.session_state.messages.append(AIMessage(content=response.content))
