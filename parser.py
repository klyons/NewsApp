import requests
import pandas as pd
import pdb
from textblob import TextBlob
from bs4 import BeautifulSoup
import validators
try:
	import RAG
	rag = RAG
except ImportError:
	rag = None


#story parser
class Parser():
	def __init__(self):
		self.print = False

	def create_columns(self, df):
		if "header" not in df.columns:
			df["header"] = ""
		if "tagline" not in df.columns:
			df["tagline"] = ""
		return df

	def get_hrefs(self, address):
		hrefs = []
		if not validators.url(address):
			print(f"Invalid URL: {address}")
			return
		response = requests.get(address)
		if response.status_code == 200:
			soup = BeautifulSoup(response.content, 'html.parser')
			for a_tag in soup.find_all('a', href=True):
				# Check if the link contains the domain name
				if address in str(a_tag):
					hrefs.append(a_tag['href'])
		else:
			print(f"Failed to fetch {address}, status code: {response.status_code}")
		return pd.DataFrame(hrefs, columns=["hrefs"])
	
	def parse_bbc(self, df):
		#find the header and the subheader
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')
				
				# Extract header
				header = soup.find('h1')
				if header:
					if self.print:
						print(header.get_text(strip=True))
					df.loc[i, "header"] = header.get_text(strip=True)
				
				# Extract tagline
				tagline = soup.find_all('p')
				if tagline:
					if self.print:
						print(tagline[0].get_text(strip=True))
					df.loc[i, "tagline"] = tagline[0].get_text(strip=True)

			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
						
	def parse_motherjones(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find_all(class_= 'entry-text')
				if header:
					if self.print:
						print(header.get_text(strip=True))
					df.loc[i, "header"] = header.get_text(strip=True)
				
				#find tagline
				tagline = soup.find('h2')
				if tagline:
					if self.print:
						print(tagline.get_text(strip=True))
					df.loc[i, "tagline"] = tagline.get_text(strip=True)

				#find date
				date = soup.find(class_ = "dateline")
				if date:
					df.loc[i, 'date'] = date.get_text()
		#df.to_csv('motherjones.csv', index=False, mode='a', header=False)  				
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")		
		df.to_parquet('Data/motherjones.parquet', index=False)
  
	def parse_bbc(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find('h1')
				if header:
					df.loc[i, "header"] = header.get_text(strip=True)
				
				#find tagline
				tagline = soup.find_all('p')
				if tagline[0]: 
					df.loc[i, "header"] = tagline[0].get_text(strip=True)

				date = soup.find(class_ = "sc-2b5e3b35-2 fkLXLN")
				if date:
					df.iloc[i, 'date'] = date.get_text()				
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
		df.to_parquet('Data/bbc.parquet', index=False) 

	def parse_msnbc(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find("h1")
				if header: 
					df.loc[i, "header"] = header.get_text(strip=True)

				#find tagline
				tagline = soup.find(id = "article-dek")
				if tagline: 
					df.loc[i, "tagline"] = tagline.get_text(strip=True)

				date = soup.find(class_ = "relative z-1")
				if date:
					df.iloc[i, 'date'] = date.get_text()					 

			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")	
		df.to_parquet('Data/msnbc.parquet', index=False)
  
	def parse_cnn(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find_all(class_= 'headline__text inline-placeholder vossi-headline-text')
				if header: 
					df.loc[i, "header"] = header.get_text(strip=True)
				#find tagline 
				tagline = soup.find_all("p")
				if tagline[0]: 
					df.loc[i, "tagline"] = tagline[0].get_text(strip=True)
				str = soup.find(class_ = "timestamp vossi-timestamp")
				date = str.split(",")
				date = date[-2] + date[-1]
				if date:
					df.iloc[i, 'date'] = date.get_text()					
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")	
		df.to_parquet('Data/cnn.parquet', index=False) 
		#get to fox news
	def parse_foxnews(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')
				#find header
				header = soup.find("h1")
				if header: 
					df.loc[i, "header"] = header.get_text(strip=True)
				#find tagline
				tagline = soup.find("h2")
				if tagline:
					df.loc[i, "tagline"] = tagline.get_text(strip=True)

				date = soup.find(class_ = "article-date")
				if date:
					df.iloc[i, 'date'] = date.get_text()						

			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
		df.to_parquet('Data/foxnews.parquet', index=False)

	def parse_newsmax(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find("h1")
				if header: 
					df.loc[i, "header"] = header.get_text(strip=True)

				#find tagline
				tagline = soup.find_all("p") # in the div that has the id of mainArticleDiv
				if tagline[0]:
					df.loc[i, "tagline"] = tagline[0].get_text(strip=True)

				date = soup.find(class_ = "artPgDate")
				if date:
					df.iloc[i, 'date'] = date.get_text()					
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
		df.to_parquet('Data/newsmax.parquet', index=False)		

	def parse_jpost(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find("h1")
				if header: 
					df.loc[i, "header"] = header.get_text(strip=True)

				#find tagline
				tagline = soup.find("h2")
				if tagline: 
					df.loc[i, "tagline"] = tagline.get_text(strip=True)
	 
				if rag and hasattr(rag, 'query_headlines') and rag.query_headlines(header, tagline):
					date = soup.find(class_ = "updated-date-date")
				else:
					date = None
				if date:
					df.iloc[i, 'date'] = date.get_text()						
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
		df.to_parquet('Data/jpost.parquet', index=False) 
	def parse_aljazeera(self, df):
		
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find(class_= 'breadcrumbs')
				if header:
					df.loc[i, "header"] = header.get_text(strip=True)

				#find tagline
				tagline = soup.find(class_ = 'article-subhead')
				if tagline[0]:
					em_tagline = tagline[0].find('em')
					if em_tagline:
						df.loc[i, "tagline"] = em_tagline.get_text(strip=True)

				date = soup.find(class_ = "screen-reader-text")
				if date:
					df.iloc[i, 'date'] = date.get_text()					
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
		df.to_parquet('Data/aljazeera.parquet', index=False)

	def parse_ap(self, df):
		#find the header and the subheader
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')
				
				#find header
				header = soup.find(class_ = 'Page-headline')
				if header:
					df.loc[i, "header"] = header.get_text(strip=True)
				
				#find tagline
				tagline = soup.find_all("p", class_ ='RichTextStoryBody RichTextStory')
				if tagline[0]:
					df.loc[i, "tagline"] = tagline[0].get_text(strip=True)

				soup = soup.find('span', attrs={'data-date': ''})
				date = soup.find("span")
				if date: 
					df.iloc[i, 'date'] = date.get_text()				 
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
		df.to_parquet('Data/ap.parquet', index=False)
	
		# Your specific parsing logic for Associated Press

"""

if __name__ == '__main__':
	parser = Parser()
	# Example: create a DataFrame with a column of URLs for testing
	# Replace these URLs with real news article URLs as needed
	data = {'links': [
		'https://www.bbc.com/news/world-us-canada-62087185',
		'https://www.bbc.com/news/world-europe-62087186'
	]}
	df = pd.DataFrame(data)
	# The parser expects the links in the first column, so pass df accordingly
	parser.parse_bbc(df)

"""