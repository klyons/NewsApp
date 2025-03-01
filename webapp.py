#https://blog.streamlit.io/langchain-streamlit/

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS



st.markdown("<style>h1{text-align: center;}</style>", unsafe_allow_html=True)
st.title("Welcome to _:violet[Newsapp]_!")


def wordcloud_gen(name):
	df = pd.read_csv(name) #name needs to be a string
	#text = " ".join(title for title in df.Title)
	df.head()
	stopwords = set(STOPWORDS)

	for val in df.CONTENT:
     
    	# typecaste each val to string
		val = str(val)
 
    	# split the value
		tokens = val.split()
     
    	# Converts each token into lowercase
		for i in range(len(tokens)):
			tokens[i] = tokens[i].lower()
     
		comment_words += " ".join(tokens)+" "
 
	wordcloud = WordCloud(width = 800, height = 800,
                	background_color ='white',
                	stopwords = stopwords,
                	min_font_size = 10).generate(comment_words)


plt = wordcloud_gen("ap.csv")
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()