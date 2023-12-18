import streamlit as st
from openai import OpenAI
import json
import requests
import streamlit_antd_components as sac


my_openai_api_key = st.secrets["OPENAI_API_KEY"]
my_tmdb_api_key = st.secrets["TMDB_API_KEY"]

# Initialize the OpenAI client
client = OpenAI(api_key=my_openai_api_key)

# Set the theme
st.set_page_config(
    page_title="Movie Recommendation AI",
    page_icon="🍿",
    initial_sidebar_state="expanded",
    layout="wide"
)

# Title of the web app
st.title("Movie Recommendation AI")

# User input for movie name
movie_name = st.text_input("What type of movies do you like?")
# ... (your existing code)

if movie_name:
    # Display the movie name
    # Display the recommended movies side by side
    status = st.status(
        f"Getting movie recommendations for ***:orange[***{movie_name}***]***", expanded=True)

    st.subheader("Recommended Movies:")
    # Create columns dynamically based on the number of recommended movies
    cols = st.columns(5)

    with status:
        prev = st.info(
            "Getting movie recommendations for ***:orange[{}]***".format(movie_name), icon="⏳")
        # Get movie recommendations from OpenAI GPT-3
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant designed to help people find movies to watch based on their inputs and preferences. Provide outputs in the form of a json object with a list of 5 recommended movies with key as 'movies'. Each movie should be a dictionary with keys 'title', 'overview', 'release_date', 'imdb_rating'. The value for 'title' should be the movie title, 'overview' should be a short description of the movie, 'release_date' should be the release date of the movie, and 'imdb_rating' should be the IMDB rating of the movie. The movies should be sorted in descending order of IMDB rating."
                    },
                    {"role": "user", "content": movie_name}
                ]
            )
            # Parse the response
            recommended_movies = json.loads(
                response.choices[0].message.content)['movies']

            if not recommended_movies:
                status.update(label="No movie recommendations found for ***:orange[{}]***".format(
                    movie_name), state="error", expanded=False)
                st.error(
                    f" No movie recommendations found for ***:orange[***{movie_name}***]***")
                st.balloons()
                st.stop()

        except Exception as e:
            prev.error("Something went wrong while getting movie recommendations for ***:orange[{}]***".format(
                movie_name), icon="❌")
            status.update(label="Something went wrong while getting movie recommendations for ***:orange[{}]***".format(
                movie_name), state="error", expanded=False)

            st.stop()

        prev.success(
            "Got movie recommendations for ***:orange[{}]***".format(movie_name), icon="✅")

        # Set the fixed height for each row
        fixed_row_height = 150  # You can adjust this value based on your preference
        fixed_h3_height = 80

        # Generate the movie poster image URLs
        for i, movie in enumerate(recommended_movies, start=1):
            # Get the movie poster URL from TMDB API

            prev = st.info(
                "Getting movie poster for ***:orange[{}]***".format(movie['title']), icon="⏳")
            status.update(
                label="Getting movie poster for ***:orange[{}]***".format(movie['title']))

            try:
                url = f"https://api.themoviedb.org/3/search/movie?api_key={my_tmdb_api_key}&query={movie['title']}"
                response = requests.get(url)
                data = response.json()

                if 'results' in data and data['results']:
                    first_result = data['results'][0]
                    poster_path = first_result.get('poster_path')
                
                    if poster_path:
                        movie["poster_url"] = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    else:
                        # Raise an exception if poster path is not found
                        raise Exception("Poster path not available in the TMDB API response.")
                else:
                    # Raise an exception if 'results' key is not present or 'results' list is empty
                    raise Exception("'results' key is missing or empty in the TMDB API response.")

            except Exception as e:
                # Handle the exception and set a default poster URL
                movie["poster_url"] = "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg"
                st.warning("Failed to get movie poster for ***:orange[{}]***".format(
                    movie['title']), icon="⚠️")

            try:
                with cols[i-1]:
                    # Display movie details
                    st.image(movie["poster_url"])

                    st.markdown(
                        f"<h3 style='height: {fixed_h3_height}px; overflow: hidden;'>{movie['title']}</h3>", unsafe_allow_html=True)

                    st.markdown(
                        f"<div style='height: {fixed_row_height}px; overflow: hidden;'>{movie['overview']}</div>", unsafe_allow_html=True)

                    st.write("")
                    st.write("***Release Date:***", movie["release_date"])

                    movie["imdb_rating"] = float(movie["imdb_rating"])

                    st.write("***IMDB Rating:***", movie["imdb_rating"])

                    # Make rating divisible by 0.5
                    movie["rating"] = round(movie["imdb_rating"] * 2) / 2

                    # Use the `sac.rate` method to display a star rating
                    sac.rate(label=None,
                             value=movie["rating"], half=True, readonly=True, count=10, key=movie["title"], color='#2980b9')
            except Exception as e:
                st.warning("Something went wrong while displaying movie details for ***:orange[{}]***".format(
                    movie['title']) + str(e), icon="❌")
            prev.success(
                "Got movie poster for ***:orange[{}]***".format(movie['title']), icon="✅")
        status.update(
            label=f"Got movie recommendations for ***:orange[***{movie_name}***]***", state="complete", expanded=False)
    st.balloons()
else:
    # Display a message if no movie name is entered
    st.info("Enter text about any movie here to get recommendations.", icon="👆")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.balloons()


# Footer section with social media links and "Made with ❤️ by me"
footer = """
    <style>
        block-container {
            padding: 0;
        }
        footer {
            background-color: #2C3E50;
            padding: 0;
            text-align: center;
            position: sticky;
            bottom: 0;
        }
        a {
            color: white;
            text-decoration: none;
            margin: 0 20px;
            hover:none;
        }
        hr {
            border-color: white;
        }
    </style>
    <footer>
        <h3 style="color: white;">Connect with Me</h3>
        <a href="https://www.instagram.com/theshahnawaaz" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 102 102" id="instagram"><defs><radialGradient id="a" cx="6.601" cy="99.766" r="129.502" gradientUnits="userSpaceOnUse"><stop offset=".09" stop-color="#fa8f21"></stop><stop offset=".78" stop-color="#d82d7e"></stop></radialGradient><radialGradient id="b" cx="70.652" cy="96.49" r="113.963" gradientUnits="userSpaceOnUse"><stop offset=".64" stop-color="#8c3aaa" stop-opacity="0"></stop><stop offset="1" stop-color="#8c3aaa"></stop></radialGradient></defs><path fill="url(#a)" d="M25.865,101.639A34.341,34.341,0,0,1,14.312,99.5a19.329,19.329,0,0,1-7.154-4.653A19.181,19.181,0,0,1,2.5,87.694,34.341,34.341,0,0,1,.364,76.142C.061,69.584,0,67.617,0,51s.067-18.577.361-25.14A34.534,34.534,0,0,1,2.5,14.312,19.4,19.4,0,0,1,7.154,7.154,19.206,19.206,0,0,1,14.309,2.5,34.341,34.341,0,0,1,25.862.361C32.422.061,34.392,0,51,0s18.577.067,25.14.361A34.534,34.534,0,0,1,87.691,2.5a19.254,19.254,0,0,1,7.154,4.653A19.267,19.267,0,0,1,99.5,14.309a34.341,34.341,0,0,1,2.14,11.553c.3,6.563.361,8.528.361,25.14s-.061,18.577-.361,25.14A34.5,34.5,0,0,1,99.5,87.694,20.6,20.6,0,0,1,87.691,99.5a34.342,34.342,0,0,1-11.553,2.14c-6.557.3-8.528.361-25.14.361s-18.577-.058-25.134-.361" data-name="Path 16"></path><path fill="url(#b)" d="M25.865,101.639A34.341,34.341,0,0,1,14.312,99.5a19.329,19.329,0,0,1-7.154-4.653A19.181,19.181,0,0,1,2.5,87.694,34.341,34.341,0,0,1,.364,76.142C.061,69.584,0,67.617,0,51s.067-18.577.361-25.14A34.534,34.534,0,0,1,2.5,14.312,19.4,19.4,0,0,1,7.154,7.154,19.206,19.206,0,0,1,14.309,2.5,34.341,34.341,0,0,1,25.862.361C32.422.061,34.392,0,51,0s18.577.067,25.14.361A34.534,34.534,0,0,1,87.691,2.5a19.254,19.254,0,0,1,7.154,4.653A19.267,19.267,0,0,1,99.5,14.309a34.341,34.341,0,0,1,2.14,11.553c.3,6.563.361,8.528.361,25.14s-.061,18.577-.361,25.14A34.5,34.5,0,0,1,99.5,87.694,20.6,20.6,0,0,1,87.691,99.5a34.342,34.342,0,0,1-11.553,2.14c-6.557.3-8.528.361-25.14.361s-18.577-.058-25.134-.361" data-name="Path 17"></path><path fill="#fff" d="M461.114,477.413a12.631,12.631,0,1,1,12.629,12.632,12.631,12.631,0,0,1-12.629-12.632m-6.829,0a19.458,19.458,0,1,0,19.458-19.458,19.457,19.457,0,0,0-19.458,19.458m35.139-20.229a4.547,4.547,0,1,0,4.549-4.545h0a4.549,4.549,0,0,0-4.547,4.545m-30.99,51.074a20.943,20.943,0,0,1-7.037-1.3,12.547,12.547,0,0,1-7.193-7.19,20.923,20.923,0,0,1-1.3-7.037c-.184-3.994-.22-5.194-.22-15.313s.04-11.316.22-15.314a21.082,21.082,0,0,1,1.3-7.037,12.54,12.54,0,0,1,7.193-7.193,20.924,20.924,0,0,1,7.037-1.3c3.994-.184,5.194-.22,15.309-.22s11.316.039,15.314.221a21.082,21.082,0,0,1,7.037,1.3,12.541,12.541,0,0,1,7.193,7.193,20.926,20.926,0,0,1,1.3,7.037c.184,4,.22,5.194.22,15.314s-.037,11.316-.22,15.314a21.023,21.023,0,0,1-1.3,7.037,12.547,12.547,0,0,1-7.193,7.19,20.925,20.925,0,0,1-7.037,1.3c-3.994.184-5.194.22-15.314.22s-11.316-.037-15.309-.22m-.314-68.509a27.786,27.786,0,0,0-9.2,1.76,19.373,19.373,0,0,0-11.083,11.083,27.794,27.794,0,0,0-1.76,9.2c-.187,4.04-.229,5.332-.229,15.623s.043,11.582.229,15.623a27.793,27.793,0,0,0,1.76,9.2,19.374,19.374,0,0,0,11.083,11.083,27.813,27.813,0,0,0,9.2,1.76c4.042.184,5.332.229,15.623.229s11.582-.043,15.623-.229a27.8,27.8,0,0,0,9.2-1.76,19.374,19.374,0,0,0,11.083-11.083,27.716,27.716,0,0,0,1.76-9.2c.184-4.043.226-5.332.226-15.623s-.043-11.582-.226-15.623a27.786,27.786,0,0,0-1.76-9.2,19.379,19.379,0,0,0-11.08-11.083,27.748,27.748,0,0,0-9.2-1.76c-4.041-.185-5.332-.229-15.621-.229s-11.583.043-15.626.229" data-name="Path 18" transform="translate(-422.637 -426.196)"></path></svg>
        </a>
        <a href="https://github.com/TheShahnawaaz/" target="_blank">
           <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="70" height="70" preserveAspectRatio="xMinYMin meet" viewBox="0 0 256 259.3" id="github"><path fill="#9EDCF2" d="M200.9 199.8c0 13.9-32.2 25.1-71.9 25.1s-71.9-11.3-71.9-25.1c0-13.9 32.2-25.1 71.9-25.1s71.9 11.2 71.9 25.1zm0 0"></path><defs><path id="a" d="M98.1 244.8c1.6 7.5 5.5 11.9 9.4 14.5h41.1c5-3.4 10.1-9.8 10.1-21.8v-31s.6-7.7 7.7-10.2c0 0 4.1-2.9-.3-4.5 0 0-19.5-1.6-19.5 14.4v23.6s.8 8.7-3.8 12.3v-29.2s.3-9.3 5.1-12.8c0 0 3.2-5.7-3.8-4.2 0 0-13.4 1.9-14 17.6l-.3 30h-3.2l-.3-30c-.6-15.6-14-17.6-14-17.6-7-1.6-3.8 4.2-3.8 4.2 4.8 3.5 5.1 12.8 5.1 12.8v29.5c-4.6-3.3-3.8-12.6-3.8-12.6v-23.6c0-16-19.5-14.4-19.5-14.4-4.5 1.6-.3 4.5-.3 4.5 7 2.6 7.7 10.2 7.7 10.2v21.7l.4 16.6z"></path></defs><clipPath id="b"><use overflow="visible" xlink:href="#a"></use></clipPath><path fill="#7DBCE7" d="M200.9 199.8c0 13.9-32.2 25.1-71.9 25.1s-71.9-11.3-71.9-25.1c0-13.9 32.2-25.1 71.9-25.1s71.9 11.2 71.9 25.1zm0 0" clip-path="url(#b)"></path><path fill="#9EDCF2" d="M46.9 125.9l-2.1 7.2s-.5 2.6 1.9 3.1c2.6-.1 2.4-2.5 2.2-3.2l-2-7.1zm0 0"></path><path fill="#010101" d="M255.8 95.6l.2-.9c-21.1-4.2-42.7-4.3-55.8-3.7 2.1-7.7 2.8-16.7 2.8-26.6 0-14.3-5.4-25.7-14-34.3 1.5-4.9 3.5-15.8-2-29.7 0 0-9.8-3.1-32.1 11.8-8.7-2.2-18-3.3-27.3-3.3-10.2 0-20.5 1.3-30.2 3.9C74.4-2.9 64.3.3 64.3.3c-6.6 16.5-2.5 28.8-1.3 31.8-7.8 8.4-12.5 19.1-12.5 32.2 0 9.9 1.1 18.8 3.9 26.5-13.2-.5-34-.3-54.4 3.8l.2.9c20.4-4.1 41.4-4.2 54.5-3.7.6 1.6 1.3 3.2 2 4.7-13 .4-35.1 2.1-56.3 8.1l.3.9c21.4-6 43.7-7.6 56.6-8 7.8 14.4 23 23.8 50.2 26.7-3.9 2.6-7.8 7-9.4 14.5-5.3 2.5-21.9 8.7-31.9-8.5 0 0-5.6-10.2-16.3-11 0 0-10.4-.2-.7 6.5 0 0 6.9 3.3 11.7 15.6 0 0 6.3 21 36.4 14.2V177s-.6 7.7-7.7 10.2c0 0-4.2 2.9.3 4.5 0 0 19.5 1.6 19.5-14.4v-23.6s-.8-9.4 3.8-12.6v38.8s-.3 9.3-5.1 12.8c0 0-3.2 5.7 3.8 4.2 0 0 13.4-1.9 14-17.6l.3-39.3h3.2l.3 39.3c.6 15.6 14 17.6 14 17.6 7 1.6 3.8-4.2 3.8-4.2-4.8-3.5-5.1-12.8-5.1-12.8v-38.5c4.6 3.6 3.8 12.3 3.8 12.3v23.6c0 16 19.5 14.4 19.5 14.4 4.5-1.6.3-4.5.3-4.5-7-2.6-7.7-10.2-7.7-10.2v-31c0-12.1-5.1-18.5-10.1-21.8 29-2.9 42.9-12.2 49.3-26.8 12.7.3 35.6 1.9 57.4 8.1l.3-.9c-21.7-6.1-44.4-7.7-57.3-8.1.6-1.5 1.1-3 1.6-4.6 13.4-.5 35.1-.5 56.3 3.7zm0 0"></path><path fill="#F5CCB3" d="M174.6 63.7c6.2 5.7 9.9 12.5 9.9 19.8 0 34.4-25.6 35.3-57.2 35.3S70.1 114 70.1 83.5c0-7.3 3.6-14.1 9.8-19.7 10.3-9.4 27.7-4.4 47.4-4.4s37-5.1 47.3 4.3zm0 0"></path><path fill="#FFF" d="M108.3 85.3c0 9.5-5.3 17.1-11.9 17.1-6.6 0-11.9-7.7-11.9-17.1 0-9.5 5.3-17.1 11.9-17.1 6.6-.1 11.9 7.6 11.9 17.1zm0 0"></path><path fill="#AF5C51" d="M104.5 85.5c0 6.3-3.6 11.4-7.9 11.4-4.4 0-7.9-5.1-7.9-11.4 0-6.3 3.6-11.4 7.9-11.4 4.3 0 7.9 5.1 7.9 11.4zm0 0"></path><path fill="#FFF" d="M172.2 85.3c0 9.5-5.3 17.1-11.9 17.1-6.6 0-11.9-7.7-11.9-17.1 0-9.5 5.3-17.1 11.9-17.1 6.5-.1 11.9 7.6 11.9 17.1zm0 0"></path><path fill="#AF5C51" d="M168.3 85.5c0 6.3-3.6 11.4-7.9 11.4-4.4 0-7.9-5.1-7.9-11.4 0-6.3 3.6-11.4 7.9-11.4 4.4 0 7.9 5.1 7.9 11.4zm0 0M130.5 100.5c0 1.6-1.3 3-3 3-1.6 0-3-1.3-3-3s1.3-3 3-3c1.6 0 3 1.3 3 3zm0 0M120.6 108c-.2-.5.1-1 .6-1.2.5-.2 1 .1 1.2.6.8 2.2 2.8 3.6 5.1 3.6s4.3-1.5 5.1-3.6c.2-.5.7-.8 1.2-.6.5.2.8.7.6 1.2-1 2.9-3.8 4.9-6.9 4.9-3.1 0-5.9-2-6.9-4.9zm0 0"></path><path fill="#C4E5D9" d="M54.5 121.6c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2 0 2.1.6 2.1 1.4zm0 0M60.3 124.8c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2 0 2.1.6 2.1 1.4zm0 0M63.8 129c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2-.1 2.1.6 2.1 1.4zm0 0M67 133.8c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2-.1 2.1.6 2.1 1.4zm0 0M70.5 138.2c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2 0 2.1.6 2.1 1.4zm0 0M75.3 142.1c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2-.1 2.1.6 2.1 1.4zm0 0M82 144.6c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2 0 2.1.6 2.1 1.4zm0 0M88.7 144.6c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.2 0 2.1.6 2.1 1.4zm0 0M95.5 143.5c0 .8-.9 1.4-2.1 1.4-1.1 0-2.1-.6-2.1-1.4 0-.8.9-1.4 2.1-1.4 1.1 0 2.1.6 2.1 1.4zm0 0"></path></svg>
        </a>
        <a href="https://www.linkedin.com/in/shahnawaz-hussain-442a72152/" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 72 72" id="linkedin"><g fill="none" fill-rule="evenodd"><g><rect width="72" height="72" fill="#117EB8" rx="4"></rect><path fill="#FFF" d="M13.139 27.848h9.623V58.81h-9.623V27.848zm4.813-15.391c3.077 0 5.577 2.5 5.577 5.577 0 3.08-2.5 5.581-5.577 5.581a5.58 5.58 0 1 1 0-11.158zm10.846 15.39h9.23v4.231h.128c1.285-2.434 4.424-5 9.105-5 9.744 0 11.544 6.413 11.544 14.75V58.81h-9.617V43.753c0-3.59-.066-8.209-5-8.209-5.007 0-5.776 3.911-5.776 7.95V58.81h-9.615V27.848z"></path></g></g></svg>
        </a>
        <hr>
        <p>Made with <span style="color:red;font-size:25px;">❤️</span> by <a href="https://www.instagram.com/theshahnawaaz" target="_blank" style="color: #2980b9; text-decoration: none; margin: 0 5px; cursor: pointer; font-weight: bold; font-size: 20px; color: orange;">Shahnawaz</a></p>
    </footer>
"""
st.markdown(footer, unsafe_allow_html=True)
