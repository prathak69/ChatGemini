import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini Bro!",
    page_icon="💎",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Load and configure the Google Gemini-Pro AI model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Custom CSS for styling
st.markdown("""
    <style>
        .st-chat-message {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .st-chat-message.you {
            background-color: #dfe7fd;
            border-left: 5px solid #1a73e8;
        }
        .st-chat-message.bro {
            background-color: #f3e5f5;
            border-left: 5px solid #9c27b0;
        }
        .st-chat-message.assistant {
            background-color: #f9fbe7;
            border-left: 5px solid #4caf50;
        }
        .st-title {
            color: #1a73e8;
            text-align: center;
            font-weight: bold;
        }
        .st-chat-input {
            margin-top: 20px;
        }
        .st-markdown {
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Display the chatbot's title on the page
st.title("💎 Gemini Bro")

# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini Bro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("you").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("bro"):
        st.markdown(gemini_response.text)

# Add a footer or additional sections if needed
st.markdown("---")
st.markdown("👾 Created with 💜 by Prathak Soni")
