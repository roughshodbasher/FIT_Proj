import json

json.dumps([])


database = {}
database["Stuff"] = "dunno what to put here, update later"

request = {}
request["type"] = 1
request["name"] = "Database"
request["data"] = database

d = json.dumps(request)
f = open("databaseInput.json","w")
f.write(d)
f.close()
