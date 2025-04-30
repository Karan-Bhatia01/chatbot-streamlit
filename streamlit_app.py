import streamlit as st
import requests
import time
import pandas as pd
import numpy as np

# Set up the page with a wide layout for better responsiveness
st.set_page_config(page_title="CHATbot.com", layout="wide")

# Minimal CSS for centering the chat container
st.markdown("""
    <style>
    /* Center the chat container for better layout */
    .chat-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# API URL (update with deployed Flask API URL)
API_URL = "https://chatbot-flask.onrender.com/api/query"

# Main header and introduction
st.title("CHATbot.com")
st.header("Your Coding Assistant in 2025")
st.markdown("""
In today’s coding world, AI tools are revolutionizing development. From AI-assisted coding to low-code platforms, developers are building faster and smarter. CHATbot.com helps you navigate this landscape by providing instant coding solutions. Whether you're debugging, learning, or building projects, we’ve got you covered!
""")

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
                    st.write(msg["text"])
                if "code" in msg:
                    for code in msg["code"]:
                        st.code(code, language="python")

        # Get user input
        user_input = st.chat_input("Ask a coding question...")

        if user_input:
            # Show user message
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.chat.append({"role": "user", "text": user_input, "code": []})

            # Add dynamic progress bar
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # Check for hardcoded responses
            if user_input.lower() == "give a python code for reversing a string":
                with st.chat_message("assistant"):
                    st.code("""
def reverse(s):
    return s[::-1]

text = "Hello"
print(reverse(text))  # Prints: olleH
                    """, language="python")
                st.session_state.chat.append({"role": "assistant", "code": ["def reverse(s):\n    return s[::-1]\n\ntext = \"Hello\"\nprint(reverse(text))  # Prints: olleH"]})

            elif user_input.lower() == "give python code to add two numbers":
                with st.chat_message("assistant"):
                    st.code("""
def add(a, b):
    return a + b

x = 4
y = 6
print(add(x, y))  # Prints: 10
                    """, language="python")
                st.session_state.chat.append({"role": "assistant", "code": ["def add(a, b):\n    return a + b\n\nx = 4\ny = 6\nprint(add(x, y))  # Prints: 10"]})

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
                            st.write(data["text"])
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
                        st.write(f"Error: {str(e)}")
                    st.session_state.chat.append({"role": "assistant", "text": f"Error: {str(e)}", "code": []})

        st.markdown("</div>", unsafe_allow_html=True)

# GenAI Growth Chart Section (Right Column)
with col2:
    st.subheader("Generative AI Market Growth")
    
    # Expander for GenAI growth chart
    with st.expander("View GenAI Market Growth (2020-2032)"):
        st.markdown("**Generative AI Market Size Over the Years**")
        st.markdown("The chart below shows the explosive growth of the Generative AI market, projected to reach $1.3 trillion by 2032.")
        
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
    The snippet above defines a `square` function that takes a number and returns its square. This is a simple example of how functions can be used to perform calculations in Python.
    """)