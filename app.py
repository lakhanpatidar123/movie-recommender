import streamlit as st
import pickle
import pandas as pd
import base64
import os
import gdown   # ✅ NEW

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------------------
# BACKGROUND
# -------------------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background-color: rgba(0, 0, 0, 0.45);
        padding: 2rem;
        border-radius: 15px;
    }}

    .main-title {{
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: #E50914;
        text-shadow: 2px 2px 6px black;
    }}

    .sub-title {{
        text-align: center;
        color: #ffffff;
        margin-bottom: 20px;
        text-shadow: 1px 1px 4px black;
    }}

    .stButton>button {{
        background-color: #E50914;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        border: none;
    }}

    label {{
        color: white !important;
        font-weight: 600;
        text-shadow: 1px 1px 4px black;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("image/bk.png")

# -------------------------------
# DOWNLOAD FILES (FIXED)
# -------------------------------
def download_file(file_id, filename):
    if not os.path.exists(filename):
        st.write(f"Downloading {filename}...")
        gdown.download(id=file_id, output=filename, quiet=False)

# ✅ YOUR FILE IDs
movies_id = "1xkSL6vkk3XpgUYCunvcVruiXrZzepEKz"
similarity_id = "1aeHUgSh_NcOxb1QnHdJLvoqaMkLDz8zT"

download_file(movies_id, "movies.pkl")
download_file(similarity_id, "similarity.pkl")

# -------------------------------
# LOAD DATA
# -------------------------------
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# -------------------------------
# POSTER FUNCTION
# -------------------------------
def fetch_poster(path):
    if pd.isna(path) or path == "":
        return "https://via.placeholder.com/200x300?text=No+Image"
    return "https://image.tmdb.org/t/p/w500/" + path


# -------------------------------
# RECOMMEND FUNCTIONS
# -------------------------------
def recommend_movie(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:11]

    return movies.iloc[[i[0] for i in movie_list]]


def recommend_genre(genre):
    return movies[
        movies['genres'].str.contains(genre, case=False, na=False)
    ].head(10)


def recommend_language(language):
    return movies[
        movies['spoken_languages'].str.contains(language, case=False, na=False)
    ].head(10)


# -------------------------------
# HEADER
# -------------------------------
st.markdown('<div class="main-title">🎬 MOVIE RECOMMENDER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Find movies based on your taste</div>', unsafe_allow_html=True)

# -------------------------------
# OPTION
# -------------------------------
st.markdown("<h3 style='text-align:center;'>Choose Recommendation Type</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    option = st.radio(
        "",
        ["🎬 Movie Based", "🎭 Genre Based", "🌐 Language Based"],
        horizontal=True
    )

# -------------------------------
# INPUTS
# -------------------------------
if option == "🎬 Movie Based":
    selected_movie = st.selectbox("Select Movie", movies['title'].values)

elif option == "🎭 Genre Based":
    genre = st.selectbox("Select Genre",
        ["Action", "Comedy", "Drama", "Romance", "Thriller"]
    )

elif option == "🌐 Language Based":
    langs = set()
    for x in movies['spoken_languages']:
        for l in x.split(','):
            langs.add(l.strip())

    language = st.selectbox("Select Language", sorted(langs))

# -------------------------------
# BUTTON
# -------------------------------
if st.button("🎥 Recommend"):

    st.markdown("<h3 style='color:white;'>Recommended Movies</h3>", unsafe_allow_html=True)

    cols = st.columns(5)

    if option == "🎬 Movie Based":
        df = recommend_movie(selected_movie)

    elif option == "🎭 Genre Based":
        df = recommend_genre(genre)

    elif option == "🌐 Language Based":
        df = recommend_language(language)

    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 5]:
            st.image(fetch_poster(row['poster_path']), use_container_width=True)
            st.markdown(
                f"<div style='text-align:center; font-weight:600; color:white;'>{row['title']}</div>",
                unsafe_allow_html=True
            )

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
<hr style='border:1px solid #444;'>
<p style='color:white; text-align:center;'>
This system uses <b>content-based filtering</b>.
</p>
""", unsafe_allow_html=True)