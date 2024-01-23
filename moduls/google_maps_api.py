import requests


def get_geo_code(place):
    api_key = "AIzaSyCcsqWN49bqMFOO2lekiixxC6eUzxuJhG4"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None


geo_code_exe = {
    "Latitude": "52.52000659999999",
    "Longitude": "13.404954",
    "PIP": "N"
}

# Example usage
place_name = "Eiffel Tower, Paris, France"
geo_code = get_geo_code(place_name)
if geo_code:
    latitude, longitude = geo_code
    print(f"The coordinates of {place_name} are: ({latitude}, {longitude})")
else:
    print(f"Failed to get the coordinates of {place_name}")
