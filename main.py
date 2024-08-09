#mailto: lyons.kelly@gmail.com

import requests
import pandas as pd
from textblob import TextBlob
from bs4 import BeautifulSoup

#dictoinary for all updated dataframes
dataframes = {}

def find_links(domain):
    # Send a GET request
    response = requests.get(domain)
    
    if response.status_code == 200:

        # Parse the response text with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Find all 'a' tags (which define hyperlinks)
        links = soup.find_all('a')
        retlinks = []
        # Extract href attribute from each link and print
        for link in links:
            url = link.get('href')
            if url and 'http' in url:  # Check if it's a valid URL
                #print(url)
                retlinks.append(url)
        return retlinks
    else: 
        print("status code error in find_links")

def create_dataframes():

    sources = {
        "Drudge_Report" : "https://www.drudgereport.com", 
        "Mother_Jones": "https://www.motherjones.com",
        "BBC" : "https://www.bbc.com/", 
        "MSNBC" : "https://www.msnbc.com/",
        "CNN" : "https://www.cnn.com/",
        "Fox_News" : "https://www.foxnews.com",
        "News_Max" : "https://www.newsmax.com/"
    }


    for name, url in sources.items():
        links = find_links(url)
        dataframes[name] = pd.DataFrame(links, columns = [name])

    return dataframes



def more_links(df):
    if df.shape[1] < 100:
        new_rows = []  
        for link in df.iloc[:, 0]:  
            extra = find_links(link)
            new_rows.extend(extra)  
        
        if new_rows:
            new_df = pd.DataFrame(new_rows, columns=df.columns)
            df = pd.concat([df, new_df], ignore_index=True)
    return df
                

def valid_link(df):
    dfName = df.columns.tolist()[0]

    i = 0

    for value in df[dfName]:
        if dfName in value:
            pass
        else: 
            df = df.drop(i)
        i += 1
    return df


def remove_duplicate(df):
    df = df.drop_duplicates(subset = df.columns.tolist()[0])
    return df



def text_blob(df):

    df = df.copy()

    if "stories" not in df.columns:

        df["stories"] = ""

    for i, link in enumerate(df.iloc[:, 0]):
        response = requests.get(link)

        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            blob = TextBlob(text)
            df.loc[i, "stories"] = str(blob)  
        else:
            print("status code error in text_blob")

    return df


if __name__ == '__main__':

    dataframes = create_dataframes()

    for name, df in dataframes.items():
        df = more_links(df)
        df = valid_link(df)
        df = remove_duplicate(df)
        df = text_blob(df)
        dataframes[name] = df

        print(df.head())
        print(df.shape[0])

"""
https://textblob.readthedocs.io/en/dev/

from bs4 import BeautifulSoup
from textblob import TextBlob
import requests

# textblob -> NLP library/module
# requests/bs4

# 1. User input
userLink = input("Enter a link to a review: ")

response = requests.get(userLink)

# 2. Fetch then parse data
if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'html.parser')
  text = soup.get_text()

  blob = TextBlob(text)
  print(type(blob))
  blob_class = 

  # polarity: -1 to 1
  # subjectivity: 0 to 1

  # Analyze sentiment
  sentiment = blob.sentiment
  print(sentiment)

else:
  print("cannot fetch")

"""
