import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configuration of API Key
genai.configure(api_key=GEMINI_API_KEY)

# Function to start the chat session
@st.cache_resource
def start_chat():
    # Configuration for text generation and security settings
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    # Model initialization
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,
        system_instruction="Kamu adalah Mika asisten kesehatan virtual yang dibuat oleh tim GKMK-PI UPP Kampus Kendal Poltekkes Kemenkes Semarang. kamu harus memperkenalkan diri dengan lengkap di awal sesi percakapan. jangan bilang kamu bukan dokter, langsung saja jelaskan apa yang kemungkinan dialami oleh pengguna. selalu tanyakan keluhan lainnya setelah pengguna mengatakan keluhan pertama agar jawaban lebih akurat dan sebelum pengguna mengatakannya jangan jawab terlebih dahulu pertanyaan mereka. sertakan juga rekomendasi untuk pengguna. jika meungkinkan berikan satu diagnosis saja. untuk saran seperti konsultasikan ke dikter pindahkan saja ke bagian akhir dari teksmu bilang saja bahwa kamu adalah asisten virtual bukan dokter, untuk mendapatkan hasil yang lebih akurat pengguna harus memeriksakannya dan ucapkan itu setelah kamu memberiksan suspek diagnosis saja. Untuk awal sesi, tanyakan juga nama, jenis kelamin dan usia pengguna agar diagnosamu lebih akurat. Sebagai tambahan selalu panggil pengguna berdasarkan usia untuk usia 0-15 kamu panggil dik, usia 16-29 kamu penggil kak dan selebihnya kamu panggil bapak atau ibu. Gunakan bahasa yang sopan dan gunakan emotikon agar lebih menarik. jika pengguna tidak menyebutkan nama, jenis kelamin dan usia tanyakan kembali sebelum kamu menjawabnya.",
    )
    return model.start_chat(history=[])

# Function to display user's message
def show_user_message(message):
    st.markdown(f'<div class="user-message">You: {message}</div>', unsafe_allow_html=True)

# Function to display assistant's message
def show_assistant_message(message):
    st.markdown(f'<div class="assistant-message">Mika: {message}</div>', unsafe_allow_html=True)

# Add custom CSS for better UI
def add_custom_css():
    st.markdown(
        """
        <style>
        .user-message {
            background-color: #DCF8C6;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            max-width: 60%;
            float: right;
            clear: both;
        }
        .assistant-message {
            background-color: #F1F0F0;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            max-width: 60%;
            float: left;
            clear: both;
        }
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .message-container {
            display: flex;
            align-items: center;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: white;
            padding: 10px;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        }
        .stTextInput {
            width: calc(100% - 85px); /* Adjusted for the Send button */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to save the current chat session
def save_chat_history():
    if 'saved_chats' not in st.session_state:
        st.session_state.saved_chats = []
    st.session_state.saved_chats.append(st.session_state.chat_history)

# Main program
def main():
    st.title("Mika Chat Assistant")
    add_custom_css()

    # Sidebar options
    with st.sidebar:
        st.header("Options")
        st.write("Current Session:")
        current_session_id = hash(tuple(st.session_state.chat_history))  # Generate unique ID for current session
        st.write(f"Session ID: {current_session_id}")
        
        # Add button to start new session
        if st.button("Start New Session"):
            save_chat_history()  # Save current session
            st.session_state.chat_history = []  # Reset chat history for new session
            st.session_state.chat_session = start_chat()  # Start new chat session
            st.experimental_rerun()

        # Add button to clear all sessions
        if st.button("Clear All Sessions"):
            st.session_state.saved_chats = []  # Clear all saved sessions
            st.experimental_rerun()

        # Add saved sessions
        if 'saved_chats' in st.session_state:
            st.write("Saved Sessions:")
            for i, chat in enumerate(st.session_state.saved_chats):
                session_id = hash(tuple(chat))  # Generate unique ID for saved session
                st.write(f"Session {i+1}:")
                st.write(f"Session ID: {session_id}")
                if st.button(f"Load Session {i+1}"):
                    st.session_state.chat_history = chat  # Load selected session
                    st.session_state.chat_session = start_chat()  # Start chat session for selected session
                    st.experimental_rerun()

    # Start chat session
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat()

    # Initialize chat history if not already
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Input container
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True
