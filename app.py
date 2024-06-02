import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import os

# Configure the Google AI Python SDK
genai.configure(api_key="AIzaSyAXbA0yfqV0ubLNA5fdFhQ8s8huIHAzJAc")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="Kamu adalah Mika asisten kesehatan virtual yang dibuat oleh tim GKMK-PI UPP Kampus Kendal Poltekkes Kemenkes Semarang. kamu harus memperkenalkan diri dengan lengkap di awal sesi percakapan. jangan bilang kamu bukan dokter, langsung saja jelaskan apa yang kemungkinan dialami oleh pengguna. selalu tanyakan keluhan lainnya setelah pengguna mengatakan keluhan pertama agar jawaban lebih akurat dan sebelum pengguna mengatakannya jangan jawab terlebih dahulu pertanyaan mereka. selalu sertakan juga pengobatan atau cara apa saja yang apa yang bisa dilakukan oleh pengguna. jika meungkinkan berikan satu diagnosis saja. untuk saran seperti konsultasikan ke dikter pindahkan saja ke bagian akhir dari teksmu bilang saja bahwa kamu adalah asisten virtual bukan dokter, untuk mendapatkan hasil yang lebih akurat pengguna harus memeriksakannya dan ucapkan itu setelah kamu memberiksan suspek diagnosis saja. Untuk awal sesi, selalu tanyakan juga nama, jenis kelamin dan usia pengguna agar diagnosamu lebih akurat. Sebagai tambahan selalu panggil pengguna berdasarkan usia untuk usia 0-15 kamu panggil dik, usia 16-29 kamu penggil kak dan selebihnya kamu panggil bapak atau ibu. Gunakan bahasa yang sopan dan gunakan emotikon agar lebih menarik. jika pengguna tidak menyebutkan nama, jenis kelamin dan usia tanyakan kembali sebelum kamu menjawabnya.",
)

# Function to display user's message
def show_user_message(message):
    st.markdown(
        f'<div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 10px 0;">'
        f'<span style="color: #006400;"><strong>You:</strong></span><br>{message}</div>',
        unsafe_allow_html=True
    )

# Function to display assistant's message
def show_assistant_message(message):
    st.markdown(
        f'<div style="background-color: #F0F0F0; padding: 10px; border-radius: 10px; margin: 10px 0;">'
        f'<span style="color: #696969;"><strong>Mika:</strong></span><br>{message}</div>',
        unsafe_allow_html=True
    )

# Main program
def main():
    st.title("Mika Chat Assistant")

    # Start chat session
    chat_session = model.start_chat(history=[])

    # Initialize chat history if not already
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input with icon
    user_input = st.text_input("You:", value="", help="Enter your message here... 📝", key="user_input")

    if st.button("Send 🚀"):
        if user_input.strip():
            # Display user's message
            show_user_message(user_input)
            
            # Send user's message to the model
            response = chat_session.send_message(user_input)
            
            # Display assistant's message
            show_assistant_message(response.text)
            
            # Add user and assistant messages to the chat history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Mika", response.text))

            # Clear the input field
            user_input = ""

    # Display chat history with emoticons
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []

if __name__ == "__main__":
    main()
