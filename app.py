import streamlit as st
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API keys from .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Streamlit UI
st.set_page_config(page_title="📰 AI News Summarizer", page_icon="🧠", layout="wide")

st.title("🧠 AI News Summarizer")
st.write("Fetch and summarize the latest news using AI 🤖")

# Input field for topic
topic = st.text_input("Enter a topic (e.g., Technology, Sports, AI):", "")

if st.button("Summarize News"):
    if not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        st.info(f"Fetching latest news about **{topic}**...")

        # Fetch news from NewsAPI
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("articles"):
            articles = data["articles"][:5]  # limit to 5 latest articles
            summaries = []

            for article in articles:
                title = article.get("title")
                description = article.get("description", "No description available.")
                content = f"Title: {title}\nDescription: {description}"

                # Summarize using Gemini AI
                prompt = f"Summarize this news article in 3-4 concise sentences:\n\n{content}"
                ai_summary = model.generate_content(prompt).text

                summaries.append({
                    "title": title,
                    "summary": ai_summary,
                    "url": article.get("url")
                })

            st.success("✅ News summarized successfully!")

            # Display results
            for s in summaries:
                st.subheader(s["title"])
                st.write(s["summary"])
                st.markdown(f"[Read full article here]({s['url']})")
                st.divider()

        else:
            st.error("No news found. Try a different topic.")
