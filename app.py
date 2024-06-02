import streamlit as st
import json
import time
import uuid
import hashlib
from user_agents import parse
import google.generativeai as genai
from config import GEMINI_API_KEY

# Konfigurasi Kunci API
genai.configure(api_key=GEMINI_API_KEY)

# Generate UUID based on timestamp, IP address, and user agent
def generate_uuid():
    # Timestamp
    timestamp = str(time.time())
    # IP Address
    ip_address = st.experimental_get_query_params().get('client_ip', [''])[0]
    # User Agent
    user_agent = st.experimental_get_query_params().get('user_agent', [''])[0]
    device_info = parse(user_agent)
    # Combine all information
    combined_info = f"{timestamp}{ip_address}{user_agent}"
    # Generate UUID from combined information
    uuid_hash = hashlib.sha256(combined_info.encode()).hexdigest()
    return uuid_hash

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

# Fungsi untuk menampilkan pesan pengguna
def show_user_message(message):
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 85%; color: black;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan pesan asisten
def show_assistant_message(message, placeholder):
    placeholder.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
            <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc; color: black;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan pesan satu karakter per waktu
def type_message(message, placeholder):
    typed_text = ""
    for char in message:
        typed_text += char
        show_assistant_message(typed_text, placeholder)
        time.sleep(0.05)  # Sesuaikan kecepatan pengetikan di sini

# Program utama
def main():
    st.title("Mika-Test")

    # Session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_uuid()  # Inisialisasi session_id jika belum ada
    session_id = st.session_state.session_id

    # Memulai sesi obrolan
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = start_chat()

    # Input pengguna
    user_input = st.text_input("Ketik pesan Anda di sini:")

    if st.button("Kirim"):
        if user_input.strip():
            # Menampilkan pesan pengguna
            show_user_message(user_input)
            
            # Placeholder untuk animasi pengetikan
            typing_placeholder = st.empty()
            with typing_placeholder.container():
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px; color: black;">
                        <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc;">
                            <em>Mika is typing...</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Simulasi penundaan untuk animasi pengetikan
            time.sleep(2)
            
            # Menambahkan pesan pengguna ke riwayat obrolan
            st.session_state.chat_history.append(("Anda", user_input))
            
            # Simpan riwayat obrolan ke dalam file JSON
            save_chat_history(st.session_state.chat_history, session_id)
            
            # Menghapus placeholder dan menampilkan pesan bot sebenarnya per karakter
            typing_placeholder.empty()
            typing_placeholder = st.empty()  # Create a new placeholder for the typing animation
            response = "Ini adalah pesan bot yang panjangnya bervariasi."  # Ganti dengan respons aktual dari bot
            type_message(response, typing_placeholder)
        
        # Menghapus isi bidang input
        st.experimental_rerun()

    # Menampilkan riwayat obrolan
    chat_history_reversed = reversed(st.session_state.chat_history)
    for sender, message in chat_history_reversed:
        if sender == "Anda":
            show_user_message(message)
        else:
            show_assistant_message(message, st.empty())

    # Tombol untuk menghapus riwayat obrolan
    if st.button("Hapus Riwayat Obrolan"):
        st.session_state.chat_history = []
        save_chat_history(st.session_state.chat_history, session_id)  # Simpan perubahan ke dalam file JSON
        st.experimental_rerun()

if __name__ == "__main__":
    main
