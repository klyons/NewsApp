import nltk
#nltk.download()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from sentence_transformers import SentenceTransformer, util
import torch
from plot_functions import *
from textblob import TextBlob
import pdb

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

from collections import Counter
import re

# Two headlines to compare
headline1 = "Trump signs executive order rebranding Pentagon as the Department of War"
headline2 = "Trump changes the Department of Defense’s name to ‘Department of War’"
headline3 = "Mystery of former Federal Reserve Governor Kugler’s resignation deepens as real estate records raise new questions"

charlie_kirk = {
	"foxnews": "Who is Tyler Robinson? What we know about Charlie Kirk's suspected assassin",
	"cnn": "What we know about Charlie Kirk shooting suspect Tyler Robinson",
	"jpost": "Who is Tyler Robinson, the suspect in Charlie Kirk's murder?",
	"newsmax": "Charlie Kirk Shooting Suspect ID'd as Tyler Robinson, 22",
	"aljazeera": "'Smart, quiet': 22-year-old suspect held over killing Charlie Kirk",
	"bbc": "Who is Tyler Robinson, the suspect in custody for shooting Charlie Kirk?"
}	

gov_shutdown = {
	"foxnews": "Substantial federal layoffs have begun amid government shutdown",
	"cnn": "Trump administration lays off thousands of federal workers during government shutdown",
	"jpost": "US State Department to fire over 1,300 employees as Trump admin. aims to shrink federal gov't",
	"newsmax": "Union Implores Judge to Hit Brakes on Spate of Government Layoffs",
	"aljazeera": "Trump announces layoffs amid government shutdown, despite legal questions.",
	"bbc": "Trump administration starts laying off thousands of workers."

}

#for semantic similarities
model = SentenceTransformer('all-MiniLM-L6-v2')


MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# 1 - very similar, 0 - not similar at all
# looks at the direct words themselves
def cosine_analysis(h1, h2):

	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform([str(h1), str(h2)])

	similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
	return similarity[0][0]

def cosine_analysis_args(*args):
	args = args[0]
	"""
	For each headline, computes its average cosine similarity against all other headlines.
	Returns a list of floats (one per headline).
	"""

	embeddings = model.encode(args, convert_to_tensor=True, normalize_embeddings=True)
	n = len(args)
	avg_similarities = []

	for i in range(n):
		ref_emb = embeddings[i]
		# Compare to all other embeddings
		others = torch.cat([embeddings[:i], embeddings[i+1:]], dim=0)
		scores = util.cos_sim(ref_emb, others)
		avg_score = float(scores.mean())
		avg_similarities.append(avg_score)

	return avg_similarities

# 1 - very similar, 0 - not similar at all
# looks at the meaning of the words

def semantic_analysis(h1, h2, model):

	embedding1 = model.encode(h1, convert_to_tensor=True)
	embedding2 = model.encode(h2, convert_to_tensor=True)

	similarity = util.cos_sim(embedding1, embedding2)
	return similarity.item()

def semantic_analysis_args(model, *args):
	args = args[0]
	# Collect only upper triangle (i < j) so we don’t repeat
	similarities = []
	hl = []

	for i in range(len(args)):
		hl = args[:i] + args[i+1:]
		hl = " ".join(hl)
		similarities.append(semantic_analysis(args[i], hl, model))

	return similarities

def matrix_cosine(*args):
	args = args[0]
	pdb.set_trace()
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform(args)

	similarities = cosine_similarity(tfidf_matrix)	
	return similarities

def matrix_semantic(*args):
	args = args[0]
	"""
	Computes a semantic similarity matrix for any number of headlines.

	Returns: NxN numpy array, where N = number of headlines
	"""
	model = SentenceTransformer('all-MiniLM-L6-v2')
	n = len(args)
	matrix = np.zeros((n, n))

	# Compute pairwise similarities
	for i in range(n):
		for j in range(n):
			if i == j:
				matrix[i, j] = 1.0
			else:
				matrix[i, j] = semantic_analysis(args[i], args[j], model)
	
	return matrix


"""
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

text = "VADER is smart, handsome, and funny!"
scores = analyzer.polarity_scores(text)
print(scores)
"""

analyzer = SentimentIntensityAnalyzer()

def sentiment_analysis_vader(*args):
	args = args[0]
	sentiment_list = []
	for a in args:
		text = a
		# Analyze sentiment
		scores = analyzer.polarity_scores(text)
		sentiment_list.append(scores['compound'])
	return sentiment_list

def sentiment_analysis(*args):
	args = args[0]
	sentiment_list = []
	for a in args:
		# Tokenize text
		encoded = tokenizer(a, return_tensors='pt')  
		# Get model output
		output = sentiment_model(**encoded)                   
		# Convert logits → probabilities
		scores = output.logits[0].detach().numpy()
		probs = softmax(scores)
		# Compute a single compound-like score
		compound = float(probs[2] - probs[0])
		sentiment_list.append(compound)
	return sentiment_list


def word_counter(txt):
	target_words = ["oil", "venezuelan", "venezuelans"]

	pdb.set_trace()

	with open(txt, "r", encoding="utf-8") as f:
		text = str(f.read().lower())

	words = re.findall(r'\b\w+\b', text.lower())

	# count all words
	counts = Counter(words)
	# print counts for target words
	#for word in target_words:
		#print(word, counts[word])

	values = [counts[word] for word in target_words]

	plt.barh(target_words, values)
	plt.title("Word Counts")
	plt.xlabel("Frequency")
	plt.ylabel("Words")
	plt.show()


headlines = list(gov_shutdown.values())

cosine = matrix_cosine(headlines)
cosine2 = cosine_analysis_args(headlines)

semantic = matrix_semantic(headlines)
semantic2 = semantic_analysis_args(model, headlines)

sentiment = sentiment_analysis(headlines)

sources = ['foxnews', 'cnn', 'jpost', 'newsmax', 'aljazeera', 'bbc']
labels = ["h4", "h5", "h6", "h7", "h8", "h9"]

"""
print(f"Cosine Similarity: {cosine_analysis(headline4, headline8)}")
print(f"Semantic Similarity: {semantic_analysis(headline5, headline8, model)}")
print(f"Matrix Cosine: {cosine}")
print(f"Matrix Semantic: {semantic}")

"""

#plot_similarity_heatmap(semantic, sources, "Semantic")
#plot_similarity_network(semantic, labels, "Semantic", threshold=0.2)
#plot_headline_3d_scatter(cosine, semantic, labels, sources)

pdb.set_trace()
#plot_headline_3d_scatter_list(cosine2, semantic2, sentiment, sources)

word_counter("venez.txt")
