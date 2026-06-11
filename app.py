import streamlit as st
import pandas as pd
import psycopg2

import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from your local .env file

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
# 1. Database Connection Setup (Replace with your actual values)

# Streamlit automatically looks into its cloud vault first
import streamlit as st

# 1. This checks your local .streamlit/secrets.toml OR your Streamlit Cloud secrets vault.
# 2. If it can't find them, it falls back to your real AWS RDS endpoint strings.
DB_HOST = st.secrets.get("DB_HOST", os.environ.get("DB_HOST"))
DB_NAME = st.secrets.get("DB_NAME", "postgres")
DB_USER = st.secrets.get("DB_USER", "postgres")
DB_PASS = st.secrets.get("DB_PASSWORD", os.environ.get("DB_PASS"))

def load_data():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    query = "SELECT title, url, published_at, sentiment_score, category FROM news_sentiment ORDER BY published_at DESC;"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Convert database strings into real Indian Standard Time (IST)
    if not df.empty:
        # 1. Ensure Pandas reads it as a datetime object
        df['published_at'] = pd.to_datetime(df['published_at'])
        
        # 2. Localize to UTC and shift forward 5.5 hours to Asia/Kolkata
        df['published_at'] = df['published_at'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
        
        # 3. Format it beautifully back to a clean text string for your table
        df['published_at'] = df['published_at'].dt.strftime('%Y-%m-%d %I:%M %p')
        
    return df

st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")
st.title("📊 Real-Time News Sentiment Analyzer")

# Helper function to generate color intensity based on the decimal score
def color_sentiment_intensity(val):
    try:
        val = float(val)
    except:
        return ''
        
    # Positive Sentiment (Shades of Green)
    if val > 0.05:
        alpha = min(abs(val), 1.0) * 0.6 + 0.1 # Dynamic transparency based on intensity
        return f'background-color: rgba(40, 167, 69, {alpha:.2f}); color: white; font-weight: bold;'
    # Negative Sentiment (Shades of Red)
    elif val < -0.05:
        alpha = min(abs(val), 1.0) * 0.6 + 0.1 # Dynamic transparency based on intensity
        return f'background-color: rgba(220, 53, 69, {alpha:.2f}); color: white; font-weight: bold;'
    # Neutral Sentiment (Grey)
    else:
        return 'background-color: rgba(108, 117, 125, 0.2); color: #6c757d;'

try:
    df = load_data()
    
    if 'category' in df.columns:
        df['category'] = df['category'].fillna('business')
    else:
        df['category'] = 'business'

    # 2. Sidebar Filter Implementation
    st.sidebar.header("Filter & Refine Controls")
    available_categories = ['All'] + list(df['category'].unique())
    selected_cat = st.sidebar.selectbox("Choose News Category", available_categories)
    hide_neutral = st.sidebar.checkbox("Hide Neutral News (Filter noise)", value=False)

    if selected_cat != 'All':
        df = df[df['category'] == selected_cat]
        
    if hide_neutral:
        df = df[(df['sentiment_score'] > 0.05) | (df['sentiment_score'] < -0.05)]

    # 3. Metric Calculations (Ensuring 2-decimal precision)
    total_articles = len(df)
    avg_sentiment = df['sentiment_score'].mean() if total_articles > 0 else 0.0

    if avg_sentiment > 0.05:
        status_label = "Positive 📈"
        color = "normal"
    elif avg_sentiment < -0.05:
        status_label = "- Negative 📉"
        color = "normal"
    else:
        status_label = "Neutral 😐"
        color = "off"

    col1, col2 = st.columns(2)
    col1.metric("Total Articles Processed", total_articles)
    
    # Value formatted strictly to 2 decimal spots
    col2.metric(
        label="Average Category Sentiment", 
        value=f"{avg_sentiment:.2f}", 
        delta=status_label, 
        delta_color=color
    )

    # 4. Visualizations
    st.subheader(f"Sentiment Analysis Breakdown ({selected_cat.capitalize()})")
    
    if total_articles > 0:
        df_chart = df.copy()
        df_chart['published_at'] = pd.to_datetime(df_chart['published_at'])
        
        st.scatter_chart(
            data=df_chart, 
            x='published_at', 
            y='sentiment_score',
            color='category',
            use_container_width=True
        )
        
        # 5. Live Data Stream with Intensity Colors and Decimal Formatting
        st.subheader("Live Data Stream")
        
        # Select and organize columns
        display_df = df[['published_at', 'category', 'title', 'sentiment_score', 'url']].copy()
        
        # Apply style matrix
        styled_df = (display_df.style
                     .map(color_sentiment_intensity, subset=['sentiment_score']) # Apply background color intensity
                     .format({'sentiment_score': '{:.2f}'})) # Force decimal point visibility
                     
        # We pass a column_config to force the url column into a clickable link
        st.dataframe(
            styled_df, 
            use_container_width=True,
            column_config={
                "url": st.column_config.LinkColumn("Article Link")
            }
        )
    else:
        st.warning("No articles found for the selected filters.")

except Exception as e:
    st.error(f"Error loading dashboard: {str(e)}")