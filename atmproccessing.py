import requests
from geopy.geocoders import Nominatim


def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(address)
    if location is None:
        return None, None
    return location.latitude, location.longitude

def process_atms(address, radius):
    latitude, longitude = get_coordinates(address)

    url = f"http://api.nessieisreal.com/atms?lat={latitude}&lng={longitude}&rad={radius}&key=e1cac451319e9263333280ff4a5b28f6"

    response = requests.get(url)
    data = response.json()

    # Sort the ATMs based on their distance from the user's location
    sorted_atms = sorted(data['data'], key=lambda x: x['geocode']['lat'])

    # Retrieve the top 3 closest ATMs (ensuring they are different)
    top_3_atms = []
    for atm in sorted_atms:
        if len(top_3_atms) == 3:
            break
        atm_address = atm['address']
        full_address = f"{atm_address['street_number']} {atm_address['street_name']}, {atm_address['city']}, {atm_address['state']}, {atm_address['zip']}"
        if full_address not in [a['address'] for a in top_3_atms]:
            top_3_atms.append({'address': full_address, 'geocode': atm['geocode']})

    return top_3_atms

def get_top_3_atms(address, radius):
    latitude, longitude = get_coordinates(address)
    if latitude is None or longitude is None:
        return []

    url = f"http://api.nessieisreal.com/atms?lat={latitude}&lng={longitude}&rad={radius}&key=e1cac451319e9263333280ff4a5b28f6"

    response = requests.get(url)
    data = response.json()

    # Sort the ATMs based on their distance from the user's location
    sorted_atms = sorted(data['data'], key=lambda x: x['geocode']['lat'])

    # Retrieve the top 3 closest ATMs (ensuring they are different)
    top_3_atms = []
    for atm in sorted_atms:
        if len(top_3_atms) == 3:
            break
        atm_address = atm['address']
        full_address = f"{atm_address['street_number']} {atm_address['street_name']}, {atm_address['city']}, {atm_address['state']}, {atm_address['zip']}"
        if full_address not in [a['address'] for a in top_3_atms]:
            top_3_atms.append({'address': full_address, 'geocode': atm['geocode']})

    return top_3_atms

