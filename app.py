import streamlit as st
from dotenv import find_dotenv, load_dotenv

from llm.prompts import INTRODUCTION_MESSAGE
from utils import (
    generate_response,
    initialize_clients,
    load_config,
    WARNING_MESSAGE,
    QUERY_SUGGESTIONS,
    AUTHORS,
    LOGO_URL,
    LOGO_TEXT_URL,
)

# Load environment variables from the .env file.
load_dotenv(find_dotenv())


# Set Streamlit page configuration with custom title and icon.
st.set_page_config(page_title="Tvoj licni majstor", page_icon=LOGO_URL)
st.image(LOGO_TEXT_URL)
qdrant_client = initialize_clients()
config = load_config()

# Display the logo and set up the sidebar with useful information and links.
# st.image(LOGO_TEXT_URL, width = 400)
st.logo(LOGO_TEXT_URL, icon_image=LOGO_URL)
with st.sidebar:
    st.subheader("💡 Primer pitanja")
    with st.container(border=True, height=250):
        st.markdown(QUERY_SUGGESTIONS)

    st.subheader("⚠️ Upozorenje")
    with st.container(border=True):
        st.markdown(WARNING_MESSAGE)

    st.subheader("✍️ Autori")
    st.markdown(AUTHORS)


# Initialize or update the session state for storing chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": INTRODUCTION_MESSAGE}]

# Display all chat messages stored in the session state.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        html_content = f"<span style='font-size: 24px;'>{message['content']}</span>"
        st.html(html_content)

# Handle user input and generate responses.
if prompt := st.chat_input("Pomozi mi sa..."):
    # Append user message to session state.
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat container.
    with st.chat_message("user"):
        html_content = f"<span style='font-size: 24px;'>{prompt}</span>"
        st.html(html_content)

    with st.chat_message("assistant"):
        # Generate a response using the LLM and display it as a stream.
        stream = generate_response(
            query=prompt,
            qdrant_client=qdrant_client,
            config=config,
        )
        # Write the response stream to the chat.
        response = st.write_stream(stream)

    # Append assistant's response to session state.
    st.session_state.messages.append({"role": "assistant", "content": response})