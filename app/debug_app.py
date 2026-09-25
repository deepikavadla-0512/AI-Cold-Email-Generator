import streamlit as st

st.title("Debugging Cold Mail Generator")

st.write("Step 1: Streamlit works")

from chains import Chain
st.write("Step 2: chains imported")

from portfolio import Portfolio
st.write("Step 3: portfolio imported")

from utils import clean_text
st.write("Step 4: utils imported")

chain = Chain()
st.write("Step 5: Chain created")

portfolio = Portfolio()
st.write("Step 6: Portfolio created")

st.write("Everything loaded successfully!")