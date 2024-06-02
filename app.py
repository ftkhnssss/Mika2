import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY
import time

# Konfigurasi Kunci API
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk memulai sesi obrolan
@st.cache(allow_output_mutation=True)
def start_chat(device_id):
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
        system_instruction="Hi! Saya Mika, asisten kesehatan virtual Anda. Silakan perkenalkan diri Anda di awal percakapan. Saya bisa membantu Anda dengan berbagai pertanyaan kesehatan. Pastikan untuk memberikan informasi lengkap dan detail agar saya bisa memberikan saran yang akurat. 😊",
        session_id=device_id  # Menggunakan device_id untuk membuat sesi unik perangkat
    )
    return model

# Fungsi untuk menampilkan pesan pengguna
def show_user_message(message):
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 85%;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan pesan asisten
def show_assistant_message(message, placeholder):
    placeholder.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
            <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

def type_message(message, placeholder):
    typed_text = ""
    for char in message:
        typed_text += char
        show_assistant_message(typed_text, placeholder)
        time.sleep(0.05)  # Adjust the typing speed here

# Program utama
def main():
    device_id = id(st)  # Menggunakan ID perangkat untuk setiap perangkat

    st.title("Mika-Test")

    # Memulai sesi obrolan
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat(device_id)

    # Inisialisasi riwayat obrolan jika belum ada
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Input pengguna
    user_input = st.text_input("Ketik pesan Anda di sini:")

    if st.button("Kirim"):
        if user_input.strip():
            # Menampilkan pesan pengguna
            show_user_message(user_input)
            
            # Placeholder untuk animasi mengetik
            typing_placeholder = st.empty()
            with typing_placeholder.container():
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                        <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc;">
                            <em>Mika is typing...</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Simulasi penundaan untuk animasi mengetik
            time.sleep(2)
            
            # Mengirim pesan pengguna ke model
            response = st.session_state.chat_session.start_chat(history=[])
            
            # Menambahkan pesan pengguna dan asisten ke riwayat obrolan
            st.session_state.chat_history.append(("Anda", user_input))
            st.session_state.chat_history.append(("Mika", response.text))
            
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
            show_user_message(message)
        else:
            show_assistant_message(message, st.empty())

    # Tombol untuk menghapus riwayat obrolan
    if st.button("Hapus Riwayat Obrolan"):
        st.session_state.chat_history = []
        st.session_state.chat_session = start_chat(device_id)  # Memulai kembali sesi obrolan
        st.experimental_rerun()

if __name__ == "__main__":
    main()
