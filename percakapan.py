import firebase_admin
from firebase_admin import credentials, db
import time
import uuid
import google.generativeai as genai
import streamlit as st

import os

# Mendapatkan path ke direktori saat ini (tempat file percakapan.py berada)
current_directory = os.path.dirname(__file__)

# Membangun path lengkap ke serviceAccountKey.json
service_account_key_path = os.path.join(current_directory, "mika-test-f7138-firebase-adminsdk-qnp9p-ac39df705b.json")

# Inisialisasi Firebase menggunakan kredensial dari serviceAccountKey.json
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred)

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

# Fungsi untuk menyimpan percakapan ke dalam Firebase
def save_chat_history_to_firebase(chat_history, session_id):
    ref = db.reference(f'chat_history/{session_id}')
    ref.set(chat_history)

# Fungsi untuk memuat percakapan dari Firebase
def load_chat_history_from_firebase(session_id):
    ref = db.reference(f'chat_history/{session_id}')
    chat_history = ref.get()
    return chat_history if chat_history else []

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

# Program utama
def main():
    st.title("Mika-Test")

    # Session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())  # Inisialisasi session_id jika belum ada
    session_id = st.session_state.session_id

    # Memulai sesi obrolan
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat()

    # Inisialisasi riwayat obrolan jika belum ada
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history_from_firebase(session_id)

    # Input pengguna
    user_input = st.text_input("Ketik pesan Anda di sini:")

    if st.button("Kirim"):
        if user_input.strip():
            # Menampilkan pesan pengguna
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 85%; color: black;">
                        {user_input}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Placeholder untuk animasi mengetik
            typing_placeholder = st.empty()
            with typing_placeholder.container():
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px; color: black;">
                        <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc;">
                            <em>Mika is typing...</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Simulasi penundaan untuk animasi mengetik
            time.sleep(2)
            
            # Mengirim pesan pengguna ke model
            response = st.session_state.chat_session.send_message(user_input)
            
            # Menambahkan pesan pengguna dan asisten ke riwayat obrolan
            st.session_state.chat_history.append(("Anda", user_input))
            st.session_state.chat_history.append(("Mika", response.text))
            
            # Simpan riwayat obrolan ke Firebase
            save_chat_history_to_firebase(st.session_state.chat_history, session_id)
            
            # Menghapus placeholder dan menampilkan pesan bot yang sebenarnya per huruf
            typing_placeholder.empty()
            typing_placeholder = st.empty()  # Create a new placeholder for the typing animation
            type_message(response.text, typing_placeholder)
        
        # Menghapus isi bidang input
        st.experimental_rerun()

    # Menampilkan riwayat obrolan
    chat_history_reversed = reversed(st.session_state.chat_history)
    for sender, message in chat_history_reversed:
        if sender == "Anda":
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 85%; color: black;">
                        {message}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                    <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc; color: black;">
                        {message}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Tombol untuk menghapus riwayat obrolan
if st.button("Hapus Riwayat Obrolan"):
    # Hapus riwayat obrolan dari session_state
    st.session_state.chat_history = []
    # Simpan perubahan ke Firebase
    save_chat_history_to_firebase(st.session_state.chat_history, session_id)
    # Mulai kembali sesi obrolan
    st.session_state.chat_session = start_chat()
    # Jalankan kembali aplikasi
    st.experimental_rerun()
