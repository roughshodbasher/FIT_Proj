import pdfplumber
data = []

name1 = "2020"
name3 = " TopSellers.pdf"
for i in range(9):
    if len(str(i+1)) == 2:
        name2 = str(i+1)
    else:
        name2 = '0'+str(i+1)
    with pdfplumber.open(name1+name2+name3) as pdf:
        page = (pdf.pages[0].extract_text())

    p = page.split('\n')
    print(p)

    flag = False
    for d in p:
        if d == "Rank  Make  Model  CO2 Range (g/km) ":
            flag = True
        else:
            if flag:
                line = d.split(" ")
                while True:
                    try:
                        line.remove("")
                    except ValueError:
                        break
                if d[0] == "20":
                    flag = False
                if line[1:] not in data:
                    data.append(line[1:])
f = open("rawData.txt",'w')
for elem in data:
    f.write("\t".join(elem)+'\n')
f.close()