from datetime import datetime


class OpportunityData:
    room_id: str
    hotel_id: str
    price: float
    desc: str
    sysCode: str
    check_in: datetime
    check_out: datetime
    nights: int
    b_token: str
    remarks: str
    limit_date: datetime
    code: str
    code_description: str

    def __init__(self, room_id, hotel_id, price, desc, sys_code, check_in, check_out, nights, b_token, remarks,
                 limit_date, code,
                 code_description):
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.price = price
        self.desc = desc
        self.sysCode = sys_code
        self.check_in = check_in
        self.check_out = check_out
        self.nights = nights
        self.b_token = b_token
        self.remarks = remarks
        print("remarks: " + remarks)
        self.limit_date = limit_date
        self.code = code
        self.code_description = code_description
