class ResponseOpportunityImg:
    body = {
        "Desc": str,
        "ImageLink": str
    }

    def __init__(self, desc, image_link):
        self.body["Desc"] = desc
        self.body["ImageLink"] = image_link


class ResponseOpportunityItem:
    body = {
        "Id": int,
        "Name": str,
        "Code": str,
        "Stars": float,
        "AddressInfo": {
            "Address": str,
            "Phone": str,
            "Fax": str,
            "City": str,
            "Country": str
        },
        "Position": {
            "Latitude": str,
            "Longitude": str,
            "PIP": str
        },
        "Images": [],
    }

    def __init__(self):
        self.body["Id"] = type[int]
        self.body["Name"] = type[str]
        self.body["Code"] = type[str]
        self.body["Stars"] = type[float]
        self.body["AddressInfo"]["Address"] = type[str]
        self.body["AddressInfo"]["Phone"] = type[str]
        self.body["AddressInfo"]["Fax"] = type[str]
        self.body["AddressInfo"]["City"] = type[str]
        self.body["AddressInfo"]["Country"] = type[str]
        self.body["Position"]["Latitude"] = type[str]
        self.body["Position"]["Longitude"] = type[str]
        self.body["Position"]["PIP"] = type[str]

    def validate_data(self, *args):
        self.body["Id"] = args[0]
        self.body["Name"] = args[1]
        self.body["Code"] = args[2]
        self.body["Stars"] = args[3]
        self.body["AddressInfo"]["Address"] = args[4]
        self.body["AddressInfo"]["City"] = args[5]
        self.body["AddressInfo"]["Country"] = args[6]
        if len(args) == 10:
            self.body["AddressInfo"]["Phone"] = type[str]
            self.body["AddressInfo"]["Fax"] = type[str]
            self.body["Position"]["Latitude"] = args[7]
            self.body["Position"]["Longitude"] = args[8]
            self.body["Position"]["PIP"] = args[9]
        elif len(args) == 11:
            self.body["AddressInfo"]["Phone"] = args[7]
            self.body["AddressInfo"]["Fax"] = type[str]
            self.body["Position"]["Latitude"] = args[8]
            self.body["Position"]["Longitude"] = args[9]
            self.body["Position"]["PIP"] = args[10]
        else:
            self.body["AddressInfo"]["Phone"] = args[7]
            self.body["AddressInfo"]["Fax"] = args[8]
            self.body["Position"]["Latitude"] = args[9]
            self.body["Position"]["Longitude"] = args[10]
            self.body["Position"]["PIP"] = args[11]

    def add_images(self, images: list):
        self.body["Images"] = images


class ResponseOpportunityHotel:
    body = {
        "Item": {},
        "Rooms": []
    }

    def __init__(self, item, rooms):
        self.body["Item"] = item
        self.body["Rooms"] = rooms


class ResponseOpportunity:
    body = {
        "Hotels": []
    }

    def __init__(self, hotels):
        self.body["Hotels"] = hotels
