import streamlit as st
import requests
import matplotlib.pyplot as plt

# Define the Flask API URL
API_URL = "https://chatbot-flask-b8pl.onrender.com/api/query"

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .stTextInput > div > input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .response-box {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 15px;
        margin-top: 10px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.markdown('<div class="main-title">CHATbot.com</div>', unsafe_allow_html=True)

# Graph: Growth of GenAI field over the years (hypothetical data)
st.subheader("Growth of GenAI Field Over the Years")
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
genai_growth = [5, 10, 20, 35, 50, 70, 100, 150, 220, 300, 400]  # Hypothetical growth in publications/funding (arbitrary units)

fig, ax = plt.subplots()
ax.plot(years, genai_growth, marker='o', color='b', label='GenAI Growth')
ax.set_xlabel('Year')
ax.set_ylabel('Growth (Arbitrary Units)')
ax.set_title('GenAI Field Growth')
ax.grid(True)
ax.legend()
st.pyplot(fig)

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
            st.markdown(f'<div class="response-box">{data["text"]}</div>', unsafe_allow_html=True)
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