import streamlit as st
from stackquery import stackquery


st.set_page_config(
    page_title="StackQuery - AI-Powered Coding Help",
    page_icon="🔍",
    layout="centered",
)

st.markdown(
    """
    <style>
        body {
            background-color: #f5f5f5;
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #774caf;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #555;
        }
        .stTextInput {
            border-radius: 10px;
            border: 2px solid #774caf;
            padding: 8px;
        }
        .stButton>button {
            background-color: #774caf;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
        }
        .result-box {
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<h1 class="title">StackQuery 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Get AI-powered answers from Stack Overflow</p>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### ℹ️ How it works:")
    st.write(
        """
        - Enter your **coding question** in the text box.
        - Click **Search** to get answers from **Stack Overflow**.
        - AI extracts the most relevant information and presents it here!
        """
    )
    st.markdown("*Made with 💜 -by Priyanshu Dutta*")


query = st.text_input(" **Enter your coding question:**", placeholder="e.g., How to fix Flutter NDK not found error?")


if st.button("Search 🔍"):
    if query.strip():
        with st.spinner("Searching for answers..."):
            response = stackquery(query)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(response, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please enter a query!")

