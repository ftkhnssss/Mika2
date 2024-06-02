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
        system_instruction="Hi! Saya Mika, asisten kesehatan virtual Anda. Silakan perkenalkan diri Anda di awal percakapan. Saya bisa membantu Anda dengan berbagai pertanyaan kesehatan. Pastikan untuk memberikan informasi lengkap dan detail agar saya bisa memberikan saran yang akurat. 😊"
    )
    return model.start_chat(history=[])

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
def show_assistant_message(message):
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
            <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; max-width: 85%; border: 1px solid #ccc;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Program utama
def main():
    st.title("Mika-Test")

    # Memulai sesi obrolan
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat()

    # Inisialisasi riwayat obrolan jika belum ada
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Bagian input pengguna dan tombol dengan posisi tetap
    st.markdown("""
        <style>
            .fixed-footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: white;
                padding: 10px 0;
                box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
            }
            .fixed-footer div {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .fixed-footer input {
                flex: 1;
                margin-right: 10px;
            }
        </style>
        <div class="fixed-footer">
            <div>
                <input type="text" id="user_input" placeholder="Ketik pesan Anda di sini:">
                <button id="send_button">Kirim</button>
                <button id="clear_button">Hapus Riwayat Obrolan</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    user_input = st.text_input("", key="user_input_key", label_visibility="collapsed")

    if st.button("Kirim", key="send_button"):
        if user_input.strip():
            # Menampilkan pesan pengguna
            show_user_message(user_input)
            
            # Mengirim pesan pengguna ke model
            response = st.session_state.chat_session.send_message(user_input)
            
            # Menambahkan pesan pengguna dan asisten ke riwayat obrolan
            st.session_state.chat_history.append(("Anda", user_input))
            st.session_state.chat_history.append(("Mika", response.text))
        
        # Menghapus isi bidang input
        st.experimental_rerun()

    # Menampilkan riwayat obrolan
    chat_history_reversed = reversed(st.session_state.chat_history)
    for sender, message in chat_history_reversed:
        if sender == "Anda":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Tombol untuk menghapus riwayat obrolan
    if st.button("Hapus Riwayat Obrolan", key="clear_button"):
        st.session_state.chat_history = []
        st.session_state.chat_session = start_chat()  # Memulai kembali sesi obrolan
        st.experimental_rerun()

if __name__ == "__main__":
    main()
