import json
import time
import uuid
import google.generativeai as genai
import streamlit as st

from config import GEMINI_API_KEY

# Konfigurasi Kunci API
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk memulai sesi obrolan
@st.cache(allow_output_mutation=True)
def start_chat():
    # Konfigurasi untuk pembangkitan teks dan pengaturan keamanan
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
    # Inisialisasi model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,
        system_instruction="Hi! Saya Mika, asisten kesehatan virtual Anda. Silakan perkenalkan diri Anda di awal percakapan. Saya bisa membantu Anda dengan berbagai pertanyaan kesehatan. Pastikan untuk memberikan informasi lengkap dan detail agar saya bisa memberikan saran yang akurat. 😊"
    )
    return model.start_chat(history=[])

# Fungsi untuk menyimpan percakapan ke dalam file JSON
def save_chat_history(chat_history, session_id):
    with open(f'{session_id}_chat_history.json', 'w') as file:
        json.dump(chat_history, file)

# Fungsi untuk memuat percakapan dari file JSON
def load_chat_history(session_id):
    try:
        with open(f'{session_id}_chat_history.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Fungsi untuk menampilkan pesan asisten dengan animasi mengetik
def type_message(message, placeholder):
    typed_text = ""
    for char in message:
        typed_text += char
        placeholder.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px; color: black;">
                <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc;">
                    {typed_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.05)  # Adjust the typing speed here
