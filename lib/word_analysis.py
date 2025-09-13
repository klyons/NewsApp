from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util


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


# 1 - very similar, 0 - not similar at all
# looks at the direct words themselves
def cosine_analysis(h1, h2):
# Convert headlines to TF-IDF vectors
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform([h1, h2])

	# Compute cosine similarity
	similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
	return similarity[0][0]

# 1 - very similar, 0 - not similar at all
# looks at the meaning of the words
def semantic_analysis(h1, h2):
	model = SentenceTransformer('all-MiniLM-L6-v2')


	embedding1 = model.encode(h1, convert_to_tensor=True)
	embedding2 = model.encode(h2, convert_to_tensor=True)

	similarity = util.cos_sim(embedding1, embedding2)
	return similarity.item()

def matrix_cosine(*args):
	headlines = []

	for a in args: 
		headlines.append(a)

	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform(headlines)

	similarities = cosine_similarity(tfidf_matrix)	
	return similarities


def matrix_semantic(*args):
	headlines = []

	for a in args:
		headlines.append(a)

		

print(f"Cosine Similarity: {cosine_analysis(headline4, headline8)}")
print(f"Semantic Similarity: {semantic_analysis(headline4, headline8)}")
print(f"Matrix Similarity: {matrix_analysis(headline4, headline5, headline6, headline7, headline8, headline9)}")