#https://blog.streamlit.io/langchain-streamlit/

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import random
import requests
#from sentiment_analysis import analyze_sent
import math
from textblob import TextBlob
from bs4 import BeautifulSoup

def analyze_sent(url):
    #response = requests.get(url)

    #if response.status_code == 200:
    #soup = BeautifulSoup(response.content, 'html.parser')
    #text = soup.get_text()

    blob = TextBlob(url) #change back to text after
    sentiment = blob.sentiment
    print("Sentiment:", sentiment)
    return sentiment.polarity  
    #else:
        #print("cannot fetch")
        #return 0


def slider(url):
    steps = [-1, -2/3, -1/3, 0, 1/3, 2/3, 1]
    polar_dictionary = {
        -1: "Strong Liberal", 
        -2/3: "Liberal",
        -1/3: "Liberal Leaner",
        0: "Independent",  	
        1/3: "Conservative Leaner",
        2/3: "Conservative",
        1: "Strong Conservative"  
    }

    score = analyze_sent(url)
    st.write(f"DEBUG: analyze_sent returned {score}")

    # Debug raw score value before rounding
    raw_value = score * 3 + 4  # calculate raw value

    # Display raw value before rounding
    st.write(f"DEBUG: Raw value before rounding: {raw_value}")

    # Now round the value for slider
    slide_num = round(raw_value)  # round for slider to get integer value

    value = st.slider("Polarity:", 1, 7, value=slide_num, step=1)

    polarity_score = steps[value - 1]
    label = polar_dictionary[polarity_score]
    st.write(f"Your article is: {label} on the polarity scale")
      


def text_on_screen(): 
    #title
	st.markdown("<style>h1{text-align: center;}</style>", unsafe_allow_html=True)
	st.title("Welcome to _:violet[Newsapp]_!")
      
    #url text box
	given_url = st.text_area("Please provide the URL you are analyzing").strip()
      
	if st.button("Submit") and len(given_url) > 0:
		slider(given_url)












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


def main():
    text_on_screen()

if __name__ == "__main__":
      main()