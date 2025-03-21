#https://blog.streamlit.io/langchain-streamlit/

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS



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

def read_csv_file(file_path):
    """
    Reads a CSV file and returns its content as a list of dictionaries.
    Each dictionary represents a row, with keys being the header names.
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None
    return data




def wordcloud_gen(name):
	#df = pd.read_csv(name) #name needs to be a string
	#text = " ".join(title for title in df.Title)
	#df.head()
     
	stopwords = set(STOPWORDS)

	for val in name:
     
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
     
	file = read_csv_file("/Users/sirikelshikar/workspace/NewsApp/text.csv")

	plt = wordcloud_gen(file)
	plt.figure(figsize = (8, 8), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad = 0)

	plt.show()
	return wordcloud