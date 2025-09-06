from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Two headlines to compare
headline1 = "Trump signs executive order rebranding Pentagon as the Department of War"
headline2 = "Trump changes the Department of Defense’s name to ‘Department of War’"

def analysis(h1, h2):
# Convert headlines to TF-IDF vectors
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform([h1, h2])

	# Compute cosine similarity
	similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
	return similarity[0][0]

print(f"Cosine Similarity: {analysis(headline1, headline2)}")