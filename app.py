import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY

# Konfigurasi Kunci API
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk memulai sesi obrolan
@st.cache_resource
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
        system_instruction="Kamu adalah Mika, asisten kesehatan virtual yang dibuat oleh Utamen. Harap perkenalkan diri Anda dengan lengkap di awal sesi percakapan. Segera jelaskan apa yang mungkin dialami oleh pengguna, tanpa menyebut bahwa Anda bukan dokter. Selalu tanyakan keluhan lain setelah pengguna menyebutkan keluhan pertama, untuk jawaban yang lebih akurat. Jangan menjawab pertanyaan mereka sebelum mereka selesai berbicara. Sertakan juga rekomendasi untuk pengguna. Jika memungkinkan, berikan satu diagnosis saja. Untuk saran seperti 'konsultasikan ke dokter', pindahkan ke bagian akhir teks Anda. Katakan bahwa Anda adalah asisten virtual, bukan dokter, dan untuk hasil yang lebih akurat, pengguna harus memeriksakan diri. Juga, tanyakan nama, jenis kelamin, dan usia pengguna agar diagnosis lebih akurat. Sebagai tambahan, panggil pengguna berdasarkan usianya: 0-15 tahun (Dik), 16-29 tahun (Kak), dan usia di atasnya (Bapak/Ibu). Gunakan bahasa yang sopan dan emotikon untuk menambah daya tarik. Jika pengguna tidak menyebutkan nama, jenis kelamin, dan usia, tanyakan lagi sebelum memberikan jawaban.",
    )
    return model.start_chat(history=[])

# Fungsi untuk menampilkan pesan pengguna
def show_user_message(message):
    st.text_area("You:", message, height=None, max_chars=None, key=None, help=None)

# Fungsi untuk menampilkan pesan asisten
def show_assistant_message(message):
    st.text_area("Mika:", message, height=None, max_chars=None, key=None, help=None)

# Program utama
def main():
    st.title("Mika Chat Assistant")

    # Memulai sesi obrolan
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat()

    # Inisialisasi riwayat obrolan jika belum ada
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Input pengguna
    user_input = st.text_input("Type your message here:")

    if st.button("Send"):
        if user_input.strip():
            # Menampilkan pesan pengguna
            show_user_message(user_input)
            
            # Mengirim pesan pengguna ke model
            response = st.session_state.chat_session.send_message(user_input)
            
            # Menambahkan pesan pengguna dan asisten ke riwayat obrolan
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Mika", response.text))
        
        # Menghapus isi bidang input
        st.experimental_rerun()

    # Menampilkan riwayat obrolan
    chat_history_reversed = reversed(st.session_state.chat_history)
    for sender, message in chat_history_reversed:
        if sender == "You":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Tombol untuk menghapus riwayat obrolan
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.chat_session = start_chat()  # Memulai kembali sesi obrolan
        st.experimental_rerun()

if __name__ == "__main__":
    main()
