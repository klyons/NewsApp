import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS


def read_csv_file(file_path):
    print("first function")
    """
    Reads a CSV file and returns its content as a list of dictionaries.
    Each dictionary represents a row, with keys being the header names.
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None
    return data




def wordcloud_gen(name):
	#df = pd.read_csv(name) #name needs to be a string
	#text = " ".join(title for title in df.Title)
	#df.head()
     
	stopwords = set(STOPWORDS)

	for val in name:
     
    	# typecaste each val to string
		val = str(val)
 
    	# split the value
		tokens = val.split()
     
    	# Converts each token into lowercase
		for i in range(len(tokens)):
			tokens[i] = tokens[i].lower()
     
		comment_words += " ".join(tokens)+" "
 
	wordcloud = WordCloud(width = 800, height = 800,
                	background_color ='white',
                	stopwords = stopwords,
                	min_font_size = 10).generate(comment_words)
     
	file = read_csv_file("/Users/sirikelshikar/workspace/NewsApp/text.csv")

	plt = wordcloud_gen(file)
	plt.figure(figsize = (8, 8), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad = 0)

	plt.show()
	return wordcloud