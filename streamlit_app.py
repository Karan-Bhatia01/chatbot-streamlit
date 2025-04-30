import streamlit as st
import requests
import time
import pandas as pd
import numpy as np

# Set up the page with a wide layout for better responsiveness
st.set_page_config(page_title="CHATbot.com", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #000000, #222222);
        color: #1DCD9F;
        font-family: monospace;
    }
    .chat-container {
        max-width: 900px;
        margin: 20px auto;
        padding: 20px;
        background-color: #222222;
        border-radius: 10px;
        border: 1px solid #169976;
    }
    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #1DCD9F;
    }
    .header-text {
        font-size: 24px;
        color: #169976;
        text-align: center;
        margin-bottom: 20px;
    }
    .intro-text {
        font-size: 16px;
        color: #1DCD9F;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    .stChatMessage {
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        color: #FFFFFF;
    }
    div[data-testid="stChatMessage"][data-author="user"] {
        background-color: #169976;
    }
    div[data-testid="stChatMessage"][data-author="assistant"] {
        background-color: #333333;
        border: 1px solid #1DCD9F;
    }
    .stChatInput > div > textarea {
        border: 2px solid #1DCD9F;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        color: #FFFFFF;
        background-color: #333333;
    }
    .stChatInput > div > textarea:focus {
        border-color: #169976;
        box-shadow: 0 0 5px rgba(29, 205, 159, 0.5);
    }
    .stButton > button {
        background-color: #1DCD9F;
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #169976;
        transform: translateY(-1px);
    }
    .chart-container {
        background-color: #222222;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #169976;
        margin-bottom: 20px;
    }
    .stExpander {
        border: 1px solid #169976;
        border-radius: 8px;
        background-color: #333333;
        color: #1DCD9F;
    }
    .stExpander p {
        color: #FFFFFF;
    }
    .stCodeBlock {
        background-color: #333333;
        border: 1px solid #169976;
        border-radius: 8px;
    }
    .stMarkdown p {
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# API URL (updated for deployment)
API_URL = "https://chatbot-flask-b8pl.onrender.com/api/query"

# Main header and introduction
st.markdown('<div class="main-title">CHATbot.com</div>', unsafe_allow_html=True)
st.markdown('<div class="header-text">Your Coding Assistant in 2025</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="intro-text">
        In today’s coding world, AI tools are revolutionizing development. From AI-assisted coding to low-code platforms, developers are building faster and smarter. CHATbot.com helps you navigate this landscape by providing instant coding solutions. Whether you're debugging, learning, or building projects, we’ve got you covered!
    </div>
""", unsafe_allow_html=True)

# Layout with two columns: Chat on the left, GenAI Growth Chart on the right
col1, col2 = st.columns([2, 1])

# Chat Section (Left Column)
with col1:
    st.subheader("Chat with CHATbot")
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat = []

    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

        # Store chat messages
        if "chat" not in st.session_state:
            st.session_state.chat = []

        # Show past messages
        for msg in st.session_state.chat:
            with st.chat_message(msg["role"]):
                if "text" in msg:
                    st.markdown(f'<div style="color:#FFFFFF;">{msg["text"]}</div>', unsafe_allow_html=True)
                if "code" in msg:
                    for code in msg["code"]:
                        st.code(code, language="python")

        # Get user input
        user_input = st.chat_input("Ask a coding question...")

        if user_input:
            # Show user message
            with st.chat_message("user"):
                st.markdown(f'<div style="color:#FFFFFF;">{user_input}</div>', unsafe_allow_html=True)
            st.session_state.chat.append({"role": "user", "text": user_input, "code": []})

            # Add dynamic progress bar
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # Check for hardcoded responses
            if user_input.lower() == "give a python code for reversing a string":
                with st.chat_message("assistant"):
                    code_snippet = """
def reverse(s):
    return s[::-1]

text = "Hello"
print(reverse(text))  # Prints: olleH
                    """
                    st.code(code_snippet, language="python")
                st.session_state.chat.append({"role": "assistant", "code": [code_snippet]})

            elif user_input.lower() == "give python code to add two numbers":
                with st.chat_message("assistant"):
                    code_snippet = """
def add(a, b):
    return a + b

x = 4
y = 6
print(add(x, y))  # Prints: 10
                    """
                    st.code(code_snippet, language="python")
                st.session_state.chat.append({"role": "assistant", "code": [code_snippet]})

            else:
                # Show dynamic loading
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        time.sleep(1)

                # Call the API
                try:
                    response = requests.post(API_URL, json={"prompt": user_input}, timeout=60)
                    response.raise_for_status()
                    data = response.json()

                    # Show assistant response
                    with st.chat_message("assistant"):
                        if data["text"]:
                            st.markdown(f'<div style="color:#FFFFFF;">{data["text"]}</div>', unsafe_allow_html=True)
                        if data["code"]:
                            for code in data["code"]:
                                st.code(code, language="python")

                    st.session_state.chat.append({
                        "role": "assistant",
                        "text": data["text"],
                        "code": data["code"]
                    })
                except Exception as e:
                    with st.chat_message("assistant"):
                        st.markdown(f'<div style="color:#FFFFFF;">Error: {str(e)}</div>', unsafe_allow_html=True)
                    st.session_state.chat.append({"role": "assistant", "text": f"Error: {str(e)}", "code": []})

        st.markdown("</div>", unsafe_allow_html=True)

# GenAI Growth Chart Section (Right Column)
with col2:
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Generative AI Market Growth")

        # Expander for GenAI growth chart
        with st.expander("View GenAI Market Growth (2020-2032)"):
            st.markdown('<div style="color:#FFFFFF;"><strong>Generative AI Market Size Over the Years</strong></div>', unsafe_allow_html=True)
            st.markdown('<div style="color:#FFFFFF;">The chart below shows the explosive growth of the Generative AI market, projected to reach $1.3 trillion by 2032.</div>', unsafe_allow_html=True)

            # Data for GenAI market size (in billion USD)
            genai_data = pd.DataFrame({
                "Year": [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032],
                "Market Size (Billion USD)": [5, 10, 20, 43.87, 66, 88, 110, 135, 165, 185, 207, 1000, 1300]
            })
            genai_data.set_index("Year", inplace=True)
            st.line_chart(genai_data, use_container_width=True)

        # Code block with explanation
        st.markdown('<div style="color:#FFFFFF;"><strong>Sample Code Snippet</strong></div>', unsafe_allow_html=True)
        st.code("""
# Function to calculate the square of a number
def square(num):
    return num * num

# Example usage
result = square(5)
print(result)  # Output: 25
        """, language="python")

        # Brief explanation
        st.markdown("""
        <div style="color:#FFFFFF;">
        <strong>Understanding the Code</strong><br>
        The snippet above defines a `square` function that takes a number and returns its square. This is a simple example of how functions can be used to perform calculations in Python.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)