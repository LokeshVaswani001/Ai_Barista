"""
AI Barista - Streamlit App
---------------------------
A chat interface for the AI Barista RAG agent, deployable for free on
Streamlit Community Cloud.
"""

import asyncio
import os

import streamlit as st
from google.genai import types

from barista_agent import get_runner

st.set_page_config(page_title="AI Barista", page_icon="☕")
st.title("☕ AI Barista")
st.caption("Ask me about our coffee shop menu — drinks, food, or allergens!")

# --- API key setup -----------------------------------------------------
# Set your Gemini API key in Streamlit's "Secrets" (Settings > Secrets):
#   GOOGLE_API_KEY = "your-key-here"
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
elif not os.environ.get("GOOGLE_API_KEY"):
    st.warning(
        "No GOOGLE_API_KEY found. Add it under Settings > Secrets in "
        "Streamlit Community Cloud, or set it as an environment variable."
    )

# --- Session state -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "runner" not in st.session_state:
    st.session_state.runner = get_runner()
    st.session_state.user_id = "guest_user"
    st.session_state.session_id = "guest_session"


async def create_session_if_needed():
    runner = st.session_state.runner
    try:
        await runner.session_service.create_session(
            app_name="ai_barista_app",
            user_id=st.session_state.user_id,
            session_id=st.session_state.session_id,
        )
    except Exception:
        # Session may already exist — that's fine.
        pass


async def get_agent_response(user_text: str) -> str:
    runner = st.session_state.runner
    await create_session_if_needed()

    content = types.Content(role="user", parts=[types.Part(text=user_text)])
    final_response = ""

    async for event in runner.run_async(
        user_id=st.session_state.user_id,
        session_id=st.session_state.session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    return final_response or "Sorry, I couldn't come up with a response."


# --- Render chat history ---------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input --------------------------------------------------------
if prompt := st.chat_input("What can I get for you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Brewing a response..."):
            reply = asyncio.run(get_agent_response(prompt))
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
