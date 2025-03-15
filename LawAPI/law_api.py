# https://justopinion.readthedocs.io/en/latest/guides/getting_started.html#selecting-text-from-an-opinion
# https://medium.datadriveninvestor.com/legal-and-justice-related-python-libraries-d3888c08768a
import os
from justopinion import CAPClient
import requests
client = CAPClient(api_token='49eb70bc06a32b6ec66b336ddcb5d68a6d010214')
#49eb70bc06a32b6ec66b336ddcb5d68a6d010214


#examples of how to use the API library
oracle_download = client.fetch(query="750 F.3d 1339")
#oracle_case = client.read_cite("750 F.3d 1339", full_case=True)

oracle_download

oracle_data = oracle_download.json()
oracle_data["results"][0]["name"]

case_names = oracle_data["results"][0]["cites_to"]


oracle_download = client.fetch(query="750 F.3d 1339")
oracle_data["results"][0]["name"]

def citations():
    citations = []
    for case in case_names:
        citations.append(case["cite"])
    print(citations)


def find_citations(citations):
	case_laws = []
	for case in citations:
		json_obj = client.fetch(query = case)
		obj = json_obj.json()
		obj ["results"][0]["name"]
		case_laws.append(obj ["results"][0]["name"])

		print (case_names [0]["cite"])
	return case_laws



#everything past here is sorta extraneous
oracle = client.read_decision_from_response(oracle_download)
oracle.name_abbreviation

oracle.opinions[0].type

thornton = client.read_cite("1 Breese 34", full_case=True)

thornton = client.read_cite("1 Breese 34", )

thornton

thornton.citations[0]

text_selection = thornton.opinions #[0].select_text([(0, 100), (312, 359)])

text_selection

parties = thornton.casebody.data.parties[0]
print(f"Parties: {parties}")


#this is our code example for pulling data from the law library
def example():
	oracle_download = client.fetch(query="750 F.3d 1339")
	#oracle_case = client.read_cite("750 F.3d 1339", full_case=True)
	print(oracle_download)

if __name__ == "__main__":
	citations()
	find_citations()

