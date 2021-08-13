# run python idle in vis stud code -> ctrl+shift+p -> python REPL
import mysql.connector
from mysql.connector.errors import DataError
from flask import Flask
from flask.ext.mysqldb import MySQL
import json

'''
Run this after installing mysql in your computer
'''
#using flask.ext
def maintwo():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'com1'
    app.config['MYSQL_PASSWORD'] = 'admin'
    app.config['MYSQL_DB'] = 'fitproj'
    mysql = MySQL(app)

    dbcursor = mysql.connection.cursor()


# using normal means
if __name__ == "__main__":
    databs = mysql.connector.connect(
        host = "localhost",
        user = "com1",
        passwd = "admin",
        # add database = after running CREATE DATABASE in .execute line 22
        database= "fitproj"
    )

    # cursor
    dbcursor = databs.cursor()

    # dbcursor.execute("CREATE DATABASE databaseone")
    #                    command         db name

    '''
    initializing table
    dbcursor.execute(" CREATE TABLE Vehicle (veh_id int PRIMARY KEY AUTO_INCREMENT, 
                    make VARCHAR(20), 
                    model VARCHAR(20),
                    yr int, 
                    registration VARCHAR(7),
                    vin VARCHAR(17),
                    fuel_type ENUM ("DIESEL", "PETROL", "ELECTRIC"),
                    fuel_cons int,
                    emissions int,
                    eng VARCHAR(10)
                        )" 
                    )
    '''

    '''
    # #try 
    # dbcursor.execute("DESCRIBE Vehicle")
    # #printing output
    # for c in dbcursor:
    #     print(c)
    '''

    # trial inserting
    #type1
    # dbcursor.execute("INSERT INTO Vehicle (make, model, yr, registration, vin, fuel_type, fuel_cons, emissions, eng) VALUES ('Lambo', 'Huracan', 2020, 'ABC123', '', 'PETROL', 1,1, 'v12')")
    # databs.commit()

    # #type2 safer
    # dbcursor.execute("INSERT INTO Vehicle (make, model, registration, vin, fuel_type, fuel_cons, emissions, eng) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s), ('Lambo', 'Huracan', 2020, 'ABC123', '', 'PETROL', 1,1, 'v12')")
    # databs.commit()



def query_to_db():
    dbcursor.execute("SELECT * FROM Vehicle")
    fetchresults = dbcursor.fetchall()

    colnames=[x[0] for x in dbcursor.description]

    to_return = []

    for results in fetchresults:
        to_return.append(dict(zip(colnames, results)))

    print(to_return[0])

    return json.dumps(to_return)



def new_vehicle(make, model, yr, regis, vin, fltype, flcons, emi, eng):
    dbcursor.execute("INSERT INTO Vehicle (make, model, registration, vin, fuel_type, fuel_cons, emissions, eng) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) , (make, model, yr, regis, vin, fltype, flcons, emi, eng)")

