def main():
    st.title("Mika Chat Assistant")
    add_custom_css()

    # Initialize chat history if not already
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar options
    with st.sidebar:
        st.header("Options")
        st.write("Current Session:")
        current_session_id = hash(tuple(st.session_state.chat_history))  # Generate unique ID for current session
        st.write(f"Session ID: {current_session_id}")
        
        # Add button to start new session
        if st.button("Start New Session"):
            save_chat_history()  # Save current session
            st.session_state.chat_history = []  # Reset chat history for new session
            st.session_state.chat_session = start_chat()  # Start new chat session
            st.experimental_rerun()

        # Add button to clear all sessions
        if st.button("Clear All Sessions"):
            st.session_state.saved_chats = []  # Clear all saved sessions
            st.experimental_rerun()

        # Add saved sessions
        if 'saved_chats' in st.session_state:
            st.write("Saved Sessions:")
            for i, chat in enumerate(st.session_state.saved_chats):
                session_id = hash(tuple(chat))  # Generate unique ID for saved session
                st.write(f"Session {i+1}:")
                st.write(f"Session ID: {session_id}")
                if st.button(f"Load Session {i+1}"):
                    st.session_state.chat_history = chat  # Load selected session
                    st.session_state.chat_session = start_chat()  # Start chat session for selected session
                    st.experimental_rerun()

    # Start chat session
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = start_chat()

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            show_user_message(message)
        else:
            show_assistant_message(message)

    # Input container
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)

    if 'send_button' in st.session_state and send_button and user_input.strip():
        # Display user's message
        show_user_message(user_input)
        
        # Send user's message to the model
        response = st.session_state.chat_session.send_message(user_input)
        
        # Add user and assistant messages to the chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Mika", response.text))
        
        # Clear the input field
        st.session_state.user_input = ""  # Menggunakan user_input untuk membersihkan input
        st.experimental_rerun()
        
    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.chat_session = start_chat()  # Restart the chat session
        st.experimental_rerun()

if __name__ == "__main__":
    main()
