
import networkx as nx
import spacy
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Load the English model (you may need to run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

text = """Natural language processing enables computers to understand human language. 
It is a core part of modern search engines and virtual assistants like Siri and Alexa."""

doc = nlp(text)

# Extract noun chunks – these are likely your 'subjects'
subjects = [chunk.text for chunk in doc.noun_chunks]

# You can also grab named entities (like 'Siri' and 'Alexa')
entities = [(ent.text, ent.label_) for ent in doc.ents]

print("Noun phrases (potential subjects):", subjects)
print("Named entities:", entities)



# Load Google's pre-trained model (about 3.5GB)
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

vector = model['language']  # returns 300D vector


#find similiaries

sim = cosine_similarity([vector1], [vector2])[0][0]



##### graph




G = nx.Graph()
G.add_nodes_from(keywords)

for i in range(len(keywords)):
    for j in range(i+1, len(keywords)):
        sim = cosine_similarity([model[keywords[i]]], [model[keywords[j]]])[0][0]
        if sim > 0.6:
            G.add_edge(keywords[i], keywords[j], weight=sim)
