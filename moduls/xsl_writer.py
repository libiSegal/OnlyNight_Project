import openpyxl


def insert_westerns_into_excel(rooms):
    filename = 'rooms.xlsx'
    try:
        wb = openpyxl.load_workbook(filename)
        sheet = wb.active
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'Rooms'
        headers = ['Price', 'Desc', 'SysCode', 'CheckIn', 'CheckOut', 'Nights', 'BToken', 'Remarks', 'Limit date',
                   'Meal plan code', 'Meal plan desc']
        sheet.append(headers)

    for room in rooms:
        encoded_western = []
        for item in room:
            if isinstance(item, str):
                try:
                    encoded_western.append(item.encode('utf-8').decode('utf-8'))
                except UnicodeEncodeError:
                    encoded_western.append(item.encode('ascii', 'ignore').decode('utf-8'))
            else:
                encoded_western.append(item)
        sheet.append(encoded_western)

    wb.save(filename)
