import streamlit as st
import json
import google.generativeai as genai
import time
import os

# Konfigurasi Kunci API
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk memulai sesi obrolan
@st.cache(allow_output_mutation=True)
def start_chat(session_id):
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

# Fungsi untuk menyimpan percakapan ke dalam file JSON dengan nama sesuai angka acak
def save_chat_history(chat_history, session_id):
    with open(f'{session_id}_chat_history.json', 'w') as file:
        json.dump(chat_history, file)

# Fungsi untuk memuat percakapan dari file JSON dengan nama sesuai angka acak
def load_chat_history(session_id):
    try:
        with open(f'{session_id}_chat_history.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Program utama
def main():
    st.title("Mika-Test")

    # Meminta pengguna untuk memasukkan angka acak saat pertama kali mengakses aplikasi
    random_number = st.text_input("Masukkan 6 angka acak:", max_chars=6)

    if len(random_number) != 6:
        st.warning("Anda harus memasukkan 6 angka acak.")

    # Inisialisasi session ID menggunakan angka acak yang dimasukkan oleh pengguna
    session_id = st.session_state.get('session_id') or random_number
    st.session_state.session_id = session_id

    # Memulai sesi obrolan
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat(session_id)

    # Inisialisasi riwayat obrolan jika belum ada
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history(session_id)

    # Input pengguna
    user_input = st.text_input("Ketik pesan Anda di sini:")

    if st.button("Kirim"):
        if user_input.strip():
            # ... Sisa kode penanganan pesan pengguna dan tanggapan asisten ...
            pass

if __name__ == "__main__":
    main()
