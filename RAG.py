# Methods for RAG

# Import Statements
from bs4 import BeautifulSoup
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import nest_asyncio
import requests
import os

from llama_parse import LlamaParse
#nest_asyncio.apply()
from llama_index import SimpleDirectoryReader


# getting the keys from .env
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LLAMAPARSE_API_KEY = os.getenv('LLAMAPARSE_API_KEY')
ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY")


embed_model = "local:BAAI/bge-small-en-v1.5" #https://huggingface.co/collections/BAAI/bge-66797a74476eb1f085c7446d

documents = " "

vector_index_std = VectorStoreIndex(documents, embed_model = embed_model)


llm_gpt35 = OpenAI(model="gpt-3.5-turbo", api_key = OPENAI_API_KEY)
query_engine_gpt35 = vector_index_std.as_query_engine(similarity_top_k=3, llm=llm_gpt35)

llm_gpt4o = OpenAI(model="gpt-4o", api_key = OPENAI_API_KEY)
query_engine_gpt4o = vector_index_std.as_query_engine(similarity_top_k=3, llm=llm_gpt4o)


tokenizer = Anthropic().tokenizer
Settings.tokenizer = tokenizer

llm_claude = Anthropic(model="claude-3-5-sonnet-20240620", api_key=ANTHROPIC_API_KEY)
query_engine_claude = vector_index_std.as_query_engine(similarity_top_k=3, llm=llm_claude)



# query function
def q(query1, **kwargs):
	headline = kwargs.get("headline")
	tagline = kwargs.get("tagline")
	query1 = "Is this news story about politics or global events?"
	response = query_engine_gpt35.query(query1)

	if response == "yes":
		return True
	
	return False

	#print("GPT-3.5 Turbo")
	#print(str(response))






