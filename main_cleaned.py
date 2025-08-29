# mailto: lyons.kelly@gmail.com
"""
News scraping application for political news sources.

Possible transfer learning libraries:
https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B
https://huggingface.co/SamLowe/roberta-base-go_emotions
https://newsapi.org/
"""

import logging
import requests
import pandas as pd
from textblob import TextBlob
from bs4 import BeautifulSoup
from lib.parser import Parser

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def text_blob(df):
    """Extract and analyze text content from links using TextBlob."""
    if df is None or df.empty:
        logger.warning("DataFrame is empty or None, skipping text extraction")
        return df
    
    df = df.copy()
    
    # Ensure required columns exist
    if "dates" not in df.columns:
        df["dates"] = ""
    if "stories" not in df.columns:
        df["stories"] = ""
        
    source_col = df.columns[0]
    
    for i, link in enumerate(df[source_col]):
        if pd.isna(link) or not link:
            continue
            
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            
            # Use xml parser if content looks like XML, otherwise use html.parser
            content_type = response.headers.get('content-type', '').lower()
            if 'xml' in content_type:
                soup = BeautifulSoup(response.content, features="xml")
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                
            text = soup.get_text(separator=' ', strip=True)
            
            # Only process if we got meaningful text
            if text:
                blob = TextBlob(text)
                df.loc[i, "stories"] = str(blob)
            else:
                df.loc[i, "stories"] = ""
            
        except requests.RequestException as e:
            logger.error(f"Error processing {link}: {str(e)}")
            df.loc[i, "stories"] = ""
            
        except Exception as e:
            logger.error(f"Unexpected error processing {link}: {str(e)}")
            df.loc[i, "stories"] = ""
    
    return df


def process_news_source(parser, source_name, url):
    """Process a single news source by getting links, extracting text, and parsing."""
    try:
        logger.info(f"Processing {source_name}...")
        
        # Get hrefs for the source
        df = parser.get_hrefs(url)
        
        if df is None or df.empty:
            logger.warning(f"No data retrieved for {source_name}")
            return None
            
        # Apply text analysis
        df = text_blob(df)
        
        # Get the corresponding parsing method
        parse_method = getattr(parser, f"parse_{source_name}", None)
        if parse_method:
            parse_method(df)
            logger.info(f"Successfully parsed {source_name}")
        else:
            logger.warning(f"No specific parser found for {source_name}")
            
        return df
        
    except Exception as e:
        logger.error(f"Error processing {source_name}: {str(e)}")
        return None


# News source URLs
SOURCES = {
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


def main():
    """Main function to orchestrate the news scraping process."""
    try:
        logger.info("Starting news scraping process...")
        
        # Instantiate the parser class
        parser = Parser()
        
        # Dictionary to store processed dataframes
        processed_dfs = {}
        
        # Process each news source
        for source_name, url in SOURCES.items():
            processed_df = process_news_source(parser, source_name, url)
            if processed_df is not None:
                processed_dfs[source_name] = processed_df
        
        logger.info("News scraping process completed.")
        logger.info(f"Successfully processed {len(processed_dfs)} sources: {list(processed_dfs.keys())}")
        
        return processed_dfs
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return {}


if __name__ == '__main__':
    results = main()
