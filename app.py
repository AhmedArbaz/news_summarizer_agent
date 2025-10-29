import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# Safe access to Streamlit secrets (only if available)
def get_secret(key: str):
    try:
        return st.secrets[key]
    except Exception:
        return None

# Load API keys safely (works both locally & on Streamlit Cloud)
NEWS_API_KEY = get_secret("NEWS_API_KEY") or os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Validate API keys
if not NEWS_API_KEY or not GOOGLE_API_KEY:
    st.error("❌ Missing API keys! Please add them to `.env` (for local use) or Streamlit Secrets (for cloud).")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# ----------------------------
# Streamlit App UI
# ----------------------------
st.set_page_config(page_title="🧠 News Summarizer Agent", page_icon="🗞️", layout="centered")

st.title("🧠 News Summarizer Agent")
st.caption("Built with Streamlit + Gemini AI + NewsAPI")

st.write("Enter a **keyword or topic** below to fetch and summarize the latest news.")

query = st.text_input("🔍 Search for News:", placeholder="e.g., Artificial Intelligence, Climate Change, Sports...")

if st.button("Fetch & Summarize"):
    if not query.strip():
        st.warning("⚠️ Please enter a topic to search.")
    else:
        with st.spinner("Fetching latest news..."):
            # Fetch top headlines from NewsAPI
            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
            response = requests.get(url)
            
            if response.status_code != 200:
                st.error("Failed to fetch news. Please check your API key or try again later.")
                st.stop()

            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                st.warning("No news found for your query.")
                st.stop()

            # Combine top 5 articles
            combined_text = ""
            for article in articles[:5]:
                combined_text += f"Title: {article['title']}\nDescription: {article.get('description', '')}\n\n"

        st.success("✅ News fetched successfully!")

        with st.spinner("Summarizing using Gemini AI..."):
            try:
                # ✅ Use updated model name
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"Summarize the following news articles into key insights:\n\n{combined_text}"
                summary = model.generate_content(prompt)

                st.subheader("🧾 Summary")
                st.write(summary.text)

            except Exception as e:
                st.error(f"Error generating summary: {e}")

        with st.expander("📰 View Raw Articles"):
            for i, article in enumerate(articles[:5], 1):
                st.markdown(f"**{i}. {article['title']}**")
                st.markdown(f"_{article.get('source', {}).get('name', 'Unknown Source')}_")
                st.write(article.get("description", "No description available"))
                st.markdown(f"[Read Full Article]({article['url']})")
                st.markdown("---")

st.markdown("---")
st.caption("Created by Ahmad Hassan • Powered by Streamlit & Gemini AI 🚀")
