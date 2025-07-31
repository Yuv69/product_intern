import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from collections import Counter
import re

# Load your final dataframe
df = pd.read_csv("leapscholar_mentions.csv")  # We'll save it below

st.set_page_config(page_title="LeapScholar Brand Monitor", layout="wide")

st.title("📊 LeapScholar Brand Perception Monitor")
st.markdown("Tracks recent mentions across Reddit and Google News.")

# Show summary stats
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Mentions", len(df))
with col2:
    st.metric("Sources", df['Source'].nunique())

# Sentiment distribution
st.subheader("📈 Sentiment Distribution")
sentiment_counts = df['Sentiment'].value_counts()
st.bar_chart(sentiment_counts)

# WordCloud
st.subheader("☁️ Word Cloud")
text = " ".join(df['Content'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=set()).generate(text)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Keyword table
st.subheader("🔍 Top Keywords")
def extract_keywords(text_series):
    all_words = []
    for text in text_series:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', str(text).lower())
        all_words.extend([word for word in words])
    return Counter(all_words).most_common(10)

keywords = extract_keywords(df['Content'])
keywords_df = pd.DataFrame(keywords, columns=["Keyword", "Frequency"])
st.dataframe(keywords_df)

# Raw data
st.subheader("📄 Raw Mentions")
st.dataframe(df[['Date', 'Content', 'Source', 'Sentiment']])
