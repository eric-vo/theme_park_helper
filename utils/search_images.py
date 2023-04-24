import os

from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch

# Load the Google Custom Search API key and CX from the .env file
load_dotenv()
GCS_DEV_KEY = os.getenv('GCS_DEV_KEY')
GCS_CX = os.getenv('GCS_CX')

# Set up the Google Custom Search client
gis = GoogleImagesSearch(GCS_DEV_KEY, GCS_CX)
search_params = {
    'num': 1,
    'fileType': 'jpg|gif|png',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|' +
              'cc_noncommercial|cc_nonderived'
}


def search_images(query: str) -> str:
    """Searches for the first image of the query.

    Parameters
    ----------
    query : str
        What to search for

    Returns
    -------
    str
        The URL of the first image result
    """
    # Set the query
    search_params['q'] = query

    # Search for images of the query
    gis.search(search_params=search_params)

    # Return the URL of the first result
    for image in gis.results():
        return image.url
