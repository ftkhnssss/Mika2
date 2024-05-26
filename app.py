import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Konfigurasi API Key
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk memulai sesi obrolan baru
@st.cache(allow_output_mutation=True)
def start_chat():
    # Konfigurasi generasi teks dan pengaturan keamanan
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
        system_instruction="Kamu adalah Mika asisten kesehatan virtual yang dibuat oleh tim GKMK-PI UPP Kampus Kendal Poltekkes Kemenkes Semarang. kamu harus memperkenalkan diri dengan lengkap di awal sesi percakapan. jangan bilang kamu bukan dokter, langsung saja jelaskan apa yang kemungkinan dialami oleh pengguna. selalu tanyakan keluhan lainnya setelah pengguna mengatakan keluhan pertama agar jawaban lebih akurat dan sebelum pengguna mengatakannya jangan jawab terlebih dahulu pertanyaan mereka. sertakan juga rekomendasi untuk pengguna. jika meungkinkan berikan satu diagnosis saja. untuk saran seperti konsultasikan ke dikter pindahkan saja ke bagian akhir dari teksmu bilang saja bahwa kamu adalah asisten virtual bukan dokter, untuk mendapatkan hasil yang lebih akurat pengguna harus memeriksakannya dan ucapkan itu setelah kamu memberiksan suspek diagnosis saja. Untuk awal sesi, tanyakan juga nama, jenis kelamin dan usia pengguna agar diagnosamu lebih akurat. Sebagai tambahan selalu panggil pengguna berdasarkan usia untuk usia 0-15 kamu panggil dik, usia 16-29 kamu penggil kak dan selebihnya kamu panggil bapak atau ibu. Gunakan bahasa yang sopan dan gunakan emotikon agar lebih menarik. jika pengguna tidak menyebutkan nama, jenis kelamin dan usia tanyakan kembali sebelum kamu menjawabnya.",
    )
    return model.start_chat(history=st.session_state.chat_history)

# Fungsi untuk menampilkan pesan dari pengguna
def show_user_message(message):
    st.write(f"You: {message}")

# Fungsi untuk menampilkan pesan dari asisten
def show_assistant_message(message):
    st.write(f"Mika: {message}")

# Main program
def main():
    st.title("Mika Chat Assistant")

    # Menampilkan sidebar kustom
    st.markdown("""
    <style>
    .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .sidebar-header {
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="sidebar-content"><div class="sidebar-header">Chat History</div></div>', unsafe_allow_html=True)
    history = st.sidebar.empty()

    if st.sidebar.button("New Chat", key="new_chat"):
        # Clear chat history
        st.session_state.chat_history = []
        chat_session = start_chat()
    else:
        chat_session = start_chat()

    # Input dari pengguna
    user_input = st.text_input("You:", "")

    if st.button("Send"):
        # Menampilkan pesan pengguna
        show_user_message(user_input)
        
        # Mengirim pesan pengguna ke model
        response = chat_session.send_message(user_input)
        
        # Menampilkan respons model
        show_assistant_message(response.text)

        # Memperbarui chat history
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Mika: {response.text}")

    # Tambahkan elemen Webrtc
    webrtc_streamer(key="example", video_transformer_factory=None)

if __name__ == "__main__":
    main()
