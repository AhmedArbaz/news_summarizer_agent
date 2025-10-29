import streamlit as st
import requests
import google.generativeai as genai


NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="🧠 AI News Summarizer",
    page_icon="📰",
    layout="wide",
)


st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
    .news-card {
        background-color: #1a1d25;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(255,255,255,0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .news-card:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(255,255,255,0.1);
    }
    .news-img {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .title {
        color: #a5d8ff;
        font-weight: bold;
    }
    a {
        color: #89c2d9;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)


st.title("📰 AI News Summarizer")
st.caption("Summarize the latest world news using Google Gemini AI ✨")

# ==========================
# 🔍 User Input
# ==========================
topic = st.text_input("Enter a topic (e.g., AI, Sports, Business):")

if st.button("Summarize News"):
    if not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        st.info(f"Fetching the latest **{topic}** news...")

        # Fetch news from NewsAPI
        url = f"https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("articles"):
            articles = data["articles"][:5]

            for article in articles:
                title = article.get("title")
                description = article.get("description", "")
                image = article.get("urlToImage")
                link = article.get("url")

                content = f"Title: {title}\nDescription: {description}"

                # Summarize using Gemini AI
                try:
                    prompt = f"Summarize this news article in 3-4 short sentences:\n\n{content}"
                    summary = model.generate_content(prompt).text
                except Exception:
                    summary = "AI summary unavailable at the moment."

                # Display result
                st.markdown('<div class="news-card">', unsafe_allow_html=True)
                if image:
                    st.image(image, use_container_width=True, caption=title)
                st.markdown(f"<h3 class='title'>{title}</h3>", unsafe_allow_html=True)
                st.write(summary)
                st.markdown(f"[📰 Read full article]({link})")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("No news found. Try another topic.")
