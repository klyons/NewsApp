#https://blog.streamlit.io/langchain-streamlit/

# https://networkx.org/documentation/stable/auto_examples/algorithms/plot_betweenness_centrality.html#sphx-glr-auto-examples-algorithms-plot-betweenness-centrality-py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import csv



st.markdown("<style>h1{text-align: center;}</style>", unsafe_allow_html=True)
st.title("Welcome to _:violet[Newsapp]_!")



st.markdown("""
<style>
    /* Change slider color from red to black */
    .stSlider [data-baseweb="slider"] .WebkitProgressBar {
        background-color: black !important;
    }
    
    /* This changes the slider thumb color to match */
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
        background-color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Create a slider with range 1-7 and step size of 1
value = st.slider("Select a value", min_value=1, max_value=7, value=4, step=1)
st.write(f"The selected value is: {value}")

