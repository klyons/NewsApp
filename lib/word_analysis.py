from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util


# Two headlines to compare
headline1 = "Trump signs executive order rebranding Pentagon as the Department of War"
headline2 = "Trump changes the Department of Defense’s name to ‘Department of War’"
headline3 = "Mystery of former Federal Reserve Governor Kugler’s resignation deepens as real estate records raise new questions"

# 1 - very similar, 0 - not similar at all
def cosine_analysis(h1, h2):
# Convert headlines to TF-IDF vectors
	vectorizer = TfidfVectorizer()
	tfidf_matrix = vectorizer.fit_transform([h1, h2])

	# Compute cosine similarity
	similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
	return similarity[0][0]


def semantic_analysis(h1, h2):
	model = SentenceTransformer('all-MiniLM-L6-v2')


	embedding1 = model.encode(h1, convert_to_tensor=True)
	embedding2 = model.encode(h2, convert_to_tensor=True)

	similarity = util.cos_sim(embedding1, embedding2)
	return similarity.item()


print(f"Cosine Similarity: {cosine_analysis(headline1, headline3)}")
print(f"Semantic Similarity: {semantic_analysis(headline1, headline3)}")