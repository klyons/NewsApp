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
				