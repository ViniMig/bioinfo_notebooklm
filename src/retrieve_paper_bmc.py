import requests

def retrieve_bmc_paper() -> str:
    """Retrieve the most recent result from biorxiv API.
    Returns the link to the full paper as a string. 
    """
    url = 'https://api.biorxiv.org/details/biorxiv/1'
    response = requests.request("GET", url)
    result = response.json()
    article = result["collection"][0]
    paper_url = f"https://www.biorxiv.org/content/{article["doi"]}v{article["version"]}.full.pdf"

    return paper_url