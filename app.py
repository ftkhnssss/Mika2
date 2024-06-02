import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY
import time

# Konfigurasi Kunci API
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk memulai sesi obrolan
def start_chat():
    # Inisialisasi model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ],
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
        system_instruction="Hi! Saya Mika, asisten kesehatan virtual Anda. Silakan perkenalkan diri Anda di awal percakapan. Saya bisa membantu Anda dengan berbagai pertanyaan kesehatan. Pastikan untuk memberikan informasi lengkap dan detail agar saya bisa memberikan saran yang akurat. 😊"
    )
    return model.start_chat(history=[])

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
def show_assistant_message(message):
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
            <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc; color: black;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan animasi mengetik
def type_message(message):
    typed_text = ""
    for char in message:
        typed_text += char
        show_assistant_message(typed_text)
        time.sleep(0.05)  # Atur kecepatan mengetik di sini

# Program utama
def main():
    st.title("Mika-Test")

    # Mendapatkan ID pengguna unik dari session cookie
    user_id = st.session_state.user_id or hash(st.session_state)

    # Set session cookie untuk pengguna ini
    st.session_state.user_id = user_id

    # Memulai sesi obrolan untuk pengguna ini jika belum ada
    if f"chat_session_{user_id}" not in st.session_state:
        st.session_state[f"chat_session_{user_id}"] = start_chat()

    # Inisialisasi riwayat obrolan jika belum ada
    if f"chat_history_{user_id}" not in st.session_state:
        st.session_state[f"chat_history_{user_id}"] = []

    # Input pengguna
    user_input = st.text_input("Ketik pesan Anda di sini:")

    if st.button("Kirim"):
        if user_input.strip():
            # Mengirim pesan pengguna ke model
            response = st.session_state[f"chat_session_{user_id}"].send_message(user_input)
            
            # Menambahkan pesan pengguna dan asisten ke riwayat obrolan
            st.session_state[f"chat_history_{user_id}"].append(("Anda", user_input))
            st.session_state[f"chat_history_{user_id}"].append(("Mika", response.text))
        
            # Menampilkan pesan pengguna dan pesan Mika satu per satu
            show_user_message(user_input)
            type_message(response.text)
        
        # Menghapus isi bidang input
        st.experimental_rerun()

    # Menampilkan riwayat obrolan
    chat_history_reversed = reversed(st.session_state[f"chat_history_{user_id}"])
    for sender, message in chat_history_reversed:
        if sender == "Anda":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Tombol untuk menghapus riwayat obrolan
    if st.button("Hapus Riwayat Obrolan"):
        st.session_state[f"chat_history_{user_id}"] = []
        st.session_state[f"chat_session_{user_id}"] = start_chat()  # Memulai kembali sesi obrolan
        st.experimental_rerun()

if __name__ == "__main__":
    main()
