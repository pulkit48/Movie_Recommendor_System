import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
sim = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pd.DataFrame(sim)


# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=52a452cd9edad23c86c4c91193e6ccdc&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(id))
    return recommended_movies, recommended_movies_posters


# Streamlit app
def main():
    st.title('Movie Recommender System')

    st.header('Recommendations')
    selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

    if st.button('Show Recommendation'):
        names, posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0], use_column_width=True)
        with col2:
            st.text(names[1])
            st.image(posters[1], use_column_width=True)
        with col3:
            st.text(names[2])
            st.image(posters[2], use_column_width=True)
        with col4:
            st.text(names[3])
            st.image(posters[3], use_column_width=True)
        with col5:
            st.text(names[4])
            st.image(posters[4], use_column_width=True)


# Run the app
if __name__ == '__main__':
    main()
