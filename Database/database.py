# run python idle in vis stud code -> ctrl+shift+p -> python REPL
import mysql.connector
from mysql.connector.errors import DataError

'''
Run this after installing mysql in your computer
'''



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

dbcursor.execute("SELECT * FROM Vehicle")

for x in dbcursor:
    print(x)