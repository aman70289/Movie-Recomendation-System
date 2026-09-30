import streamlit as st
import pickle
import requests


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


# =========================================================
# TMDB CONFIG
# =========================================================

API_KEY = st.secrets["TMDB_API_KEY"]

TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# =========================================================
# FETCH POSTER FROM TMDB
# =========================================================

@st.cache_data
def fetch_poster(movie_id):

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return IMAGE_BASE_URL + poster_path

        return None

    except requests.exceptions.RequestException as e:

        st.error(f"TMDB API Error: {e}")
        return None

    except Exception as e:

        st.error(f"Error: {e}")
        return None


# =========================================================
# RECOMMEND MOVIES
# =========================================================

def recommend(movie):

    # Find selected movie index
    movie_index = movies[movies["title"] == movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Sort according to similarity
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        # ---------------------------------------------
        # Movie title
        # ---------------------------------------------

        movie_title = movies.iloc[i[0]]["title"]

        # ---------------------------------------------
        # Get Movie ID
        # ---------------------------------------------

        if "movie_id" in movies.columns:

            movie_id = movies.iloc[i[0]]["movie_id"]

        elif "id" in movies.columns:

            movie_id = movies.iloc[i[0]]["id"]

        else:

            movie_id = None

        # ---------------------------------------------
        # Add movie title
        # ---------------------------------------------

        recommended_movies.append(movie_title)

        # ---------------------------------------------
        # Fetch poster
        # ---------------------------------------------

        if movie_id is not None:

            poster = fetch_poster(movie_id)

        else:

            poster = None

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# =========================================================
# STREAMLIT UI
# =========================================================

st.title("🎬 Movie Recommendation System")

st.write(
    "Select a movie and get 5 similar movie recommendations."
)


# =========================================================
# MOVIE SELECTION
# =========================================================

selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies["title"].values
)


# =========================================================
# RECOMMEND BUTTON
# =========================================================

if st.button("🍿 Recommend Movies"):

    with st.spinner("Finding recommendations..."):

        names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")


    # =====================================================
    # DISPLAY 5 MOVIES
    # =====================================================

    cols = st.columns(5)

    for i in range(len(names)):

        with cols[i]:

            # Movie poster
            if posters[i]:

                st.image(
                    posters[i],
                    use_container_width=True
                )

            else:

                st.info("Poster not available")

            # Movie title
            st.markdown(
                f"### {names[i]}"
            )