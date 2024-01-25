import requests
import json

url = "https://pub_srv.beprotravel.net/BePro/api/Hotels/Information"

payload = json.dumps({
  "Query": {
    "Command": 1,
    "LanguageCode": "en",
    "RoomBToken": "‡536‡DE.BERLIN‡hb5‡277678‡2024-01-16‡2‡EUR‡‡DBL.DB-2‡Double With Double Bed‡‡‡RO‡‡‡‡‡‡‡‡‡‡‡‡‡‡QIw94l6Cz6LGjomSHBmFvA==‡O2A0C‡‡2‡0‡0‡0‡1‡‡‡1‡‡0‡0‡1‡BERLIN‡Berlin‡‡FreeCordinanats‡52.52000659999999‡13.404954‡8‡25hours Hotel Bikini Berlin‡20240116|20240118|W|202|277678|DBL.DB-2|ID_B2B_20|RO|RA3B2BHB|1~2~0||N@06~A-SIC~200117~795003773~N~~~NRF~FDFB22C510E3442170480294393505AAIL07500860081001308233f3‡‡‡52.50556‡13.33783‡BEPRO‡N‡hbed.en.DE.277678.‡0‡135‡IL‡DE‡‡",
    "HotelInfo": {
      "UniqueKey": "8db24d5a",
      "ProductTypeCode": "HTL"
    },
    "ResultMode": "Json",
    "MaxMilliSecondsTimeToWait": 60000
  },
  "LanguageCode": "en"
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Basic Qz17e0NPTVBBTll9fTpEPXt7REVQQVJUTUVOVH19OkI9e3tCUkFOQ0h9fTpVPXt7VVNFUn19OlA9e3tQQVNTV09SRH19'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
