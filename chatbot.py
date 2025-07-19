from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import streamlit as st
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        width: 100%;
        max-width: 100%;
        margin: 0;
        padding: 0;
    }
    
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #000000;
        max-width: 70%;
        clear: both;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #000000;
        float: right;
        margin-left: 30%;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        color: #000000;
        float: left;
        margin-right: 30%;
    }
    
    .timestamp {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize model with error handling
@st.cache_resource
def initialize_model():
    try:
        model = ChatOllama(model="phi3:latest")
        return model
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        logger.error(f"Model initialization failed: {str(e)}")
        return None

# Initialize session state
def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "messages" not in st.session_state:
        # Initialize with system message and AI introduction
        st.session_state.messages = [
            SystemMessage(content="You are Sara, a warm and helpful AI assistant designed to help with programming, cloud computing, and general technical guidance. You NEVER refer to yourself as an AI, a model, or Phi-3. You NEVER say you are developed by Microsoft. You are just 'Sara'. You speak in a friendly, polite tone with simple, non-jargon-heavy language. Avoid giving dates or specific years. You prioritize clarity, kindness, and professionalism in every message."),
        ]
    if "model_ready" not in st.session_state:
        st.session_state.model_ready = False
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

# Format timestamp
def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

# Display chat message with styling
def display_message(sender, message, timestamp):
    if sender == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {message}
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 AI:</strong> {message}
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

# Clear chat history
def clear_chat():
    st.session_state.history = []
    # Reset messages to initial state with system message and AI introduction
    st.session_state.messages = [
        SystemMessage(content="I am a coding assistant"),
        AIMessage(content="I am Sara, nice to help you")
    ]
    st.session_state.conversation_started = False
    st.rerun()

# Export chat history
def export_chat():
    if st.session_state.history:
        export_text = f"Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        for sender, message, timestamp in st.session_state.history:
            export_text += f"[{timestamp}] {sender}: {message}\n\n"
        return export_text
    return "No chat history to export."

# Main app
def main():
    initialize_session_state()
    
    # Header
    st.title("🤖 AI Chatbot")
    st.markdown("*Powered by Phi3 - Your AI Assistant*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model status
        model = initialize_model()
        if model:
            st.success("✅ Model loaded successfully")
            st.session_state.model_ready = True
        else:
            st.error("❌ Model failed to load")
            st.session_state.model_ready = False
        
        st.markdown("---")
        
        # Chat statistics
        st.header("📊 Chat Stats")
        total_messages = len(st.session_state.history)
        user_messages = sum(1 for msg in st.session_state.history if msg[0] == "user")
        bot_messages = total_messages - user_messages
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("Exchanges", user_messages)
        
        st.markdown("---")
        
        # Export and clear options
        st.header("🔧 Actions")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
        
        if st.session_state.history:
            export_text = export_chat()
            st.download_button(
                label="💾 Export Chat",
                data=export_text,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            This chatbot uses **Phi3** model through Ollama.
            
            **Features:**
            - Real-time AI responses
            - Chat history
            - Export conversations
            - Responsive design
            
            **Tips:**
            - Be specific in your questions
            - Use clear, concise language
            - Try different topics!
            """)
    
    # Main chat interface
    if not st.session_state.model_ready:
        st.error("⚠️ Model not ready. Please check the sidebar for status.")
        return
    
    # Display chat history
    if st.session_state.history:
        st.markdown("## 💬 Conversation")
        
        # Create container for chat messages
        chat_container = st.container()
        
        with chat_container:
            # Display messages in chronological order (oldest first)
            for sender, message, timestamp in st.session_state.history:
                display_message(sender, message, timestamp)
    
    else:
        # Welcome message
        st.markdown("""
        ## 👋 Welcome to the AI Chatbot!
        
        Start a conversation by typing a message in the input field below.
        
        **Try asking about:**
        - General knowledge questions
        - Creative writing prompts
        - Problem-solving help
        - Casual conversation
        
        I'm here to help! 🚀
        """)
    
    # Chat input form at bottom
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message...",
                key="user_input",
                placeholder="Ask me anything...",
                label_visibility="collapsed"
            )
        
        with col2:
            submitted = st.form_submit_button(
                "Send 📤",
                use_container_width=True,
                type="primary"
            )
    
    # Process user input
    if submitted and user_input.strip():
        if not st.session_state.conversation_started:
            st.session_state.conversation_started = True
        
        # Add user message to history for display
        timestamp = get_timestamp()
        st.session_state.history.append(("user", user_input.strip(), timestamp))
        
        # Add user message to langchain messages
        st.session_state.messages.append(HumanMessage(content=user_input.strip()))
        
        # Generate bot response
        with st.spinner("🤔 Thinking..."):
            try:
                start_time = time.time()
                # Pass all messages to maintain conversation context
                result = model.invoke(st.session_state.messages)
                response_time = time.time() - start_time
                
                bot_timestamp = get_timestamp()
                st.session_state.history.append(("bot", result.content, bot_timestamp))
                
                # Add AI response to langchain messages
                st.session_state.messages.append(AIMessage(content=result.content))
                
                # Log response time
                logger.info(f"Response generated in {response_time:.2f} seconds")
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                bot_timestamp = get_timestamp()
                st.session_state.history.append(("bot", error_msg, bot_timestamp))
                
                # Add error message to langchain messages
                st.session_state.messages.append(AIMessage(content=error_msg))
                
                logger.error(f"Error generating response: {str(e)}")
        
        # Auto-scroll to bottom
        st.rerun()

if __name__ == "__main__":
    main()