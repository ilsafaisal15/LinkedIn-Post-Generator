import streamlit as st
import requests
import os

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="🚀"
)

st.title("🚀 AI LinkedIn Post Generator (Groq Powered)")
st.write("Generate high-engagement LinkedIn posts instantly.")

# ------------------------
# Load Groq API Key from Secrets
# ------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Please add GROQ_API_KEY in Hugging Face Space Secrets.")
    st.stop()

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------------
# User Inputs
# ------------------------
topic = st.text_input("Enter Topic")

tone = st.selectbox(
    "Select Tone",
    ["Professional", "Motivational", "Storytelling", "Bold", "Friendly"]
)

generate = st.button("Generate Post")

# ------------------------
# Generate Content
# ------------------------
if generate:
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating your post..."):

            prompt = f"""
Write a high-engagement LinkedIn post about "{topic}".

Tone: {tone}

Requirements:
- Strong hook in first line
- Short readable paragraphs
- Add spacing for clarity
- End with an engaging question
- Include 3 relevant hashtags
"""

            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are a LinkedIn content expert."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }

            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                st.success("✅ Post Generated!")
                st.text_area("Your LinkedIn Post", content, height=400)
            else:
                st.error("Error generating content.")
                st.write(response.text)
