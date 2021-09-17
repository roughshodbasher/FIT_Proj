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
    try:
        cnx = mysql.connector.connect(user='root', password='',
                                      host='localhost',
                                      database='fitproj')
        return True, cnx
    except:
        result = {}
        result["status"] = 500
        result["message"] = "Cannot connect to the database"
        return False, result


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
        elif command == "login":
            return login(request)

        # add things to the database


def get_vehicle_info(rego):
    """
    This function takes in a string, rego, this will be the registration of a vehicle, and gets all the data relevant
    to the vehicle and return it as a json string.
    :param rego: string, vehicle registration number
    :return: json response
    if the call was successful, then this function returns a json in the form
    {status: 200, message: [{"registration": registration of vehicle, "vin": vin of vehicle, "veh_type_id": vehicle type
    id stored in the database}]}

    else:
    if the call was unsuccessful:
    if error connecting with database, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}

    if there is problem with the registration number, then it returns:
    {"status": 400, "message": "Invalid registration number"}
    """
    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # execute the query if connection is available
    if is_connected:
        cursor = con.cursor()

        # query: select from db, information about the vehicle
        query = "select * from fitproj.Vehicle where registration = %s"

        param = (rego, )
        # execute query
        cursor.execute(query, param)
        # fetch the results
        fetch_results = cursor.fetchall()

        # if not result returned when looking up the vehicle with registration = rego, then return error message
        if not fetch_results:
            response = {}
            response["status"] = 400
            response["message"] = "Invalid registration number"
            return json.dumps(response)

        colnames = [x[0] for x in cursor.description]   # get the column names
        # close connection and cursor
        cursor.close()
        con.close()
        # call make_json to combine the column names and the data and return the final result as a json string
        return make_json(fetch_results, colnames, 200)

    # else, immediate return the error message
    else:
        return json.dumps(con)


def get_all_vehicle():
    """
    This function gets the registration number of all the vehicles in the database
    :return: json response
    if the call was successful, then this function returns a json in the form
    {status: 200, message: [{"registration": "Plate number"} ... {"registration": "Plate number"}]}
    else:
    if the call was unsuccessful, if error connecting with database, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}
    """
    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # execute the query if connection is available
    if is_connected:
        cursor = con.cursor()
        query = "select registration from fitproj.Vehicle"

        # execute query
        cursor.execute(query)
        # fetch results
        fetch_results = cursor.fetchall()
        # get the column names of the results, this will be used as key in the json response
        colnames=[x[0] for x in cursor.description]
        # close the cursor and connection
        cursor.close()
        con.close()
        # call make_json to generate the json response with all the data
        return make_json(fetch_results, colnames, 200)

    # else, immediate return the error message
    else:
        return json.dumps(con)


def make_json(fetchresults, colnames, status):
    """
    This is a function that combines the results returned from the database, and the status code of the query into
    a single json string
    :param fetchresults: this contains the actual data returned by the query
    :param colnames: the columns names, this will be used as keys in the json string
    :param status: status code
    :return: json string, in the form,
    {"status": int, "message": [array containing each row returned]}
    """
    response = {}
    response["status"] = status
    to_return = []
    response["message"] = to_return
    # for each row in the fetchresults, add to the array
    for results in fetchresults:
        to_return.append(dict(zip(colnames, results)))
    return json.dumps(response)



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


def login(data):
    login_id = data["login_id"]
    password = data["password"]
    res = {}
    con = connect_to_db()
    cursor = con.cursor()
    query = "select user_id from fitproj.Users where loginID = %s and BINARY password = %s;"
    param = (login_id, password,)
    cursor.execute(query, param)
    fetchresults = cursor.fetchall()
    if not fetchresults:
        res["status"] = "error"
        res["response"] = "wrong login id or password"
    else:
        user_id = fetchresults[0][0]
        res["status"] = "success"
        res["response"] = user_id
    cursor.close()
    con.close()
    return json.dumps(res)