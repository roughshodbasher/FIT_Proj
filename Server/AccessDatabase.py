import mysql.connector
import json


# get vehicle information by rego
#{"type": 1, "name": "Database", "data": {"method": "get", "command": "vehicle_info", "rego": "vehicle registration number"}}}
# get vehicle trip by rego
#{"type": 1, "name": "Database", "data": {"method": "get", "command": "vehicle_trip", "rego": "vehicle registration number"}}}


#{"type": 1, "name": "Database", "data": {"method": "get", "command": "emission"}}}
#{"type": 1, "name": "Database", "data": {"method": "post", "command": "add_vehicle", "vin":"", "make": "",
# "rego": "", "year": "", "fuel_consumption": "", "kilometers": "", "engine":""}}}





def connect_to_db():
    cnx = mysql.connector.connect(user='root', password='',
                                  host='localhost',
                                  database='fitproj')
    return cnx


def handle_db_request(request):
    method = request["method"]
    command = request["command"]

    if method == "get":
        if command == "vehicle_info":
            return get_vehicle_info(request["rego"])
        elif command == "all_vehicle_info":
            return get_all_vehicle()
        # call appropriate function based on request
    elif method == "post":
        if command == "add_vehicle":
            add_vehicle(request)
        pass
        # add things to the database


def get_vehicle_info(rego):
    con = connect_to_db()
    cursor = con.cursor()
    # query: select from db, information about the vehicle
    query = "select * from fitproj.Vehicle where registration = %s"

    param = (rego, )
    cursor.execute(query, param)
    fetchresults = cursor.fetchall()
    colnames = [x[0] for x in cursor.description]
    cursor.close()
    con.close()
    return make_json(fetchresults, colnames)
    return info


def get_all_vehicle():
    con = connect_to_db()
    cursor = con.cursor()
    query = "select * from fitproj.Vehicle"

    cursor.execute(query)
    fetchresults = cursor.fetchall()
    colnames=[x[0] for x in cursor.description]
    cursor.close()
    con.close()
    return make_json(fetchresults, colnames)


def make_json(fetchresults, colnames):
    to_return = []
    for results in fetchresults:
        to_return.append(dict(zip(colnames, results)))
    return json.dumps(to_return)



def get_trip_by_rego():
    con = connect_to_db()
    # execute query and process data here

    con.close()


def get_emission():
    pass


def add_trip(trip):
    pass

def add_vehicle(data):
    pass
