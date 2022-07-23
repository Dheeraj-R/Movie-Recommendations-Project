import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies_model.pkl', 'rb'))
moviesA = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendations')
option = st.selectbox("Type or select movie", moviesA)


def fetch_the_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0f23f016d6e9999296d536c85b15d674&language=en-US')
    final_data = response.json()
    final_path = "https://image.tmdb.org/t/p/w185/" + final_data['poster_path']
    return final_path


def recommend(name):
    movie_index = movies_list[movies_list['title'] == name].index[0]
    distances = similarity[movie_index]
    rec_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_poster = []
    for i in rec_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_poster.append(fetch_the_poster(movie_id))  # poster from tmdb api

    return recommended_movies, recommended_poster


if st.button('Recommend'):
    rec, poster = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    col_list = [col1, col2, col3, col4, col5]
    count = 0

    while count != 5:
        with col_list[count]:
            # st.text(rec[count])
            st.image(poster[count], caption=rec[count], use_column_width='always')
            count += 1



