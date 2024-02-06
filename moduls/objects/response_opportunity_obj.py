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


class ResponseOpportunityRoom:
    body = {
        "RoomId": int,
        "Desc": str,
        "Price": float,
        "SysCode": str,
        "NumAdt": int,
        "NumCnn": int,
        "CnnAge": [],
        "CheckIn": str,
        "CheckOut": str,
        "Nights": int,
        "Remarks": str,
        "LimitDate": str,
        "BToken": str,
        "MetaData": {
            "Code": str,
            "Desc": str
        }
    }

    def __init__(self):
        self.body["RoomId"] = type[int]
        self.body["Desc"] = type[str]
        self.body["Price"] = type[float]
        self.body["SysCode"] = type[str]
        self.body["NumAdt"] = 2
        self.body["NumCnn"] = 0
        self.body["CnnAge"] = []
        self.body["CheckIn"] = type[str]
        self.body["CheckOut"] = type[str]
        self.body["Nights"] = type[int]
        self.body["BToken"] = type[str]
        self.body["LimitDate"] = type[str]
        self.body["Remarks"] = type[str]
        self.body["MetaData"]["Code"] = type[str]
        self.body["MetaData"]["Desc"] = type[str]

    def fill_obj(self, room_id, price, desc, sys_code, check_in, check_out, nights, token,
                 limit_date, remarks, meal_plan_code, meal_plan_desc):
        self.body["RoomId"] = room_id
        self.body["Desc"] = desc
        self.body["Price"] = price
        self.body["SysCode"] = sys_code
        self.body["NumAdt"] = 2
        self.body["NumCnn"] = 0
        self.body["CnnAge"] = []
        self.body["CheckIn"] = check_in
        self.body["CheckOut"] = check_out
        self.body["Nights"] = nights
        self.body["BToken"] = token
        self.body["LimitDate"] = limit_date
        self.body["Remarks"] = remarks
        self.body["MetaData"]["Code"] = meal_plan_code
        self.body["MetaData"]["Desc"] = meal_plan_desc

    def add_desc(self, desc):
        self.body["Desc"] = desc


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
