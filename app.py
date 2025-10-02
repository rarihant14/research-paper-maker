import streamlit as st
import requests

BACKEND_URL = "https://research-backend.onrender.com"


st.set_page_config(page_title="AI Research Paper Maker", layout="wide")
st.title("📄 AI Research Paper Maker")
st.write("Generate structured research papers in plain text.")

topic = st.text_input("🔍 Enter Research Topic")
style = st.selectbox("🖋 Writing Style", ["academic", "casual", "technical"])
words = st.slider("📏 Word Count", 500, 5000, 1500, step=100)

if st.button("🚀 Generate Paper"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Submitting job..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/research/generate", json={
                    "topic": topic,
                    "style": style,
                    "words": words
                })
                if resp.status_code == 200:
                    job_id = resp.json()["job_id"]
                    st.session_state["job_id"] = job_id
                    st.success(f"Job submitted ✅ (ID: {job_id})")
                else:
                    st.error(f"Error: {resp.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

# Check and download
if "job_id" in st.session_state:
    job_id = st.session_state["job_id"]
    if st.button("📊 Check Status"):
        try:
            resp = requests.get(f"{BACKEND_URL}/research/status/{job_id}")
            if resp.status_code == 200:
                job = resp.json()
                st.write(f"**Status:** {job['status']}")
                if job["status"] == "completed":
                    st.success("🎉 Paper ready!")
                    download = requests.get(f"{BACKEND_URL}/research/download/{job_id}")
                    if download.status_code == 200:
                        paper = download.json()["paper"]
                        st.text_area("📄 Generated Research Paper", paper, height=600)
                        st.download_button("💾 Download Paper", data=paper, file_name=f"paper_{job_id}.txt", mime="text/plain")
                elif job["status"] == "failed":
                    st.error("❌ Job failed.")
            else:
                st.error(f"Error fetching status: {resp.text}")
        except Exception as e:
            st.error(f"Error: {e}")
