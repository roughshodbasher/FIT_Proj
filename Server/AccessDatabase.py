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
    """
    This function connects to the database
    :return: a tuple
    if the connection was successful, then return:
    (True, the connection)
    else:
    return (False, error message which is to be returned)
    """
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
    """
    This function takes in a json and execute relevant function based on the command in the json request
    :param request: json
    :return: json, contains the status code and message of the query
    """
    method = request["method"]
    command = request["command"]

    # execute the relevant function based on the query
    # get data from the database
    if method == "get":
        # get the information of a particular vehicle
        if command == "vehicle_info":
            return get_vehicle_info(request["rego"])
        # get the registration number of all vehicles in the database
        elif command == "all_vehicle_info":
            return get_all_vehicle()
        # get all trips between two dates
        elif command == "trip":
            return get_trip(request)
    elif method == "post":
        # add a vehicle to the database
        if command == "add_vehicle":
            return add_vehicle(request)
        # add a truck to the database, based on type
        elif command == "add_truck_by_type":
            return add_truck_by_type(request)
        # checks login detail of the user
        elif command == "login":
            return login(request)
        # add trip to the database
        elif command == "add_trip":
            return add_trip(request)



def get_vehicle_info(rego):
    """
    This function takes in a string, rego, this will be the registration of a vehicle, and gets all the data relevant
    to the vehicle and return it as a json.
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
        query = "select * from fitproj.Vehicle v join fitproj.VehicleType t on v.veh_type_id = t.veh_id where registration = %s"


        param = (rego, )
        # execute query
        cursor.execute(query, param)
        # fetch the results
        fetch_results = cursor.fetchall()

        # if not result returned when looking up the vehicle with registration = rego, then return error message
        if not fetch_results:
            cursor.close()
            con.close()
            response = {}
            response["status"] = 400
            response["message"] = "Invalid registration number"
            return json.dumps(response)

        colnames = [x[0] for x in cursor.description]   # get the column names
        # close connection and cursor
        cursor.close()
        con.close()
        # call make_json to combine the column names and the data and return the final result as a json
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
    a single json
    :param fetchresults: this contains the actual data returned by the query
    :param colnames: the columns names, this will be used as keys in the json
    :param status: status code
    :return: json, in the form,
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


def add_trip(data):
    """
    This function takes in a json, containing information about a trip, and add the trip to the database
    :param data: json containing the data about the trip to be added
    :return:
    if the trip got inserted to the database successfully, then it returns:
    {"status": 200, "message": "Trip added successfully"}

    else:
    if the call was unsuccessful, if error connecting with database, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}

    if error occurred when inserting the trip, then a generic error message is returned:
    {"status":400, "message":"Error occurred when adding the trip to the database"}    """
    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # if connection to database was successful
    if is_connected:
        try:
            # get the data from the input json "data"
            user_id = data["user_id"]
            veh_reg = data["veh_reg"]
            start = data["start"]
            end = data["end"]
            dist = data["distance"]
            date = data["date"]

            # get the emission information for the vehicle, and calculate the total emission from the trip
            vehicle = json.loads(get_vehicle_info(data["veh_reg"]))
            total_emi = dist * vehicle["message"][0]["emissions"]

            cursor = con.cursor()
            query = "insert into fitproj.Trips (user_id, veh_reg, start, end, dist, date, total_emi) values " \
                    "(%s, %s, %s, %s, %s, %s, %s)"

            param = (user_id, veh_reg, start, end, dist, date, total_emi, )
            # execute query
            cursor.execute(query, param)
            con.commit()
            # close the cursor and connection
            cursor.close()
            con.close()
            # the insertion was successful, return relevant message
            return json.dumps({"status": 200, "message": "Trip added successfully"})
        except:
            # error occurred in the try block when trying to insert the trip, return relevant error message
            return json.dumps({"status":400, "message":"Error occurred when adding the trip to the database"})

    # else, immediate return the error message
    else:
        return json.dumps(con)



def add_vehicle(data):
    """
    This function takes in a json that contains the vehicle information, and add the vehicle to the database
    :param data: json, containing the information for the vehicle, vin, make, registration, year, fuel_cons,
    model, engine, fuel_type, emission
    :return:
    if the insertion was successful, then it returns:
    {"status": 200, "message": "Vehicle added successfully"}

    else:
    if the call was unsuccessful, if error connecting with database, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}

    if error occurred when inserting the vehicle, then a generic error message is returned:
    {"status": 400, "message": "Error occurred when adding the vehicle to the database"}
    """

    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # if connection to database was successful
    if is_connected:
        try:
            # gets the relevant data from the input json
            vin = data["vin"]
            make = data["make"]
            registration = data["rego"]
            year = data["year"]
            fuel_cons = data["fuel_consumption"]
            model = data["model"]
            engine = data["engine"]
            fuel_type = data["fuel_type"]
            emission = data["emission"]

            cursor = con.cursor()

            # get the vehicle id for the vehicle that is about to be inserted based on year, make and model
            query = "select veh_id from fitproj.VehicleType where yr = %s and make = %s and model = %s"

            param = (year, make, model,)
            cursor.execute(query, param)
            fetchresults = cursor.fetchall()

            # if fetchresults == [], then this means that the database doesn't not have the information for the type of
            # the vehicle stored, so create a new vehicle type in the database using the data being passed in
            if fetchresults == []:
                # query to create the new vehicle type
                new_type_query = "insert into fitproj.VehicleType (make, model, yr, fuel_type, fuel_cons, emissions, eng, trucktype) " \
                                 "values(%s, %s, %s, %s, %s, %s, %s, NULL)"
                param1 = (make, model, year, fuel_type, fuel_cons, emission, engine, )
                cursor.execute(new_type_query, param1)
                con.commit()

                # now get the vehicle type id (that was just been inserted)
                cursor.execute(query, param)
                veh_type_id = cursor.fetchall()[0][0]  # get the id
            else:
                # if the type already exist in the database, then get the id from fetchresults
                veh_type_id = fetchresults[0][0]

            # insert the vehicle into the vehicle table, using registration, vin and vehicle type id
            new_veh_query = "insert into fitproj.Vehicle (registration, vin, veh_type_id) values (%s, %s, %s)"
            param2 = (registration, vin, veh_type_id)
            cursor.execute(new_veh_query, param2)
            con.commit()
            cursor.close()
            con.close()
            return json.dumps({"status":200, "message":"Vehicle added successfully"})
        except:
            return json.dumps({"status":400, "message":"Error occurred when adding the vehicle to the database"})

    # else, immediate return the error message
    else:
        return json.dumps(con)


def add_truck_by_type(data):
    """
    This function takes in a json containing information about a truck, and inserts the truck into the database.
    This insertion is based on truck type, so only information needed is the vin, registration, fuel_cons, emission
    and trucktype.

    :param data: json, containing the information about the truck, vin, registration, fuel_cons, emission, trucktype
    :return:
    if the insertion was successful, then it returns:
    {"status": 200, "message": "Vehicle added successfully"}

    else:
    if the call was unsuccessful, if error connecting with database, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}

    if error occurred when inserting the vehicle, then a generic error message is returned:
    {"status": 400, "message": "Error occurred when adding the vehicle to the database"}
    """

    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # if connection to database was successful
    if is_connected:
        try:
            # get the data from json
            vin = data["vin"]
            registration = data["rego"]
            fuel_cons = data["fuel_consumption"]
            emission = data["emission"]
            trucktype = data["trucktype"]

            cursor = con.cursor()
            # get the vehicle id for the type of the vehicle that is being inserted
            query = "select veh_id from fitproj.VehicleType where trucktype = %s"
            param = (trucktype, )
            cursor.execute(query, param)
            fetchresults = cursor.fetchall()

            # if fetchresults == [], then the database does not have any record for the this type of truck, so
            # need to create a vehicle/truck type
            if fetchresults == []:
                # query to create the new type
                new_type_query = "insert into fitproj.VehicleType (make, model, yr, fuel_type, fuel_cons, emissions, eng, trucktype) " \
                                 "values(NULL, NULL, NULL, NULL, %s, %s, NULL, %s)"
                param1 = (fuel_cons, emission, trucktype,)
                cursor.execute(new_type_query, param1)
                con.commit()
                cursor.execute(query, param)

                # get the vehicle id for the new type just created
                veh_type_id = cursor.fetchall()[0][0]
            else:
                # else, if the type already exist in the database, just get the vehicle id from result returned
                veh_type_id = fetchresults[0][0]

            # insert vehicle into the vehicle table using registration, vin and vehicle type id
            new_veh_query = "insert into fitproj.Vehicle (registration, vin, veh_type_id) values (%s, %s, %s)"
            param2 = (registration, vin, veh_type_id, )
            cursor.execute(new_veh_query, param2)
            con.commit()
            cursor.close()
            con.close()
            return json.dumps({"status":200, "message":"Vehicle added successfully"})
        except:
            return json.dumps({"status":400, "message":"Error occurred when adding the vehicle to the database"})

    # else, immediate return the error message
    else:
        return json.dumps(con)


def get_trip(data):
    """
    This function takes in a json, which contains two dates, and it will return trips of all vehicles that are between
    the two dates (inclusive)
    :param data: json, {start: start date, end: end date}, date is in the form yyyy-mm-dd
    :return:
    if no error occurred then it returns an array of all the trips:
    {"status": 200,
    "message": [{"trip_id": , "user_id": , "veh_reg": , "start": , "end": , "dist":, "date": , "total_emi": } ...]}

    else:
    if error with database connection, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}
    """
    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # if connection to database was successful
    if is_connected:
        cursor = con.cursor()
        start_d = data["start"]
        end_d = data["end"]
        # select trips that are greater than or equal to the start date and less than or equal to the end date
        query = "select * from fitproj.Trips where date >= %s and date <= %s;"

        param = (start_d, end_d, )

        # execute the query
        cursor.execute(query, param, )
        fetchresults = cursor.fetchall()
        new_results = []

        # the date returned by the trip is a datetime object, need to convert it to string
        for r in fetchresults:
            date = r[6]
            date.strftime('%m/%d/%Y')
            new_results.append((r[0], r[1], r[2], r[3], r[4], r[5], str(date), r[7]))
        colnames = [x[0] for x in cursor.description]   # get the columns names
        cursor.close()
        con.close()
        # call make_json to combine all the data
        return make_json(new_results, colnames, 200)

    # else, immediate return the error message
    else:
        return json.dumps(con)


def login(data):
    """
    This function authenticate user login
    :param data: json, this contains the login_id and password
    :return: json
    if no error occurred, then it returns:
    {"status": 200, "message": the user_id for the user}

    else:
    if error with database connection, then it returns:
    {"status": 500, "message": "Cannot connect to the database"}

    if the login_id or password is incorrect, then it returns:
    {"status": 400, "message": "Incorrect login id or password"}
    """
    # result of connecting to the database
    result = connect_to_db()
    # is_connected is a boolean indicating if the connection was successful
    is_connected = result[0]
    # if the connection was successful, con will be the connection, otherwise, con will be the error message
    # to be sent back to the client
    con = result[1]

    # if the connection to database is successful then execute the following
    if is_connected:
        # get the login_id and password from input json
        login_id = data["login_id"]
        password = data["password"]

        # get cursor and execute query
        cursor = con.cursor()
        query = "select user_id from fitproj.Users where loginID = %s and BINARY password = %s;"
        param = (login_id, password,)
        cursor.execute(query, param)

        # get result
        fetchresults = cursor.fetchall()

        res = {}

        # if none got returned, then something is wrong with the login_id or password, set status and  error message
        if not fetchresults:
            res["status"] = 400
            res["message"] = "Incorrect login id or password"
        # else, the authentication was successful, return the user_id for the user
        else:
            user_id = fetchresults[0][0]
            res["status"] = 200
            res["message"] = user_id
        cursor.close()
        con.close()
        return json.dumps(res)

    # else, immediate return the error message
    else:
        return json.dumps(con)