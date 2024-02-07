import requests


def get_geo_code(place):
    api_key = "AIzaSyCcsqWN49bqMFOO2lekiixxC6eUzxuJhG4"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"

    response = requests.get(url, verify=False)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return {
            "latitude": latitude,
            "longitude": longitude,
            "PIP": "N"
        }
    else:
        return None




# print(get_geo_code("Netanya IL"))