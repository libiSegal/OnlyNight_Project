import requests
import json


def one_hotel_information_request(room_token):
    url = "https://pub_srv.beprotravel.net/BePro/api/Hotels/Information"

    payload = json.dumps({
        "Query": {
            "Command": 1,
            "LanguageCode": "en",
            "RoomBToken": room_token,
            "ResultMode": "Json",
            "MaxMilliSecondsTimeToWait": 60000
        },
        "LanguageCode": "en"
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic Qz0zOkQ9MTpCPTUyNDpVPTcyMTQ6UD01NEIzOUE1'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response



