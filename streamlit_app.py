import os
import streamlit as st
import requests
import pandas as pd

st.title("Workout Data Analyzer")

st.write("This app allows you to analyze your workout data from Hevy.")

# Input field for API Key
api_key = st.text_input("Enter your Hevy API Key:", type="password")
api_url = "https://api.hevyapp.com/v1/workouts"  
headers = {"api-key": api_key}      

# Button to test the API Key
if st.button("Test API Key"):
    if api_key:
        # Test the API key by making a simple request

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            st.success("API Key is valid!")
            # Optionally, show a snippet of the data
            data = response.json()
            st.write("Sample Data:", data[:5])  # Display the first 5 records for preview
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            st.error(f"Response status code: {response.status_code}")
            st.error(f"Response content: {response.content}")
        except Exception as err:
            st.error(f"An error occurred: {err}")
    else:
        st.warning("Please enter an API Key to test.")


    
def fetch_workout_data():
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
        st.error(f"Other error occurred: {err}")
    return pd.DataFrame()

if st.button("Fetch Workout Data"):
    data = fetch_workout_data()
    if not data.empty:
        st.write(data)
    
