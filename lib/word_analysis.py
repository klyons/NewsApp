from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from plot_functions import *
from textblob import TextBlob


# Two headlines to compare
headline1 = "Trump signs executive order rebranding Pentagon as the Department of War"
headline2 = "Trump changes the Department of Defense’s name to ‘Department of War’"
headline3 = "Mystery of former Federal Reserve Governor Kugler’s resignation deepens as real estate records raise new questions"
headline4 = "Who is Tyler Robinson? What we know about Charlie Kirk's suspected assassin" #fox
headline5 = "What we know about Charlie Kirk shooting suspect Tyler Robinson" #cnn
headline6 = "Who is Tyler Robinson, the suspect in Charlie Kirk's murder?" #jpost
headline7 = "Charlie Kirk Shooting Suspect ID'd as Tyler Robinson, 22" #newsmax
headline8 = "'Smart, quiet': 22-year-old suspect held over killing Charlie Kirk" #aljazeera
headline9 = "Who is Tyler Robinson, the suspect in custody for shooting Charlie Kirk?" #bbc

#for semantic similarities
model = SentenceTransformer('all-MiniLM-L6-v2')

# 1 - very similar, 0 - not similar at all
# looks at the direct words themselves
def cosine_analysis(h1, h2):

	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform([h1, h2])

	similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
	return similarity[0][0]

def cosine_analysis_args(*args):
	"""
	Takes in any number of text inputs and returns a flattened list
	of pairwise cosine similarities (upper triangle, no duplicates).
	"""
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform(args)

	# Full similarity matrix
	similarity_matrix = cosine_similarity(tfidf_matrix)

	# Collect only upper triangle (i < j) so we don’t repeat
	similarities = []
	hl = []
	args_list = list(args)
	for i in range(len(args_list)):
		hl = args_list[:i] + args_list[i+1:]
		hl = " ".join(hl)
		similarities.append(cosine_analysis(i, hl))

	return similarities

# 1 - very similar, 0 - not similar at all
# looks at the meaning of the words

def semantic_analysis(h1, h2, model):

	embedding1 = model.encode(h1, convert_to_tensor=True)
	embedding2 = model.encode(h2, convert_to_tensor=True)

	similarity = util.cos_sim(embedding1, embedding2)
	return similarity.item()

def semantic_analysis_args(model, *args):

	# Collect only upper triangle (i < j) so we don’t repeat
	similarities = []
	hl = []
	args_list = list(args)
	for i in range(len(args_list)):
		hl = args_list[:i] + args_list[i+1:]
		hl = " ".join(hl)
		similarities.append(semantic_analysis(args_list[i], hl, model))

	return similarities

def matrix_cosine(*args):
	headlines = []

	for a in args: 
		headlines.append(a)

	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform(headlines)

	similarities = cosine_similarity(tfidf_matrix)	
	return similarities

def matrix_semantic(*args):
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

def sentiment_analysis(*args):
	sentiment_list = []
	for a in args:
		blob = TextBlob(a)
		# Analyze sentiment
		sentiment = blob.sentiment
		sentiment_list.append(sentiment)
	return sentiment_list

		
cosine = matrix_cosine(headline4, headline5, headline6, headline7, headline8, headline9)
cosine2 = cosine_analysis_args(headline4, headline5, headline6, headline7, headline8, headline9)

semantic = matrix_semantic(headline4, headline5, headline6, headline7, headline8, headline9)
semantic2 = semantic_analysis_args(model, headline4, headline5, headline6, headline7, headline8, headline9)

sentiment = sentiment_analysis(headline4, headline5, headline6, headline7, headline8, headline9)

sources = ['foxnews', 'cnn', 'jpost', 'newsmax', 'aljazeera', 'bbc']
labels = ["h4", "h5", "h6", "h7", "h8", "h9"]

print(f"Cosine Similarity: {cosine_analysis(headline4, headline8)}")
print(f"Semantic Similarity: {semantic_analysis(headline5, headline8, model)}")
print(f"Matrix Cosine: {cosine}")
print(f"Matrix Semantic: {semantic}")

#plot_similarity_heatmap(semantic, sources, "Semantic")
#plot_similarity_network(semantic, labels, "Semantic", threshold=0.2)
#plot_headline_3d_scatter(cosine, semantic, labels, sources)
plot_headline_3d_scatter_list(cosine2, semantic2, sentiment, labels)