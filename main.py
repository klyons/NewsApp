#mailto: lyons.kelly@gmail.com
'''
possible transfer learning libraries:
https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B
https://huggingface.co/SamLowe/roberta-base-go_emotions
'''
import requests
import pandas as pd
import pdb
from textblob import TextBlob
from bs4 import BeautifulSoup
from parser import *

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
    df = df.copy()
    if "dates" not in df.columns:

        df["dates"] = ""
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

sources = {
        #"drudgereport": "https://www.drudgereport.com", 
        "motherjones": "https://www.motherjones.com",
        "bbc": "https://www.bbc.com/", 
        "msnbc": "https://www.msnbc.com/",
        "cnn": "https://www.cnn.com/",
        "foxnews": "https://www.foxnews.com",
        "newsmax": "https://www.newsmax.com/",
        "jpost": "https://www.jpost.com/",
        "aljazeera": "https://www.aljazeera.com/",
        "acociatedPress": "https://apnews.com/",
    }

if __name__ == '__main__':
    
    dataframes = create_dataframes(sources)
    pdb.set_trace()
    
    parser = Parser()
    #  ['motherjones', 'bbc', 'msnbc', 'cnn', 'foxnews', 'newsmax', 'jpost', 'aljazeera', 'acociatedPress']
    df_mj = parser.parse_stories_mother_jones(dataframes['motherjones'])
    parser.parse_bbc(dataframes['bbc'])
    # parser.parse_stories_drudge(dataframes)
    parser.parse_stories_cnn(dataframes['cnn'])
    parser.parse_stories_foxnews(dataframes['foxnews'])
    parser.parse_stories_newsmax(dataframes['newsmax'])
    parser.parse_stories_jpost(dataframes['jpost'])
    parser.parse_stories_aljazeera(dataframes['aljazeera'])
    parser.parse_stories_acociatedPress(dataframes['acociatedPress'])
    
    # dataframes is a dictionary of dataframes
    
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
