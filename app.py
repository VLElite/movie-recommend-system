import pickle
import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
from PIL import Image
from io import BytesIO

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------
# Load CSS
# -------------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -------------------------------
# OMDb API Key
# -------------------------------
API_KEY = "8c29a9fd"

# -------------------------------
# Default Poster
# -------------------------------
DEFAULT_POSTER = "https://upload.wikimedia.org/wikipedia/en/7/7a/1917poster.jpg"

# -------------------------------
# Fetch Movie Details
# -------------------------------
def fetch_movie_details(movie_name):

    try:

        movie_name = quote(movie_name)

        url = f"https://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

        response = requests.get(url, timeout=10)

        data = response.json()

        poster = data.get("Poster", DEFAULT_POSTER)

        if poster == "N/A":
            poster = DEFAULT_POSTER

        # convert http to https
        if poster.startswith("http://"):
            poster = poster.replace("http://", "https://")

        return {
            "poster": poster,
            "rating": data.get("imdbRating", "N/A"),
            "genre": data.get("Genre", "N/A"),
            "plot": data.get("Plot", "No description available"),
            "year": data.get("Year", "N/A")
        }

    except Exception as e:

        print(e)

        return {
            "poster": DEFAULT_POSTER,
            "rating": "N/A",
            "genre": "N/A",
            "plot": "No description available",
            "year": "N/A"
        }


# -------------------------------
# Recommendation Function
# -------------------------------
def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:

        movie_title = movies.iloc[i[0]].title

        movie_details = fetch_movie_details(movie_title)

        recommended_movies.append({
            "title": movie_title,
            "poster": movie_details["poster"],
            "rating": movie_details["rating"],
            "genre": movie_details["genre"],
            "year": movie_details["year"],
            "plot": movie_details["plot"]
        })

    return recommended_movies


# -------------------------------
# Load Pickle Files
# -------------------------------
with open("movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# -------------------------------
# Header Section
# -------------------------------
st.markdown(
    "<h1>🎬 AI Movie Recommender</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Discover movies you'll love 🍿</div>",
    unsafe_allow_html=True
)

st.write("")

# -------------------------------
# Movie Selection
# -------------------------------
selected_movie_name = st.selectbox(
    "🎥 Choose Your Favorite Movie",
    movies["title"].values
)

# -------------------------------
# Recommendation Button
# -------------------------------
if st.button("Recommend Movies"):

    with st.spinner("Finding awesome movies for you... 🍿"):

        recommended_movies = recommend(selected_movie_name)

    st.subheader("🔥 Top Recommended Movies")

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        movie = recommended_movies[idx]

        with col:

            st.markdown(
                "<div class='movie-card'>",
                unsafe_allow_html=True
            )

            # -------------------------------
            # Poster Section
            # -------------------------------
            try:

                poster_url = movie["poster"]

                headers = {
                    "User-Agent": "Mozilla/5.0"
                }

                response = requests.get(
                    poster_url,
                    headers=headers,
                    timeout=10
                )

                image = Image.open(
                    BytesIO(response.content)
                )

                st.image(
                    image,
                    use_container_width=True
                )

            except Exception as e:

                st.write(e)

                st.image(
                    DEFAULT_POSTER,
                    use_container_width=True
                )

            # -------------------------------
            # Movie Title
            # -------------------------------
            st.markdown(
                f"""
                <div class='movie-title'>
                    {movie["title"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------
            # IMDb Rating
            # -------------------------------
            st.markdown(
                f"""
                <p style='color:#FFD700;
                          text-align:center;
                          font-weight:bold;'>
                    ⭐ IMDb: {movie["rating"]}
                </p>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------
            # Genre
            # -------------------------------
            st.markdown(
                f"""
                <p style='color:#cbd5e1;
                          text-align:center;
                          font-size:14px;'>
                    🎭 {movie["genre"]}
                </p>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------
            # Release Year
            # -------------------------------
            st.markdown(
                f"""
                <p style='color:#94a3b8;
                          font-size:13px;
                          text-align:center;'>
                    📅 {movie["year"]}
                </p>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )