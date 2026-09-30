import streamlit as st
import pickle

# -----------------------------
# Load saved files
# -----------------------------

movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


# -----------------------------
# Recommendation Function
# -----------------------------

def recommend(movie):

    # Movie ka index find karo
    index = movies[movies["title"] == movie].index[0]

    # Selected movie ki similarity
    distances = similarity[index]

    # Similar movies sort karo
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommendation System")

st.write(
    "Select a movie and get 5 movies similar to it."
)

# Movie dropdown
selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

# Recommend button
if st.button("🎯 Recommend Movies"):

    recommendations = recommend(selected_movie)

    st.subheader("Recommended Movies")

    for movie in recommendations:
        st.write("🎬", movie)
 