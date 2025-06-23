import streamlit as st
print("Streamlit module location:", st.__file__)
print("Streamlit version:", st.__version__)
print("Streamlit dir:", dir(st))
st.experimental_rerun() 