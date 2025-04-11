import requests
import pandas as pd
import pdb
from textblob import TextBlob
from bs4 import BeautifulSoup
#from RAG.py import *


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
	"""
	def parse_stories_mother_jones(df):
		#find the header and the subheader
		df = self.create_columns(df)
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')
				
				# Extract header
				header = soup.find('h1')
				if header:
					df.loc[i, "header"] = header.get_text(strip=True)
				
				# Extract tagline
				tagline = soup.find('h2')
				if tagline:
					df.loc[i, "tagline"] = tagline.get_text(strip=True)
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
	
	def parse_stories_drudge(df):
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
					df.loc[i, "header"] = header.get_text(strip=True)
				
				# Extract tagline
				tagline = soup.find('h2')
				if tagline:
					df.loc[i, "tagline"] = tagline.get_text(strip=True)
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
	"""			
	def parse_bbc(df):
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
					df.loc[i, "tagline"] = tagline.get('id')

			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
						
	def parse_motherjones(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			pdb.set_trace()
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

				#find header
				header = soup.find('h1')
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
				df.iloc[i, 'date'] = date.get_text()

		df.to_csv('motherjones.csv', index=False, mode='a', header=False)  		


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

		df.to_csv('bbc.csv', index=False, mode='a', header=False) 	

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

		df.to_csv('msnbc.csv', index=False, mode='a', header=False) 

	def parse_cnn(self, df):
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
				tagline = soup.find_all("p")
				if tagline[0]: 
					df.loc[i, "tagline"] = tagline[0].get_text(strip=True)
				str = soup.find(class_ = "timestamp vossi-timestamp")
				date = str.split(",")
				date = date[-2] + date[-1]
				if date:
					df.iloc[i, 'date'] = date.get_text()	

		df.to_csv('cnn.csv', index=False, mode='a', header=False) 


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

		df.to_csv('foxnews.csv', index=False, mode='a', header=False) 		

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

		df.to_csv('newsmax.csv', index=False, mode='a', header=False) 

				

	def parse_stories_jpost(self, df):
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
					df.loc[i, tagline] = tagline.get_text(strip=True)
				if rag.query_headlines(header, tagline):
					date = soup.find(class_ = "updated-date-date")
				if date:
					df.iloc[i, 'date'] = date.get_text()	

		df.to_csv('jpost.csv', index=False, mode='a', header=False) 	

	def parse_stories_aljazeera(self, df):
		
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
				tagline = soup.find('p')
				if tagline[0]:
					em_tagline = tagline[0].find('em')
					if em_tagline:
						df.loc[i, "tagline"] = em_tagline.get_text(strip=True)

				date = soup.find(class_ = "screen-reader-text")
				if date:
					df.iloc[i, 'date'] = date.get_text()	

		df.to_csv('aljazeera.csv', index=False, mode='a', header=False) 

	def parse_stories_ap(self, df):
		pdb.set_trace()
		#find the header and the subheader
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
					df.loc[i, "tagline"] = tagline[0].get_text(strip=True)

				soup = soup.find(class_ = "Page-dateModified")
				date = soup.find("span")
				if date: 
					df.iloc[i, 'date'] = date.get_text()

		df.to_csv('ap.csv', index=False, mode='a', header=False) 

    
        # Your specific parsing logic for Associated Press



if __name__ == '__main__':
	
	parser = Parser()
	
	parser.parse_bbc()
    