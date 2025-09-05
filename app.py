import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"


st.title("🎥 YouTube Transcript Bot")


youtube_url = st.text_input("Enter YouTube video link:")

if st.button("Generate Transcript"):
    if youtube_url:
        with st.spinner("Processing video... this may take a while ⏳"):
            res = requests.post(f"{FASTAPI_URL}/transcribe",
                                json={"url": youtube_url})
            if res.status_code == 200:
                data = res.json()
                st.success("Transcript generated!")
                st.session_state["video_id"] = data["video_id"]
            else:
                st.error("Failed to generate transcript")

if "video_id" in st.session_state:
    st.subheader("Ask questions about the transcript")
    question = st.text_input("Your question:")

    if st.button("Ask"):
        if question:
            res = requests.post(
                f"{FASTAPI_URL}/ask", json={"video_id": st.session_state['video_id'], "question": question})
            if res.status_code == 200:
                data = res.json()
                st.write("Answer:", data["answer"])
            else:
                st.error("Failed to get answer")
