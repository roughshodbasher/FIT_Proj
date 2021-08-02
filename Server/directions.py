import json
import urllib.request
import math
import numpy as np
# import numpy.linalg as np.linalg
"""
API Documentation
https://developers.google.com/maps/documentation/directions/get-directions
"""

def getDirectionsDemo():
    """startLocation = "Disneyland"
    endLoaction = "Universal Studios Hollywood"
    vehicle =  ("Toyota, Yarris, 2013")"""
    emissions = 165 #Co2 g/km
    f = open("routeTest.json")
    t = json.load(f)
    estimatedDistance = t['routes'][0]['legs'][0]['distance']['value']/1000

    # estimated emissions: g/CO2 * CO2 = g
    estimatedEmissions = emissions*estimatedDistance




    routeRaw = []
    polyLine = []
    for d in t['routes'][0]['legs'][0]['steps']:
        routeRaw.append((d['start_location']['lat'],d['start_location']['lng']))
        polyLine.append(d['polyline']['points'])

    routeRaw.append((t['routes'][0]['legs'][0]['steps'][-1]['end_location']['lat'],t['routes'][0]['legs'][0]['steps'][-1]['end_location']['lng']))
    return (t,routeRaw,polyLine,estimatedEmissions)


def getDirections(data):
    # pull info out of data request
    start = "-37.7953066353135,145.0323949434231"
    end = "-37.78408613899136,145.06219662680624"
    key = "key"
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+start+"&destination="+end+"&key="+key) as url:
        url_data = json.loads(url.read().decode())
    print(url_data)

def polylineToLinearCoords(polys):
    coords = []
    for poly in polys:
        coords.append(decodePolyline(poly))
    # for c in coords:
    #     for d in c:
    #         print(str(d[0])+'\t'+str(d[1]))
    return coords


def decodePolyline(poly='',precision=5):
    # code adapted from https://github.com/mapbox/polyline/blob/master/src/polyline.js
    index = 0
    lat = 0
    lng = 0
    coordinates = []
    shift = 0
    result = 0
    byte = None
    latitude_change = None
    longitude_change = None
    factor = math.pow(10,precision)


    while index < len(poly):
        byte = 0
        shift = 0
        result = 0
        firstLoop = True
        while byte >= 0x20 or firstLoop:
            firstLoop = False
            byte = ord(poly[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5

        if (result & 1):
            latitude_change = ~(result >> 1)
        else:
            latitude_change = (result >> 1)

        shift = 0
        result = 0

        firstLoop = True
        while firstLoop or byte >= 0x20:
            firstLoop = False
            byte = ord(poly[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5

        if (result & 1):
            longitude_change = ~(result >> 1)
        else:
            longitude_change = (result >> 1)

        lat += latitude_change
        lng += longitude_change

        coordinates.append([lat/factor,lng/factor])

    return coordinates

def deltaCoord(coords):
    zero = coords[0]
    relativeCoords = []
    for c in coords:
        # print(c,zero)
        relativeCoords.append([zero[0]-c[0],zero[1]-c[1]])
    return relativeCoords

def relVector(origin,v2):
    return [v2[0]-origin[0],v2[1]-origin[1]]

def vectorDist(pos,point1,point2,tolerance=0):
    C = np.array([0,0])
    B = np.array(point2) - np.array(point1)
    A = np.array(pos) - np.array(point1)
    if np.linalg.norm(B) <= tolerance:
        return np.inf
    print(np.dot(B, A),(np.linalg.norm(B) * np.linalg.norm(A)))
    print(abs(math.acos(np.dot(B, A) / (np.linalg.norm(B) * np.linalg.norm(A)))))
    if abs(math.acos(np.dot(B,A)/(np.linalg.norm(B)*np.linalg.norm(A)))) < math.pi/180*5:
        return np.inf
    print(A,B,C)
    print(str(pos[0])+'\t'+str(pos[1])+'\n'+str(point1[0])+'\t'+str(point1[1])+'\n'+str(point2[0])+'\t'+str(point2[1]))
    print(pos,',',point1,',',point2)
    print()
    #below is the 'proper' way to calculate the distance, but it isnt working
    p3 = np.array(pos)
    p1 = np.array(point1)
    p2 = np.array(point2)
    return abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1))

def onRoute(coords,pos,tolerance=10):
    #converting tolerance into lat long format
    # https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm
    # 0.00001 = 1.11 m -> 0.000009009 = 1m
    tolerance *= 0.000009009

    # checking distance between nodes
    for i,coord in enumerate(coords):
        if math.sqrt((coord[0]-pos[0])**2+(coord[1]-pos[1])**2) <= tolerance:
            return True
    for i in range(len(coords)-1):
        #creating a box around each stage of the route
        if coords[i][0] < coords[i+1][0]:
            minX = coords[i][0] - tolerance
            maxX = coords[i + 1][0] + tolerance
        else:
            minX = coords[i + 1][0] - tolerance
            maxX = coords[i][0] + tolerance
        if coords[i][1] < coords[i+1][1]:
            minY = coords[i][1] - tolerance
            maxY = coords[i + 1][1] + tolerance
        else:
            minY = coords[i + 1][1] - tolerance
            maxY = coords[i][1] + tolerance

        if minX < pos[0] and minY < pos[1] and maxX > pos[0] and maxY > pos[1]:
            #not perfect but functional
            return True
    return False


if __name__ == "__main__":
    """test data"""
    onRouteLoc1 = [33.8161014800008, -117.9225146125875]
    onRouteLoc2 = [33.82157343203593, -117.92277292780344]
    offRouteLoc = [33.8353080852262, -117.92214664830355]
    0.000009009


    """ end test data"""
    d = getDirectionsDemo()
    coords = polylineToLinearCoords(d[2])
    flatCoords = []
    for arr in coords:
        for c in arr:
            flag = True
            for elem in flatCoords:
                flag2 = True
                for i in range(len(c)):
                    if c[i] != elem[i]:
                        flag2 = False
                        break
                if flag2:
                    flag = False
                    break
            if flag:
                flatCoords.append(c)

    outPos = [33.8309851,-117.9298142]
    print(onRoute(flatCoords,onRouteLoc1))
    print(onRoute(flatCoords,onRouteLoc2))
    print(onRoute(flatCoords,offRouteLoc))
    print(onRoute(flatCoords,[33.8821008,-118.0249616]))
    print(onRoute(flatCoords,[33.8309851,-117.9298142]))
    print(onRoute(flatCoords,[33.8417245,-117.9522119]))
    # print(vectorDist([33.8309851,-117.9298142] , [33.81837, -117.92214] , [33.81838, -117.92214])/ 0.000009009)
