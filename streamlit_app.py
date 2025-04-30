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
    /* Background and overall theme */
    .stApp {
        background: linear-gradient(to bottom right, #e3f2fd, #90caf9);
        font-family: 'Arial', sans-serif;
    }
    
    /* Center the main content */
    .main-content {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Main title styling with gradient */
    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        background: -webkit-linear-gradient(#1976d2, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Header styling */
    .header-text {
        font-size: 24px;
        color: #0d47a1;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Intro text styling */
    .intro-text {
        font-size: 16px;
        color: #333;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.6;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    div[data-testid="stChatMessage"][data-author="user"] {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
    }
    div[data-testid="stChatMessage"][data-author="assistant"] {
        background-color: #ffffff;
        border: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* Response text styling */
    .response-text {
        font-size: 16px;
        color: #333;
        line-height: 1.6;
    }
    
    /* Chat input styling */
    .stChatInput > div > textarea {
        border: 2px solid #1976d2;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stChatInput > div > textarea:focus {
        border-color: #0d47a1;
        box-shadow: 0 0 8px rgba(25, 118, 210, 0.3);
    }
    
    /* Clear chat button styling */
    .stButton > button {
        background-color: #1976d2;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0d47a1;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* GenAI chart section styling */
    .chart-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Expander styling */
    .stExpander {
        border: 1px solid #90caf9;
        border-radius: 10px;
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# API URL (updated for deployment)
API_URL = "https://chatbot-flask-b8pl.onrender.com/api/query"

# Main header and introduction
st.markdown('<div class="main-title">CHATbot.com</div>', unsafe_allow_html=True)
st.markdown('<div class="header-text">Your Coding Assistant in 2025</div>', unsafe_allow_html=True)
st.markdown('<div class="intro-text">AI tools are transforming coding with faster, smarter solutions. CHATbot.com offers instant help for debugging, learning, or building projects.</div>', unsafe_allow_html=True)

# Layout with two columns: Chat on the left, GenAI Growth Chart on the right
col1, col2 = st.columns([2, 1])

# Chat Section (Left Column)
with col1:
    st.subheader("Chat with CHATbot")
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat = []

    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        # Store chat messages
        if "chat" not in st.session_state:
            st.session_state.chat = []

        # Show past messages
        for msg in st.session_state.chat:
            with st.chat_message(msg["role"]):
                if "text" in msg:
                    st.markdown(f'<div class="response-text">{msg["text"]}</div>', unsafe_allow_html=True)
                if "code" in msg:
                    for code in msg["code"]:
                        st.code(code, language="python")

        # Get user input
        user_input = st.chat_input("Ask a coding question...")

        if user_input:
            # Show user message
            with st.chat_message("user"):
                st.markdown(f'<div class="response-text">{user_input}</div>', unsafe_allow_html=True)
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
                            st.markdown(f'<div class="response-text">{data["text"]}</div>', unsafe_allow_html=True)
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
                        st.markdown(f'<div class="response-text">Error: {str(e)}</div>', unsafe_allow_html=True)
                    st.session_state.chat.append({"role": "assistant", "text": f"Error: {str(e)}", "code": []})

        st.markdown('</div>', unsafe_allow_html=True)

# GenAI Growth Chart Section (Right Column)
with col2:
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Generative AI Market Growth")
        
        # Expander for GenAI growth chart
        with st.expander("View GenAI Market Growth (2020-2032)"):
            st.markdown("**Generative AI Market Size Over the Years**")
            st.markdown("The chart below shows the growth of the GenAI market, projected to reach $1.3 trillion by 2032.")
            
            # Data for GenAI market size (in billion USD)
            genai_data = pd.DataFrame({
                "Year": [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032],
                "Market Size (Billion USD)": [5, 10, 20, 43.87, 66, 88, 110, 135, 165, 185, 207, 1000, 1300]
            })
            genai_data.set_index("Year", inplace=True)
            st.line_chart(genai_data, use_container_width=True)

        # Code block with explanation
        st.markdown("**Sample Code Snippet**")
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
        **Understanding the Code**  
        The `square` function takes a number and returns its square.
        """)
        st.markdown('</div>', unsafe_allow_html=True)