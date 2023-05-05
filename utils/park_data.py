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
    for land in get_park_data(park_id)['lands']:
        for ride in land['rides']:
            if ride['id'] == ride_id:
                return ride['name']
    
    for ride in get_park_data(park_id)['rides']:
        if ride['id'] == ride_id:
            return ride['name']


def ride_name_to_id(park_id: int, ride_name: str) -> int:
    for land in get_park_data(park_id)['lands']:
        for ride in land['rides']:
            if ride['name'].lower() == ride_name.lower():
                return ride['id']
    
    for ride in get_park_data(park_id)['rides']:
        if ride['name'].lower() == ride_name.lower():
            return ride['id']


def park_id_to_name(park_id: int) -> str:
    if park_id == 16:
        return "Disneyland Park"
    elif park_id == 17:
        return "Disney California Adventure"


def park_name_to_id(park_name: str) -> int:
    if park_name.lower() == "disneyland park":
        return 16
    elif park_name.lower() == "disney california adventure":
        return 17
    

def is_ride_open(park_id: int, ride_id: int) -> bool:
    for land in get_park_data(park_id)['lands']:
        for ride in land['rides']:
            if ride['id'] == ride_id:
                return ride['is_open']
    
    for ride in get_park_data(park_id)['rides']:
        if ride['id'] == ride_id:
            return ride['is_open']


def get_ride_wait_time(park_id: int, ride_id: int) -> int:
    for land in get_park_data(park_id)['lands']:
        for ride in land['rides']:
            if ride['id'] == ride_id:
                return ride['wait_time']
    
    for ride in get_park_data(park_id)['rides']:
        if ride['id'] == ride_id:
            return ride['wait_time']