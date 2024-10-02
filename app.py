import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime
import os

# Get the YouTube API key from the environment variable
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    st.error("YouTube API key not found. Please set the YOUTUBE_API_KEY environment variable.")
    st.stop()

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_all_comments(video_id: str):
    try:
        comments = []
        nextPageToken = None
        while True:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken,
                order='time'
            ).execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })

            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break

        return comments
    except Exception as e:
        return f"An error occurred while fetching comments: {str(e)}"

st.set_page_config(layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        color: #333;
        font-family: 'Roboto', sans-serif;
        line-height: 1.6;
        background-color: #f0f2f5;
    }
    .main {
        max-width: 800px;
        margin: 0 auto;
        background-color: white;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .comments-container {
        max-width: 800px;
        margin: 2rem auto;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        background-color: #f9f9f9;
    }
    .comments-scrollable {
        max-height: 500px;
        overflow-y: auto;
    }
    .comment {
        background-color: #ffffff;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .comment-author {
        font-weight: bold;
        color: #2c3e50;
    }
    .comment-date {
        font-size: 0.8em;
        color: #7f8c8d;
    }
    .comment-text {
        margin-top: 5px;
    }
    .comment-likes {
        font-size: 0.9em;
        color: #3498db;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("YouTube Comments Extractor")

video_id = st.text_input("Enter YouTube Video ID")

if st.button("Extract Comments"):
    if video_id:
        with st.spinner("Extracting comments..."):
            comments = get_all_comments(video_id)
            if isinstance(comments, list):
                st.markdown("<div class='comments-container'>", unsafe_allow_html=True)
                st.markdown("<h2>Comments</h2>", unsafe_allow_html=True)
                st.markdown("<div class='comments-scrollable'>", unsafe_allow_html=True)
                for comment in comments:
                    st.markdown(f"""
<div class="comment">
    <div class="comment-author">{comment['author']}</div>
    <div class="comment-date">{comment['published_at']}</div>
    <div class="comment-text">{comment['text']}</div>
    <div class="comment-likes">👍 {comment['likes']}</div>
</div>
""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error(comments)
    else:
        st.error("Please enter a YouTube Video ID.")
