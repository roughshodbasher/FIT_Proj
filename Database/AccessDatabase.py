import mysql.connector


def connect_to_db():
    cnx = mysql.connector.connect(user=, password=,
                                  host=,
                                  database=)
    return cnx


def get_vehicle_info(rego):
    con = connect_to_db()
    cursor = con.cursor()
    # query: select from db, information about the vehicle
    query = "select * from fit_db.Vehicle where rego = %s"

    param = (rego, )
    cursor.execute(query, param)
    info = {}
    cols = cursor.description
    items = cursor.fetchall()[0]
    for i in range(len(cols)):
        col_name = cols[i][0]
        info[col_name] = items[i]

    cursor.close()
    con.close()
    return info


def get_trip_by_rego():
    con = connect_to_db()
    # execute query and process data here

    con.close()


def get_emission():
    pass


def add_trip(trip):
    pass




