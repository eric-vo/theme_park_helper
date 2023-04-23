import requests


def get_park_data(park_id: int):
    """Gets the data for the specified park from the Queue-Times API.

    Parameters
    ----------
    park_id : int
        The ID of the park to get data for

    Returns
    -------
    dict
        The data for the park
    """
    return requests.get(
        f'https://queue-times.com/en-US/parks/{park_id}/queue_times.json'
    ).json()
