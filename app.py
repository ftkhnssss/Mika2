import streamlit as st
import time
import uuid
import json

from percakapan import start_chat, save_chat_history, load_chat_history, type_message

# Program utama
def main():
    st.title("Mika-Test")

    # Session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())  # Inisialisasi session_id jika belum ada
    session_id = st.session_state.session_id

    # Memulai sesi obrolan
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat(session_id)  # Menggunakan session_id sebagai argumen untuk memulai sesi obrolan

    # Inisialisasi riwayat obrolan jika belum ada
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history(session_id)  # Menggunakan session_id untuk memuat histori obrolan

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
            
            # Simpan riwayat obrolan ke dalam file JSON
            save_chat_history(st.session_state.chat_history, session_id)
            
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
        st.session_state.chat_history = []
        save_chat_history(st.session_state.chat_history, session_id)  # Simpan perubahan ke dalam file JSON
        st.session_state.chat_session = start_chat(session_id)  # Memulai kembali sesi obrolan dengan session_id yang baru
        st.experimental_rerun()

if __name__ == "__main__":
    main()
