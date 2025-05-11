import pickle
import streamlit as st
import requests
# TMDb API poster fetch
st.markdown("[Download similarity.pkl from Google Drive](https://drive.google.com/file/d/1xK9W9xMTZ3HQ-fEsin9lIsJwlUdnrO-Q/view?usp=sharing
)")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6c509083a1c98f861af9f8faa893d8f2&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise Exception("API Error")
        data = response.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image"
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        print(f"Poster fetch failed: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('🎬   Movie Recommender System')

# Load model and data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations
if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie)
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i])
