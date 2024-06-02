import streamlit as st
from datetime import datetime
import time

# Function to display user's message
def show_user_message(message):
    st.markdown(
        f'<div style="background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 10px 0;">'
        f'<span style="color: #006400;"><strong>You:</strong></span><br>{message}</div>',
        unsafe_allow_html=True
    )

# Function to display assistant's message
def show_assistant_message(message):
    st.markdown(
        f'<div style="background-color: #F0F0F0; padding: 10px; border-radius: 10px; margin: 10px 0;">'
        f'<span style="color: #696969;"><strong>Mika:</strong></span><br>{message}</div>',
        unsafe_allow_html=True
    )

# Main program
def main():
    st.title("Mika Chat Assistant")

    # User input with icon
    user_input = st.text_input("You:", value="", help="Enter your message here... 📝", key="user_input")

    if st.button("Send 🚀"):
        if user_input.strip():
            # Display user's message
            show_user_message(user_input)
            
            # Simulate typing delay
            st.markdown('<span style="color: #696969;"><em>Mika is typing...</em></span>', unsafe_allow_html=True)
            time.sleep(2)  # Simulate typing delay
            
            # Simulate assistant response (replace with actual response from the assistant)
            response = "Hello! How can I assist you today?"
            
            # Display assistant's message
            show_assistant_message(response)
            
            # Clear the input field
            st.session_state.user_input = ""

if __name__ == "__main__":
    main()
