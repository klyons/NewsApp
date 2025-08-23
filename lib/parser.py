import requests
import pandas as pd
import pdb
from textblob import TextBlob
from bs4 import BeautifulSoup
import validators
from urllib.parse import urljoin
import os
from datetime import datetime

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
        response = requests.get(address)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            from urllib.parse import urlparse
            base_domain = urlparse(address).netloc
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Make absolute if needed
                if not href.startswith(('http://', 'https://')):
                    href = urljoin(address, href)
                # Only keep links on the same domain
                href_domain = urlparse(href).netloc
                if href_domain == base_domain and validators.url(href):
                    hrefs.append(href)
        else:
            print(f"Failed to fetch {address}, status code: {response.status_code}")
        return pd.DataFrame(hrefs, columns=["hrefs"])
#--------------------------------------------------------------------------------------------------
    #fix header & tagline - otherwise DONE
    def parse_motherjones(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.motherjones.com"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
                soup = BeautifulSoup(response.content, 'html.parser')
                # find header
                header = soup.find(class_='entry-text')
                if header:
                    if self.print:
                        print(header.get_text(strip=True))
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find('h2')
                if tagline:
                    if self.print:
                        print(tagline.get_text(strip=True))
                    df.loc[i, "tagline"] = tagline.get_text(strip=True)
                # find date
                date = soup.find(class_ = "dateline")
                if date:
                    df.loc[i, 'date'] = date.get_text(strip=True)
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {full_link}, status code: {response.status_code}")
        parquet_path = f'Data/motherjones.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)

#--------------------------------------------------------------------------------------------------
# Doesn't work because of a webscrapper block
#     def parse_bbc(self, df):
#         pdb.set_trace()
#         counter = 0
#         df = self.create_columns(df)
#         df = df.reset_index(drop=True)
#         base_url = "https://www.bbc.com"
#         # Iterate over all rows in the DataFrame3
#         for i, row in df.iterrows():
#             link = row.get('hrefs', None)
#             # Skip empty, fragment, or mailto/javascript links
#             if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
#                 continue
#             # Convert relative URLs to absolute
#             full_link = urljoin(base_url, str(link))
#             response = requests.get(full_link)
#             if response.status_code == 200:
#                 counter += 1
#                 soup = BeautifulSoup(response.content, 'html.parser')
#                 # find header
#                 header = soup.find('h1')
#                 if header:
#                     df.loc[i, "header"] = header.get_text(strip=True)
#                 # find tagline
#                 tagline = soup.find_all('p')
#                 if tagline[0]:
#                     df.loc[i, "header"] = tagline[0].get_text(strip=True)
#                 # find date
#                 date = soup.find(class_ = "sc-2b5e3b35-2 fkLXLN")
#                 if date:
#                     df.iloc[i, 'date'] = date.get_text()
#                 df.to_parquet('Data/bbc.parquet', index=False)
#             else:
#                 print(f"Failed to fetch {link}, status code: {response.status_code}")
#         df.to_parquet('Data/bbc.parquet', index=False)
#         pdb.set_trace()
#--------------------------------------------------------------------------------------------------
    #fix header & tagline & date - otherwise DONE  
    def parse_msnbc(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.msnbc.com"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
                soup = BeautifulSoup(response.content, 'html.parser')
                # find header
                header = soup.find('h1')
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find_all('p')
                if tagline[0]:
                    df.loc[i, "header"] = tagline[0].get_text(strip=True)
                # find date
                date = soup.find(class_ = "sc-2b5e3b35-2 fkLXLN")
                if date:
                    df.loc[i, 'date'] = date.get_text()
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/bbc.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            for col in ['header', 'tagline', 'date']:
                if col not in combined_df.columns:
                    combined_df[col] = ""
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)
#--------------------------------------------------------------------------------------------------        
    #no date - otherwise DONE
    def parse_cnn(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.cnn.com"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
                soup = BeautifulSoup(response.content, 'html.parser')
                header = soup.find(class_= 'headline__text inline-placeholder vossi-headline-text')
                # find header
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find("p")
                if tagline:
                    df.loc[i, "tagline"] = tagline.get_text(strip=True)
                # find date
                str_ = soup.select(".timestamp vossi-timestamp")
                if str_:
                    date = str_.split(",") if str_ else []
                    if len(date) >= 2:
                        date = date[-2] + date[-1]
                        df.loc[i, 'date'] = date
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/cnn.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)

#--------------------------------------------------------------------------------------------------
    #no date - otherwise DONE 
    def parse_foxnews(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.foxnews.com"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            # Fetch the page content
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # find header
                header = soup.find("h1")
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find("h2")
                if tagline:
                    df.loc[i, "tagline"] = tagline.get_text(strip=True)
                # find date
                date = soup.find(class_ = "article-date")
                if date:
                    df.loc[i, 'date'] = date.get_text()
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/foxnews.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)
#--------------------------------------------------------------------------------------------------
    #no date - otherwise DONE
    def parse_newsmax(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.newsmax.com"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            # Fetch the page content
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                header = soup.find("h1")
                # find header
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find("p")
                if tagline:
                    df.loc[i, "tagline"] = tagline.get_text(strip=True)
                # find date
                date = soup.find(class_ = "artPgDate")
                if date:
                    df.loc[i, 'date'] = date.get_text()
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/foxnews.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)

#--------------------------------------------------------------------------------------------------        
    # no date - otherwise DONE
    def parse_jpost(self, df):
        pdb.set_trace()
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.jpost.com"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            # Fetch the page content
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
                soup = BeautifulSoup(response.content, 'html.parser')
                # find header
                header = soup.find("h1")
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find("h2")
                if tagline:
                    df.loc[i, "tagline"] = tagline.get_text(strip=True)
                # find date
                date = soup.find(class_ = "updated-date-date")
                if date:
                    df.loc[i, 'date'] = date.get_text()
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/{base_url.split("//")[-1].split(".")[0]}.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            # Ensure required columns exist before dropping duplicates
            for col in ['header', 'tagline', 'date']:
                if col not in combined_df.columns:
                    combined_df[col] = ""
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        pdb.set_trace()
        combined_df.to_parquet(parquet_path, index=False)

#--------------------------------------------------------------------------------------------------
    def parse_aljazeera(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://www.aljazeera.com/"
        df = self.create_columns(df)
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # find header
                header = soup.find(class_= 'breadcrumbs')
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find(class_ = 'article-subhead')
                if tagline and hasattr(tagline, '__getitem__') and tagline[0]:
                    em_tagline = tagline[0].find('em')
                    if em_tagline:
                        df.loc[i, "tagline"] = em_tagline.get_text(strip=True)
                date = soup.find(class_ = "screen-reader-text")
                # find date
                if date:
                    df.loc[i, 'date'] = date.get_text()
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/{base_url.split("//")[-1].split(".")[0]}.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)
#--------------------------------------------------------------------------------------------------
    def parse_ap(self, df):
        counter = 0
        df = self.create_columns(df)
        df = df.reset_index(drop=True)
        base_url = "https://apnews.com/"
        # Iterate over all rows in the DataFrame
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            response = requests.get(full_link)
            if response.status_code == 200:
                counter += 1
                soup = BeautifulSoup(response.content, 'html.parser')
                # find header
                header = soup.find(class_ = 'Page-headline')
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                # find tagline
                tagline = soup.find_all("p", class_ ='RichTextStoryBody RichTextStory')
                if tagline[0]:
                    df.loc[i, "tagline"] = tagline[0].get_text(strip=True)
                # find date
                soup = soup.find('span', attrs={'data-date': ''})
                date = soup.find("span")
                if date:
                    df.loc[i, 'date'] = date.get_text()
                else: 
                    df.loc[i, 'date'] = str(datetime.now())
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")
        parquet_path = f'Data/{base_url.split("//")[-1].split(".")[0]}.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)
#--------------------------------------------------------------------------------------------------
    def parse_generic(self, df, base_url, header_tag, tagline_tag, date_class):
        df = self.create_columns(df)
        # Collect new rows in a list
        new_rows = []
        for i, row in df.iterrows():
            link = row.get('hrefs', None)
            # Skip empty, fragment, or mailto/javascript links
            if not link or str(link).startswith('#') or str(link).startswith('mailto:') or str(link).startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            full_link = urljoin(base_url, str(link))
            response = requests.get(full_link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                header = soup.find(header_tag)
                if header:
                    df.loc[i, "header"] = header.get_text(strip=True)
                tagline = soup.find(tagline_tag)
                if tagline:
                    df.loc[i, "tagline"] = tagline.get_text(strip=True)
                date = soup.find(class_=date_class)
                if date:
                    df.loc[i, 'date'] = date.get_text()
                new_rows.append(df.iloc[i])
            else:
                print(f"Failed to fetch {link}, status code: {response.status_code}")

        # After the loop
        parquet_path = f'Data/{base_url.split("//")[-1].split(".")[0]}.parquet'
        if os.path.exists(parquet_path):
            existing_df = pd.read_parquet(parquet_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['header', 'tagline', 'date'], keep='last')
        else:
            combined_df = df
        combined_df.to_parquet(parquet_path, index=False)
