import requests
import pandas as pd
import pdb
from textblob import TextBlob
from bs4 import BeautifulSoup

#story parser
class Paser():
    
	def __init__(self):
		pass

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
				
	def parse_stories_bbc(df):
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
				tagline = soup.find_all('p')
				if tagline:
					df.loc[i, "tagline"] = tagline.get('id')
					pdb.set_trace()
			else:
				print(f"Failed to fetch {link}, status code: {response.status_code}")
	"""					
	def parse_stories_motherjones(self, df):
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
				tagline = soup.find('h2')
				if tagline:
					df.loc[i, "tagline"] = tagline.get_text(strip=True)

	def parse_stories_bbc(self, df):
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
				print("bbc tagline: " + str(tagline))


	def parse_stories_msnbc(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

	def parse_stories_cnn(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

	def parse_stories_foxnews(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

	def parse_stories_newsmax(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

	def parse_stories_jpost(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

	def parse_stories_aljazeera(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')

	def parse_stories_ap(self, df):
		df = self.create_columns(df)
		# i want the item in the columns []
		for i, link in enumerate(df.iloc[0]):
			response = requests.get(link)
			if response.status_code == 200:
				soup = BeautifulSoup(response.content, 'html.parser')