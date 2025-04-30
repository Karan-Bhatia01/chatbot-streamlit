import streamlit as st
import requests

# Define the Flask API URL
API_URL = "https://chatbot-flask-b8pl.onrender.com"

# Streamlit app
st.title("Chatbot Interface")

# Input prompt
prompt = st.text_input("Enter your prompt:", "What is a Python list?")

# Button to send the request
if st.button("Get Response"):
    try:
        # Send POST request to the Flask API
        response = requests.post(API_URL, json={"prompt": prompt})
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the response
        data = response.json()

        # Display the response text
        if "text" in data:
            st.subheader("Response:")
            st.write(data["text"])
        else:
            st.error("Error: 'text' not found in response")

        # Display any code snippets if present
        if "code" in data and data["code"]:
            st.subheader("Code:")
            for code_snippet in data["code"]:
                st.code(code_snippet, language="python")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
    except ValueError as e:
        st.error(f"Error parsing response: {str(e)}")

if __name__ == "__main__":
    st.write("Streamlit app is running.")