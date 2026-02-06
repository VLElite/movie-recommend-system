import pickle
import streamlit as st
import pandas as pd
import requests

# -------------------------------
# Fetch Poster Function
# -------------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=Poster+Not+Found"

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path is None:
            return "https://via.placeholder.com/500x750?text=No+Poster"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        return "https://via.placeholder.com/500x750?text=Network+Error"


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
    recommended_movies_posters = []

    for i in movie_list:
        row = movies.iloc[i[0]]

        movie_id = row["id"]   # ✅ FIXED (Correct Column)

        recommended_movies.append(row["title"])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# -------------------------------
# Load Pickle Files
# -------------------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies = pd.DataFrame(movies)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    st.subheader("Top 5 Recommended Movies:")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
