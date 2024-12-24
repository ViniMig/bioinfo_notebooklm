import requests

from constants import BMC_API_KEY


def retrieve_bmc_paper():  # -> str:
    """Builds a query with personal API and a few settings
    such as:
      journal ISSN: for BMC Bioinformatics specifically;
      MAX_RESULTS: corresponds to the 'p' setting in BMC API
      START_RESULT_INDEX: corresponds to the 's' setting in BMC API

    and retrieves the most recent json result (using API default behaviour,
    by not setting date options in the query).

    Returns the link to the full paper as a string. 
    """
    # Setup query parameters
    BMC_BIOINFORMATICS_ISSN = "1471-2105"
    MAX_RESULTS = 1
    START_RESULT_INDEX = 1

    url = f'https://api.springernature.com/meta/v2/json?api_key={BMC_API_KEY}&callback=&s={
        START_RESULT_INDEX}&p={MAX_RESULTS}&q=(issn:{BMC_BIOINFORMATICS_ISSN})'

    response = requests.request("GET", url)
    result = response.json()

    paper_url = result['records'][0]['url'][0]['value']

    return paper_url
