import streamlit as st
import pickle
import pandas as pd
import requests
# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=API_KEY&language=en-US"
        response = requests.get(url)
        data = response.json()
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/original/" + data['poster_path']
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Image"
    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/300x450.png?text=Error"

# Recommendation function
def recommend(movie):
    mov_ind = movies[movies['title'] == movie].index[0]
    distances = similarity[mov_ind]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies =[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

# Streamlit UI
st.title("Movie Recommender System")

selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selected_movie)
    st.write("Recommended Movies:")
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

