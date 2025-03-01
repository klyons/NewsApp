#https://blog.streamlit.io/langchain-streamlit/

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud



st.markdown("<style>h1{text-align: center;}</style>", unsafe_allow_html=True)
st.title("Welcome to _:violet[Newsapp]_!")


def wordCloud(name):
	df = pd.read_csv(name) #name needs to be a string
	#text = " ".join(title for title in df.Title)
	df.head()
