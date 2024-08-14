import streamlit as st
import requests
import pandas as pd

st.title("Workout Data Analyzer")

st.write("This app allows you to analyze your workout data from Hevy.")

# Define the API URL
api_url = "https://api.hevyapp.com/v1/workouts"

# Check if the API key is stored in session state
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

# Input field for API Key
api_key_input = st.text_input("Enter your Hevy API Key:", type="password")

# Button to test the API Key
if st.button("Test API Key"):
    if api_key_input:
        headers = {"api-key": api_key_input}
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            st.session_state['api_key'] = api_key_input  # Store the API key in session state
            st.success("API Key is valid!")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            st.error(f"Response status code: {response.status_code}")
            st.error(f"Response content: {response.content}")
        except Exception as err:
            st.error(f"An error occurred: {err}")
    else:
        st.warning("Please enter an API Key to test.")

# Function to fetch workout data
def fetch_workout_data(api_key):
    headers = {"api-key": api_key}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        st.error(f"Response status code: {response.status_code}")
        st.error(f"Response content: {response.content}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return pd.DataFrame()

# Button to fetch workout data
if st.button("Fetch Workout Data"):
    if st.session_state['api_key']:
        data = fetch_workout_data(st.session_state['api_key'])
        if not data.empty:
            st.write(data)
    else:
        st.warning("Please enter and test your API Key first.")