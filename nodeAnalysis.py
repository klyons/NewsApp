# for word embeddings and graph analysis
# Import necessary libraries for Word2Vec and graph analysis
from gensim.models import KeyedVectors

# nodeAnalysis.py
# This script performs node analysis on news articles using Word2Vec embeddings and NetworkX for graph representation.
# also creates a graph of articles based on cosine similarity of their embeddings.
import networkx as nx

#standard libraries
import logging
import numpy as np
import nltk
from nltk.corpus import stopwords
import string

# Load the Google News Word2Vec model. Ensure you have the 'GoogleNews-vectors-negative300.bin' file.
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

# Ensure you have downloaded necessary NLTK resources:
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Simple tokenization and cleaning example:
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    return tokens

def document_vector(text):
    tokens = preprocess(text)
    vectors = [model[word] for word in tokens if word in model.key_to_index]
    return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)

# Example usage:
sample_article = "Your news article text goes here."
doc_vector = document_vector(sample_article)


from scipy.spatial.distance import cosine

def cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

# Assume article_vectors is a list of vectors for your news articles
# For constructing a graph, you might consider a similarity threshold to decide when an edge should be added.
threshold = 0.8  # Adjust based on exploratory analysis


G = nx.Graph()

# Add nodes to the graph (could use article IDs or titles)
for idx in range(len(article_vectors)):
    G.add_node(idx)

# Add weighted edges between articles based on cosine similarity
n_articles = len(article_vectors)
for i in range(n_articles):
    for j in range(i + 1, n_articles):
        sim = cosine_similarity(article_vectors[i], article_vectors[j])
        if sim > threshold:
            G.add_edge(i, j, weight=sim)