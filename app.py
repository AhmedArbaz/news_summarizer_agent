import streamlit as st
import requests
import google.generativeai as genai

# ✅ Load secrets from Streamlit Cloud (or local .streamlit/secrets.toml)
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="AI News Summarizer", page_icon="📰", layout="wide")

st.title("📰 AI News Summarizer")
st.write("Fetch and summarize the latest news articles using Google Gemini.")

# --- User Input ---
query = st.text_input("Enter a topic (e.g. AI, Technology, Sports):")

if st.button("Get News"):
    if not query:
        st.warning("⚠️ Please enter a topic to search for news.")
    else:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                st.info("No news articles found for this topic.")
            else:
                for i, article in enumerate(articles[:5], 1):
                    st.subheader(f"{i}. {article['title']}")
                    st.write(article['description'] or "")
                    st.write(f"[Read more]({article['url']})")

                    # --- AI Summary ---
                    prompt = f"Summarize this news article in 3 sentences:\n\n{article['title']}\n{article['description']}"
                    try:
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        summary = model.generate_content(prompt)
                        st.success(summary.text.strip())
                    except Exception as e:
                        st.error(f"AI summary failed: {e}")
        else:
            st.error(f"News API error: {response.status_code}")
