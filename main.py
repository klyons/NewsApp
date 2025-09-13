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
# local libs
from lib.logger import get_logger
from lib.parser import *
from urllib.parse import urlparse

#dictionary for all updated dataframes
dataframes = {}


log = get_logger(__name__)

#finding all the links on a webpage
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

#creating dataframes for each source
def create_dataframes(sources):
    dataframes = {}
    for name, url in sources.items():
        links = find_links(url)
        filtered_links = [link for link in links if name in link]
        dataframes[name] = pd.DataFrame(filtered_links, columns=[name])
    return dataframes     

#pulling the text from the links
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
 
#sources for news websites
sources = {
        "motherjones": "https://www.motherjones.com/politics/",
        #"bbc": "https://www.bbc.com/news/", 
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
 
    #motherjones
    df_mj = parser.get_hrefs(sources['motherjones'])
    df_mj = text_blob(df_mj) 
    df_mj = parser.parse_motherjones(df_mj)
    #

    #bbc
    #df_bc = parser.get_hrefs(sources['bbc'])
    #df_bc = text_blob(df_bc) 
    #df_bc = parser.parse_bbc(df_bc)
    
    # MSNBC
    df_msnbc = parser.get_hrefs(sources['msnbc'])
    df_msnbc = text_blob(df_msnbc)
    df_msnbc = parser.parse_msnbc(df_msnbc)

    # CNN
    df_cnn = parser.get_hrefs(sources['cnn'])
    df_cnn = text_blob(df_cnn) 
    df_cnn = parser.parse_cnn(df_cnn)

    # Fox News
    df_fn = parser.get_hrefs(sources['foxnews'])
    df_fn = text_blob(df_fn) 
    df_fn = parser.parse_foxnews(df_fn)
    #

    # Newsmax
    df_nm = parser.get_hrefs(sources['newsmax'])
    df_nm = text_blob(df_nm) 
    df_nm = parser.parse_newsmax(df_nm)

    # The Jerusalem Post
    df_jp = parser.get_hrefs(sources['jpost'])
    df_jp = text_blob(df_jp) 
    df_jp = parser.parse_jpost(df_jp)

    # Al Jazeera
    df_al = parser.get_hrefs(sources['aljazeera'])
    df_al = text_blob(df_al) 
    df_al = parser.parse_aljazeera(df_al)

    # Associated Press
    df_ap = parser.get_hrefs(sources['ap'])
    df_ap = text_blob(df_ap) 
    df_ap = parser.parse_ap(df_ap)
    
    