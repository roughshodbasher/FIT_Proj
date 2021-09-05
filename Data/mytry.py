import csv

def trashPrint (nList):
    for row in nList:
        for item in row:
            print (item, end=" ")
        print("")

data = []
myfile = open("Data/rawData.txt", "r")
for row in myfile:
    data.append(row.strip().split())
myfile.close()
# trashPrint(data)
#print(data)

data3 = []
for row in data:
    if (row[2] == "4x4"):
        data3.append(row[0:2] + row[3:6])
    else:
        data3.append(row)

data2 = []
for row in data3 :
    data2.append(row[0:2] + [2020]+ [int(row[2]) + int(row[4]) * 0.75] )


with open("data.csv", 'w') as f:
    writer = csv.writer(f)
    header = ["Make", "Model", "Year", "Emission (CO2 g/km)"]
    writer.writerow(header)
    writer.writerows(data2)


