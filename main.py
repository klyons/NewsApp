#mailto: lyons.kelly@gmail.com
'''
possible transfer learning libraries:
https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B
https://huggingface.co/SamLowe/roberta-base-go_emotions
https://newsapi.org/
'''
import requests
import pandas as pd
import pdb
from textblob import TextBlob
from bs4 import BeautifulSoup
from parser import *
from urllib.parse import urlparse

#dictionary for all updated dataframes
dataframes = {}

def find_links(domain):
    # Send a GET request
    try:
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
    except:
        print("try except error response code error??")

def get_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    website_name = domain.split('.')[1]  # Extract the main domain name
    return website_name

def create_dataframes(sources):
    dataframes = {}
    for name, url in sources.items():
        links = find_links(url)
        filtered_links = [link for link in links if name in link]
        dataframes[name] = pd.DataFrame(filtered_links, columns=[name])
    return dataframes     

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
    if "story" not in df.columns:
        df["story"] = ""
    for i, link in enumerate(df.iloc[:, 0]):
        response = requests.get(link)

        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            blob = TextBlob(text)
            df.loc[i, "story"] = str(blob)  
        else:
            print("status code error in text_blob")
    return df

sources = {
        "motherjones": "https://www.motherjones.com/politics/",
        "bbc": "https://www.bbc.com/news/", 
        "msnbc": "https://www.msnbc.com/white-house/",
        "cnn": "https://www.cnn.com/politics/",
        "foxnews": "https://www.foxnews.com/politics/",
        "newsmax": "https://www.newsmax.com/politics/",
        "jpost": "https://www.jpost.com/international/",
        "aljazeera": "https://www.aljazeera.com/news/",
        "ap": "https://apnews.com/politics/",
    }

if __name__ == '__main__':
    
    # dataframes is a dictionary of dataframes
    dataframes = create_dataframes(sources)
    #instantiate the parser class
    parser = Parser()
    
    # Parse and process links from Mother Jones
    # This will extract and process hyperlinks from the Mother Jones dataframe
    df_mj = parser.get_hrefs(sources['motherjones'])
    #
    #df_mj = valid_link(df_mj)
    #df_mj = remove_duplicate(df_mj)
    df_mj = text_blob(df_mj) 
    df_mj = parser.parse_motherjones(df_mj)
    #

    df_bc = parser.get_hrefs(sources['bbc'])
    #
    #df_bc = valid_link(df_bc)
    #df_bc = remove_duplicate(df_bc)
    df_bc = text_blob(df_bc) 
    df_bc = parser.parse_bbc(df_bc)
    #
    
    df_cnn = parser.get_hrefs(sources['cnn'])
    #
    #df_cnn = valid_link(df_cnn)
    #df_cnn = remove_duplicate(df_cnn)
    df_cnn = text_blob(df_cnn) 
    df_cnn = parser.parse_cnn(df_cnn)
    #
    
    df_fn = parser.get_hrefs(sources['foxnews'])
    #
    #df_fn = valid_link(df_fn)
    #df_fn = remove_duplicate(df_fn)
    df_fn = text_blob(df_fn) 
    df_fn = parser.parse_foxnews(df_fn)
    #

    df_nm = parser.get_hrefs(sources['newsmax'])
    #
    #df_nm = valid_link(df_nm)
    #df_nm = remove_duplicate(df_nm)
    df_nm = text_blob(df_nm) 
    df_nm = parser.parse_newsmax(df_nm)
    #
    
    df_jp = parser.get_hrefs(sources['jpost'])
    #
    #df_jp = valid_link(df_jp)
    #df_jp = remove_duplicate(df_jp)
    df_jp = text_blob(df_jp) 
    df_jp = parser.parse_jpost(df_jp)
    #
    
    df_al = parser.get_hrefs(sources['aljazeera'])
    #
    #df_al = valid_link(df_al)
    #df_al = remove_duplicate(df_al)
    df_al = text_blob(df_al) 
    df_al = parser.parse_aljazeera(df_al)
    #
    
    df_ap = parser.get_hrefs(sources['ap'])
    #
    #df_ap = valid_link(df_ap)
    #df_ap = remove_duplicate(df_ap)
    df_ap = text_blob(df_ap) 
    df_ap = parser.parse_ap(df_ap)
    #
    


    
"""

    for name, df in dataframes.items():
        df = valid_link(df)
        df = remove_duplicate(df)
        df = text_blob(df)
        # Call the corresponding parsing function if it exists
        if name in parse_functions:
            getattr(parser, parse_functions[name])(df)
            print(df.head(2), "\n", getattr)
        df.to_csv(f'data/{name}.csv', index=False)
"""

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