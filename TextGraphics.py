
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import re

def read_text_file(file_path):
    """
    Reads a text file and returns its content as a string.
    Handles potential file reading issues.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred reading the file: {e}")
        return None

def wordcloud_gen(file_path):
    """
    Generates a word cloud from a text file.
    Returns the WordCloud object.
    """
    # Read the text file
    text = read_text_file(file_path)
    if text is None or not text.strip():
        print("No text found to generate word cloud")
        return None
    
    # Clean the text: remove special characters and normalize spaces
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    if not cleaned_text:
        print("No valid text content after cleaning")
        return None
    
    # Define stopwords
    stopwords = set(STOPWORDS)
    custom_stopwords = ["applause", "america", "country", "will","american","people","president","united","states"]
    stopwords.update(custom_stopwords)
    # Generate the wordcloud
    try:
        wordcloud = WordCloud(
            width=800, 
            height=800,
            background_color='white',
            stopwords=stopwords,
            min_font_size=10,
            max_words=200  # Limit to top 200 words for better visibility
        ).generate(cleaned_text)
        return wordcloud
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None

def main():
    # Use the correct path to your text file
    file_path = os.path.normpath("data/biden_inagural.csv")  # Despite .csv extension, treating as text
    
    # Generate wordcloud
    wordcloud = wordcloud_gen(file_path)
    
    if wordcloud is None:
        return
    
    # Plot the wordcloud
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
    # Optionally save the wordcloud image
    # wordcloud.to_file("wordcloud.png")

if __name__ == "__main__":
    main()