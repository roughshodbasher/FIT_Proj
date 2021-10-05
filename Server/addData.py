import xlrd
import random, string
import json
from random import randint
import datetime




def rego_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

myfl = xlrd.open_workbook("All Data.xlsx")  # file path can be different
'''urban car'''
sheet = myfl.sheet_by_index(1)

for i in range(1, sheet.nrows):
    data = sheet.row_values(i)

    json_data = {}
    json_data["vin"] = rego_generator(15, string.digits)
    json_data["rego"] = rego_generator()
    json_data["year"] = int(data[2])
    json_data["fuel_consumption"] = 0
    json_data["model"] = data[1]
    json_data["make"] = data[0]
    json_data["engine"] = "0"
    json_data["fuel_type"] = "PETROL"
    json_data["emission"] = int(data[3])

    # idntknow how to call this
    add_vehicle(json_data)



'''trucks by type'''
sheet = myfl.sheet_by_index(2)

for i in range(1, sheet.nrows):
    data = sheet.row_values(i)

    json_data = {}
    json_data["vin"] = rego_generator(15, string.digits)
    json_data["rego"] = rego_generator()
    json_data["fuel_consumption"] = int(data[1])
    json_data["trucktype"] = data[0]
    json_data["emission"] = int(data[2])

    # idntknow how to call this
    add_truck_by_type(json_data)


def date_generator(yr_str = 2021, yr_en = 2021, mn_st = 8, mn_en = 10, dy_st = 1, dy_en = 30):
    date = datetime.date(randint(yr_str,yr_en), randint(mn_st, mn_en), randint(dy_st, dy_en))
    return date
#
def creating_random_trips():
    data = {"method": "get", "command": "all_vehicle_info"}
    response = json.loads(handle_db_request(data))

    vehicles = response["message"]

    suburbs = ['South Yarra', 'St Kilda', 'Carlton', 'Brunswick', 'Footscray', 'Fitzroy', 'Richmond', 'South Melbourne', 'East Melbourne', 'Clayton', 'Carneigie']

    for _ in range(30):
        trip = {}
        trip["user_id"] = random.randint(1, 2) #between user 1 and 2
        # get a random vehicle
        random_veh = get_vehicle_info(vehicles[random.randint(0, len(vehicles)-1)]["registration"])
        random_veh_rego = json.loads(random_veh)["message"][0]["registration"]
        trip["veh_reg"] = random_veh_rego
        trip["start"] = suburbs[random.randint(0, len(suburbs)-1)]
        trip["end"] = suburbs[random.randint(0, len(suburbs)-1)]
        trip["distance"] = random.randint(10, 30)
        trip["date"] = str(date_generator())
        add_trip(trip)

creating_random_trips()