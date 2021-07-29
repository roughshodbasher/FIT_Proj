import json
import urllib.request
import math
import numpy as np
from numpy.linalg import norm as npNorm
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

def polylineToLinearCoods(polys,start=[-37.914580917633366, 145.1349687098531]):
    coords = []
    for poly in polys:
        coords.append(decodePolyline(poly))

    relCoords = []
    origin = None
    for c in coords:
        relCoords.append(deltaCoord(c,origin))
        origin = relCoords[-1][-1]
    flatCoords = []
    for co in relCoords:
        for c in co:
            if not (c in flatCoords):
                flatCoords.append([c[0]+start[0],c[1]+start[1]])
    return flatCoords


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

def deltaCoord(coords,zero=None):
    if not zero:
        zero = coords[0]
    relativeCoords = []
    for c in coords:
        # print(c,zero)
        relativeCoords.append([zero[0]-c[0],zero[1]-c[1]])
    return relativeCoords

def relVector(origin,v2):
    return [v2[0]-origin[0],v2[1]-origin[1]]

def vectorDist(pos,point1,point2):
    p3 = np.array(pos)
    p1 = np.array(point1)
    p2 = np.array(point2)
    return abs(npNorm(np.cross(p2-p1, p1-p3))/npNorm(p2-p1))

def onRoute(coords,pos,tolerance=10):
    #converting tolerance into lat long format
    # https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm
    # 0.00001 = 1.11 m -> 0.000009009 = 1m
    tolerance *= 0.000009009

    # checking distance between nodes
    for i,coord in enumerate(coords):
        if math.sqrt((coord[0]-pos[0])**2+(coord[1]-pos[1])**2) <= tolerance:
            print("here")
            return True
        print(math.sqrt((coord[0]-pos[0])**2+(coord[1]-pos[1])**2)/tolerance)
    for i in range(len(coords)-1):
        #calculating distance between location and the line of each leg
        if vectorDist(pos,coords[i],coords[i+1]) <= tolerance:
            print(vectorDist(pos,coords[i],coords[i+1]),tolerance)
            return True
    return False


if __name__ == "__main__":
    """test data"""
    onRouteLoc1 = [33.8161014800008, -117.9225146125875]
    onRouteLoc2 = [33.815593242933474, -117.92358940803874]
    offRouteLoc = [33.81809687566821, -117.91943153015087]



    """ end test data"""
    d = getDirectionsDemo()
    #
    # NEED TO FIX REL COORDINATES
    #
    coords = polylineToLinearCoods(d[2],d[1][0])
    print(d[1][0])
    # print(onRoute(coords,onRouteLoc1))
    print(onRoute(coords,onRouteLoc2))
    # print(onRoute(coords,offRouteLoc))
    #print(vectorDist([5,1],[0,1]))