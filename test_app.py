import streamlit as st

st.set_page_config(
    page_title="Test",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Test App")
st.write("If you see this, Streamlit is working!")

if st.button("Click me"):
    st.success("Button clicked!")

