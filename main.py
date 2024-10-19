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
import parser

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
            print(retlinks)
            return retlinks
    except:
        print("try except error response code error??")

def get_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    website_name = domain.split('.')[1]  # Extract the main domain name
    return website_name

def create_dataframes():
    sources = {
        "drudgereport": "https://www.drudgereport.com", 
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

    dataframes = {}
    for name, url in sources.items():
        links = find_links(url)
        filtered_links = [link for link in links if name in link]
        dataframes[name] = pd.DataFrame(filtered_links, columns=[name])
    return dataframes

"""
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

"""               

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
            pdb.set_trace()
            df.loc[i, "stories"] = str(blob)  
        else:
            print("status code error in text_blob")
    return df


parse_functions = {
    #'drudgereport': parse_stories_drudge,
    'motherjones': parse_stories_motherjones,
    'bbc': parse_stories_bbc,
    #'msnbc': parse_stories_msnbc,
    #'cnn': parse_stories_cnn,
    #'foxnews': parse_stories_foxnews,
    #'newsmax': parse_stories_newsmax,
    #'jpost': parse_stories_jpost,
    #'aljazeera': parse_stories_aljazeera,
    #'acociatedPress': parse_stories_ap
}

if __name__ == '__main__':
    
    parser = parser.Parser()
    
    parse_functions = {
        #'drudgereport': parserparse_stories_drudge,
        #'motherjones': parser.parse_stories_motherjones,
        'bbc': parser.parse_stories_bbc,
        #'msnbc': parser.parse_stories_msnbc,
        #'cnn': parser.parse_stories_cnn,
        #'foxnews': parser.parse_stories_foxnews,
        #'newsmax': parser.parse_stories_newsmax,
        #'jpost': parser.parse_stories_jpost,
        #'aljazeera': parser.parse_stories_aljazeera,
        'acociatedPress': parser.parse_stories_ap
    }
    dataframes = create_dataframes()
    # dataframes is a dictionary of dataframes
    
    
    for name, df in dataframes.items():
        df = valid_link(df)
        df = remove_duplicate(df)
        df = text_blob(df)
        pdb.set_trace()
        # Call the corresponding parsing function if it exists
        if name in parse_functions:
            getattr(parser, parse_functions[name])(df)


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
