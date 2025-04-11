# measuring sentiment of a text

from bs4 import BeautifulSoup
from textblob import TextBlob
import requests

# textblob -> NLP library/module
# requests/bs4


def analyze_sent():
  # 1. User input
  userLink = input("Enter a link to a review: ")

  response = requests.get(userLink)

  # 2. Fetch then parse data
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    blob = TextBlob(text)
    print(type(blob))
    #blob_class = 

    # polarity: -1 to 1
    # subjectivity: 0 to 1

    # Analyze sentiment
    sentiment = blob.sentiment
    print(sentiment)

  else:
    print("cannot fetch")