import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configuration of API Key
genai.configure(api_key=GEMINI_API_KEY)

# Function to start the chat session
@st.cache(allow_output_mutation=True)
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
    st.write(f"You: {message}")

# Function to display assistant's message
def show_assistant_message(message):
    st.write(f"Mika: {message}")

# Main program
def main():
    st.title("Mika Chat Assistant")

    # Start chat session
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat()

    # Initialize chat history if not already
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("You:", "")

    if st.button("Send"):
        # Display user's message
        show_user_message(user_input)
        
        # Send user's message to the model
        response = st.session_state.chat_session.send_message(user_input)
        
        # Add user and assistant messages to the chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Mika", response.text))

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
