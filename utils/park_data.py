import requests


def get_park_data(park_id: int) -> dict:
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


def ride_id_to_name(park_id: int, ride_id: int) -> str:
    match = None
    
    for land in get_park_data(park_id)['lands']:
        for ride in land['rides']:
            if ride['id'] == ride_id:
                match = ride['name']
                break
    
    if match is None:
        for ride in get_park_data(park_id)['rides']:
            if ride['id'] == ride_id:
                match = ride['name']
                break

    return match


def ride_name_to_id(park_id: int, ride_name: str) -> int:
    match = None
    
    for land in get_park_data(park_id)['lands']:
        for ride in land['rides']:
            if ride['name'] == ride_name:
                match = ride['is']
                break
    
    if match is None:
        for ride in get_park_data(park_id)['rides']:
            if ride['name'] == ride_name:
                match = ride['is']
                break

    return match


def park_id_to_name(park_id: int) -> str:
    if park_id == 16:
        return "Disneyland Park"
    elif park_id == 17:
        return "Disney California Adventure"
    
    return None


def park_name_to_id(park_name: str) -> int:
    if park_name.lower() == "disneyland park":
        return 16
    elif park_name.lower() == "disney california adventure":
        return 17
    
    return None