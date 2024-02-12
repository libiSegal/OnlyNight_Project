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


one_hotel_information_request("‡553248635212849588‡AE.DUBAI‡hb5‡64219‡2024-02-15‡1‡USD‡‡ROO.RO-2‡Room Run Of House‡‡135_8925_SQ1432_SR1412‡BB‡‡‡‡‡‡‡‡‡‡‡‡‡‡SxAJSZgqt6GnNq16I8nW1A==‡O2A0C‡‡2‡0‡0‡0‡1‡‡‡‡‡0‡0‡1‡DUBAI‡DIFC‡‡FreeCordinanats‡25.2048493‡55.2707828‡5‡Swissotel Al Murooj Dubai‡20240215|20240216|W|148|64219|ROO.RO-2|ID_B2B_44|BB|B2CXXXX|1~2~0||N@06~A-SIC~209159~-1713486655~N~~~NOR~31D2DE0BAA4A469170773423988805AAIL07500690063001508209159‡‡‡25.202826‡55.2757709‡BEPRO‡N‡hbed.en.AE.64219.‡138‡135‡IL‡AE‡‡")
