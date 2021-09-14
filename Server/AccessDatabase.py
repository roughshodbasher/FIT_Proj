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
        elif command == "trip":
            return get_trip(request)
        # call appropriate function based on request
    elif method == "post":
        if command == "add_vehicle":
            return add_vehicle(request)
        elif command == "add_truck_by_type":
            return add_truck_by_type(request)

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
    try:
        vin = data["vin"]
        make = data["make"]
        registration = data["rego"]
        year = data["year"]
        fuel_cons = data["fuel_consumption"]
        model = data["model"]
        kilometers = data["kilometers"]
        engine = data["engine"]
        fuel_type = data["fuel_type"]
        emission = data["emission"]

        con = connect_to_db()
        cursor = con.cursor()
        query = "select veh_id from fitproj.VehicleType where yr = %s and make = %s and model = %s"

        param = (year, make, model,)
        cursor.execute(query, param)
        fetchresults = cursor.fetchall()
        if fetchresults == []:
            new_type_query = "insert into fitproj.VehicleType (make, model, yr, fuel_type, fuel_cons, emissions, eng, trucktype) " \
                             "values(%s, %s, %s, %s, %s, %s, %s, NULL)"
            param1 = (make, model, year, fuel_type, fuel_cons, emission, engine)
            cursor.execute(new_type_query, param1,)
            con.commit()
            cursor.execute(query, param)
            veh_type_id = cursor.fetchall()[0][0]
        else:
            veh_type_id = fetchresults[0][0]

        # insert vehicle in the vehicle table
        new_veh_query = "insert into fitproj.Vehicle (registration, vin, veh_type_id) values (%s, %s, %s)"
        param2 = (registration, vin, veh_type_id)
        cursor.execute(new_veh_query, param2)
        con.commit()
        cursor.close()
        con.close()
        return json.dumps("success")
    except:
        return json.dumps("error")


def add_truck_by_type(data):
    try:
        vin = data["vin"]
        registration = data["rego"]
        fuel_cons = data["fuel_consumption"]
        emission = data["emission"]
        trucktype = data["trucktype"]

        con = connect_to_db()
        cursor = con.cursor()
        query = "select veh_id from fitproj.VehicleType where trucktype = %s"

        param = (trucktype, )
        cursor.execute(query, param)
        fetchresults = cursor.fetchall()
        if fetchresults == []:
            new_type_query = "insert into fitproj.VehicleType (make, model, yr, fuel_type, fuel_cons, emissions, eng, trucktype) " \
                             "values(NULL, NULL, NULL, NULL, %s, %s, NULL, %s)"
            param1 = (fuel_cons, emission, trucktype,)
            cursor.execute(new_type_query, param1)
            con.commit()
            cursor.execute(query, param)
            veh_type_id = cursor.fetchall()[0][0]
        else:
            veh_type_id = fetchresults[0][0]

        # insert vehicle in the vehicle table
        new_veh_query = "insert into fitproj.Vehicle (registration, vin, veh_type_id) values (%s, %s, %s)"
        param2 = (registration, vin, veh_type_id, )
        cursor.execute(new_veh_query, param2)
        con.commit()
        cursor.close()
        con.close()
        return json.dumps("success")
    except:
        return json.dumps("error")



def get_trip(data):
    con = connect_to_db()
    cursor = con.cursor()
    start_d = data["start"]
    end_d = data["end"]
    query = "select * from fitproj.Trips where date >= %s and date <= %s;"

    param = (start_d, end_d, )
    cursor.execute(query, param)
    fetchresults = cursor.fetchall()
    new_results = []
    for r in fetchresults:
        date = r[6]
        date.strftime('%m/%d/%Y')
        new_results.append((r[0], r[1], r[2], r[3], r[4], r[5], str(date), r[7]))
    colnames = [x[0] for x in cursor.description]
    cursor.close()
    con.close()
    return make_json(new_results, colnames)