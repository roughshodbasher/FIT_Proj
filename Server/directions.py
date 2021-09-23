import json
import urllib.request
import math
import numpy as np
import timeit
import minPath


meters_to_coord = 0.000009009

# import numpy.linalg as np.linalg
"""
API Documentation
https://developers.google.com/maps/documentation/directions/get-directions
"""
class Path:
    '''
    The path class generates the path taken by the user based on the polyline retrived from the Google Maps API
    The path is split up to only contain straight paths, a box is created around these subpaths using the CoordBox subclass
    The sub-class CoordBox is used to test whether a set point is on route
        Coordbox is a basic box around each subpath along the route, extended by the tolerance
        i.e the minpoint will be offset by 5 meters (tolerance = 10 / 2)
        to test if on route, coordbox checks if within the box it generates
            if within the box, uses euclids alg to find distance between line generated by route points and users position
                not just using euclids alg as it doesnt seem to care if the line isnt infinite and will say a point is < 1m away even if its 100km away
            if euclids says w/in distance, return True else returns False

    '''
    def __init__(self,polyline=[''],tolerance=10):
        '''
        Path Class, used to determine whether the user is on the route or not
        :param polyline: array containing googlemaps API polyline of the route
        :param tolerance: how far we are allowing the user to go off route before telling them
        '''
        # storing the polyline incase needed later (may remove)
        self.polyline = polyline

        # converting tolerance to coordinate distance (lat/long) from meters

        self.tolerance = tolerance * 0.000009009
        # coordBoxes contains all the coordBox objects
        self.coordBoxes = []
        #converting polyline into lat/long coordinates
        self.coords = self.polylineToLinearCoords(self.polyline)
        #creating the coordBoxes
        for i in range(len(self.coords)-1):
            self.coordBoxes.append(self.CoordBox(self.coords[i],self.coords[i+1],self.tolerance))

    def saveCords(self):
        f = open("Route Test 2.csv","w")
        for elem in self.coords:
            f.write(str(elem[0])+","+str(elem[1])+'\n')
        f.close()

    def onRoute(self,pos):
        '''
        onRoute will determine whether the user is still following their given route
        :param pos: users location
        :return: Boolean
        '''
        # primitave check, iterating through each coordBox, and checking if the user is in the box
        #   -Change to lib(?) for faster lookup
        for box in self.coordBoxes:
            if box.inBox(pos):
                return True
        return False

    def polylineToLinearCoords(self,polys):
        '''
        polylineToLinearCoords converts array of polylines into single array containing lat/long coordinates of route
        :param polys: array containing googlemaps API polyline of the route
        :return: array containing lat/long coordinates of each minor point of the route
        '''
        coords = []
        #decoding poly lines into coordinates
        for poly in polys:
            coords.append(self.decodePolyline(poly))
        #flattening coordinates into a single array
        flatCoords = []
        for subcord in coords:
            for c in subcord:
                if not (c in flatCoords):
                    flatCoords.append(c)
        return flatCoords

    def decodePolyline(self,poly='', precision=5):
        """
        Function is taken from https://github.com/mapbox/polyline/blob/master/src/polyline.js and Ive translated it to python
        I dont understand what its doing but it is working, and tested by plotting the points it returns giving the exact same route
        """
        index = 0
        lat = 0
        lng = 0
        coordinates = []
        shift = 0
        result = 0
        byte = None
        latitude_change = None
        longitude_change = None
        factor = math.pow(10, precision)

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

            coordinates.append([lat / factor, lng / factor])

        return coordinates


    class CoordBox:
        '''
        Coordbox is just a box spanning 2 points extended by the input tolerance
        Used to check whether a position is on route, and storing as a class is considerably faster than calculating it each time
        '''
        def __init__(self,pos1,pos2,tolerance):
            #creating the box,
            # "bottom left" of the box = [minX,minY]
            # "top right" of the box = [maxX,maxY]
            # tolerance is added/subtracted to allow being slightly off route
            if pos1[0] < pos2[0]:
                self.maxX = pos2[0]
                self.minX = pos1[0]
            else:
                self.minX = pos2[0]
                self.maxX = pos1[0]
            if pos1[1] < pos2[1]:
                self.maxY = pos2[1]
                self.minY = pos1[1]
            else:
                self.minY = pos2[1]
                self.maxY = pos1[1]
            self.minY -= tolerance/2
            self.minX -= tolerance/2
            self.maxY += tolerance/2
            self.maxX += tolerance/2
            #storing exact points and tolerance for euclids alg used in inBox
            self.p1 = np.array(pos1)
            self.p2 = np.array(pos2)
            self.tolerance = tolerance

        def inBox(self,pos):
            """
            inBox will determine whether the users position is within tolerance of the route
                by default it will check if the user is within 10m of the road
            :param pos: users lat long coordinates
            :return:
            """
            # if within the box
            if self.minX < pos[0] and self.minY < pos[1] and self.maxX > pos[0] and self.maxY > pos[1]:
                # Euclids algorithm
                # checking if within tolerance range
                #  not just using euclids alg as it doesnt seem to care if the line isnt infinite and will say a point is < 1m away even if its 100km away
                if np.cross(self.p2 - self.p1, pos - self.p1) / np.linalg.norm(self.p2 - self.p1) <= self.tolerance:
                    return True
            return False

class Travelling:
    def __init__(self,data=json.dumps({"start":"lat\/lng: (-37.810108,144.9582684)","destinations":"[lat\/lng: (-37.8174907,144.9545615), lat\/lng: (-37.9069897,145.1560372)]","vehicle":"ABC123"}),debug=False):
        data = json.loads(data)

        #cleaning the input data from mobile application
        data["start"] = data["start"][data["start"].find("(") + 1:data["start"].find(")")]
        data["start"] = data["start"].split(",")
        data["start"][0] = float(data["start"][0])
        data["start"][1] = float(data["start"][1])

        data["destinations"] = data["destinations"].split("lat\/lng")
        del data["destinations"][0]
        for i in range(len(data["destinations"])):
            data["destinations"][i] = data["destinations"][i][
                                      data["destinations"][i].find("(") + 1:data["destinations"][i].find(")")]
            data["destinations"][i] = data["destinations"][i].split(",")
            data["destinations"][i][0] = float(data["destinations"][i][0])
            data["destinations"][i][1] = float(data["destinations"][i][1])

        self.tolerance = 10
        self.data = data
        self.destinations = data["destinations"][:]
        self.visited = [data["start"]]

        print(data)

        if len(self.data["destinations"]) == 1:
            self.single = True
            if not debug:
                (self.apiData, self.polyLine, self.estimatedDistance, keyCheck) = getDirectionsSingle(data)
            else:
                (self.apiData, self.polyLine, self.estimatedDistance, keyCheck) = getDirectionsSingleDemo()
        else:
            self.single = False
            (self.apiData, self.polyLine, self.estimatedDistance, keyCheck) = getDirectionsMultiple(data)
        if keyCheck:
            self.path = Path(self.polyLine)
        else:
            raise KeyError

    def onRoute(self,point):
        self.visited.append(point)
        if not self.single:
          self.removeVisited(point)
        if  self.path.onRoute(point):
            return True
        else:
            if self.single:
                self.path = getDirectionsSingle(point,self.destinations)
            else:
                #optimize
                self.path = getDirectionsMultiple(point,self.destinations)
            return False

    def removeVisited(self,point):
        i = 0
        while i < len(self.destinations):
            if np.linalg.norm(np.array(point),np.array(self.destinations[i])) < self.tolerance/meters_to_coord:
                del self.destinations[i]
            else:
                i += 1
        return True

    def atEnd(self,point):
        if np.linalg.norm(np.array(point), np.array(self.destinations[-1])) < self.tolerance / meters_to_coord:
            return True
        return False

    def calcEmissions(self):
        # use lin alg to cal distances mult by car emissions
        return
def getDirectionsSingleDemo():
    """startLocation = "Disneyland"
    endLoaction = "Universal Studios Hollywood"
    """

    f = open("routeTest.json")
    t = json.load(f)
    estimatedDistance = t['routes'][0]['legs'][0]['distance']['value']/1000
    # estimated emissions: g/CO2 * CO2 = g
    estimatedEmissions = emissions*estimatedDistance
    polyLine = []
    for d in t['routes'][0]['legs'][0]['steps']:
        polyLine.append(d['polyline']['points'])

    return (t,polyLine,estimatedDistance)

def getDirectionsSingle(start = [0,0], destinations = {0:[0,0]},debug=False):
    # pull info out of data request
    start = str(start["start"][0])+','+str(start["start"][1])
    end = str(destinations["destinations"][0][0])+','+str(destinations["destinations"][0][1])
    key = ""
    if not key:
        try:
            f = open("key.api")
            for line in f:
                key = line.rstrip()
        except:
            key = ""
            return ("No API key",None,None,False)
    try:
        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+start+"&destination="+end+"&key="+key) as url:
            url_data = json.loads(url.read().decode())
    except:
        return ("Incorrect API key", None, None, False)

    if debug:
        print(url_data)
    t = url_data
    estimatedDistance = t['routes'][0]['legs'][0]['distance']['value'] / 1000
    polyLine = []
    for d in t['routes'][0]['legs'][0]['steps']:
        polyLine.append(d['polyline']['points'])

    return (t, polyLine, estimatedDistance, True)

def getDirectionsMultiple(data,debug=False):
    start = data["start"]
    destinations = data["destinations"]
    key = ""
    if not key:
        try:
            f = open("key.api")
            for line in f:
                key = line.rstrip()
        except:
            key = ""
            return ("No API key", None, None, False)

    # need to call the api n times (n is the number of locations)
    # d = json.loads(data)
    # print(d["destinations"])
    print(destinations)
    destinations = [start] + destinations
    for i, coord in enumerate(destinations):
        destinations[i][0] = str(destinations[i][0])
        destinations[i][1] = str(destinations[i][1])
    arr = []
    for elem in destinations:
        arr.append(",".join(elem))
    destinationString = "|".join(arr)
    distanceMatrix = []
    # print(d["destinations"])
    if not debug:
        for elem in destinations:
            # print("???")
            try:
                with urllib.request.urlopen(
                        "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + ",".join(
                                elem) + "&destinations=" + destinationString + "&key=" + key) as url:
                    url_data = json.loads(url.read().decode())
                    temp = []
                    for elem in url_data["rows"][0]["elements"]:
                        temp.append(elem["distance"]["value"])
                    distanceMatrix.append(temp)
            except:
                return ("Incorrect API key", None, None, False)
    order = minPath.main(distanceMatrix)
    order.append(0)
    locationOrder = []
    for elem in order:
        locationOrder.append(destinations[elem])
    startLocation = ",".join(locationOrder.pop(0))
    toString = []
    for elem in locationOrder:
        toString.append(",".join(elem))
    destinations = "|".join(toString)
    m = "https://maps.googleapis.com/maps/api/directions/json?origin=" + startLocation + "&destination=" + startLocation + "&waypoints=" + destinations + "&key=" + key
    print(m)
    if not debug:
        try:
            with urllib.request.urlopen(m) as url:
                t = json.loads(url.read().decode())
        except:
            return ("Incorrect API key", None, None, False)
    else:
        f = open("routeMulti.json")
        t = json.load(f)
    estimatedDistance = t['routes'][0]['legs'][0]['distance']['value'] / 1000
    polyLine = []
    for d in t['routes'][0]['legs'][0]['steps']:
        polyLine.append(d['polyline']['points'])
    return (t, [t["routes"][0]["overview_polyline"]["points"]], estimatedDistance, True)

def getDirectionsMultipleDemo(data=json.dumps({"start" : [0,0], "destinations" : {0 : [0,0]}}),debug=False):
    key = None
    if not key:
        try:
            f = open("key.api")
            for line in f:
                key = line.rstrip()
        except:
            key = ""
            return ("No API key", None, None, False)
    # need to call the api n times (n is the number of locations)
    d = json.loads(data)
    # print(d["destinations"])
    d["destinations"] = [d["start"]] + d["destinations"]
    for i,coord in enumerate(d["destinations"]):
        d["destinations"][i][0] = str(d["destinations"][i][0])
        d["destinations"][i][1] = str(d["destinations"][i][1])
    arr = []
    for elem in d["destinations"]:
        arr.append(",".join(elem))
    destinationString = "|".join(arr)
    distanceMatrix = []
    print(d["destinations"])
    if not debug:
        for elem in d["destinations"]:
            print("???")
            try:
                with urllib.request.urlopen("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + ",".join(elem) + "&destinations=" + destinationString + "&key=" + key) as url:
                    url_data = json.loads(url.read().decode())
                    temp = []
                    for elem in url_data["rows"][0]["elements"]:
                        temp.append(elem["distance"]["value"])
                    distanceMatrix.append(temp)
            except:
                return ("Incorrect API key", None, None, False)
    else:
        distanceMatrix = [[0, 2086, 3242, 3331, 9165, 24737, 25172, 19199],
        [1156, 0, 1156, 3611, 10440, 26012, 26448, 10719],
        [2312, 1156, 0, 2884, 8937, 24509, 24944, 9563],
        [5400, 4244, 3518, 0, 5890, 22734, 23169, 11802],
        [10778, 10212, 8795, 6327, 0, 18795, 19344, 13223],
        [30372, 29806, 28389, 25921, 23532, 0, 18879, 33823],
        [17645, 16489, 15333, 27188, 24790, 20628, 0, 14944],
        [13536, 10572, 9416, 23135, 13391, 30161, 15128, 0],    ]
    order = minPath.main(distanceMatrix)
    order.append(0)
    print(order)
    locationOrder = []
    for elem in order:
        locationOrder.append(d["destinations"][elem])
    startLocation = ",".join(locationOrder.pop(0))
    toString = []
    for elem in locationOrder:
        toString.append(",".join(elem))
    destinations = "|".join(toString)
    print(destinations)
    m = "https://maps.googleapis.com/maps/api/directions/json?origin=" + startLocation + "&destination=" + startLocation +"&waypoints="+destinations+ "&key=" + key
    print(m)
    if not debug:
        try:
            with urllib.request.urlopen(m) as url:
                t = json.loads(url.read().decode())
        except:
            return ("Incorrect API key", None, None, False)
    else:
        f = open("routeMulti.json")
        t = json.load(f)
    estimatedDistance = t['routes'][0]['legs'][0]['distance']['value'] / 1000
    polyLine = []
    for d in t['routes'][0]['legs'][0]['steps']:
        polyLine.append(d['polyline']['points'])
    print(polyLine)
    print(t["routes"][0]["overview_polyline"]["points"])
    return (t, [t["routes"][0]["overview_polyline"]["points"]], estimatedDistance, True)




if __name__ == "__main__":
    """test data"""
    onRouteLoc1 = [33.8161014800008, -117.9225146125875]
    onRouteLoc2 = [33.82157343203593, -117.92277292780344]
    offRouteLoc = [33.8353080852262, -117.92214664830355]


    '''test car information
        vehicle =  ("Toyota, Yarris, 2013")
    '''
    emissions = 165  # Co2 g/km

    testRoute = [[33.8161014800008, -117.9225146125875], [33.82157343203593, -117.92277292780344], [33.8353080852262, -117.92214664830355],[33.8821008,-118.0249616],[33.8155166,-117.9238358],[33.8215783,-117.9226437]]
    """ end test data"""
    # (t, polyLine, estimatedDistance, keyCheck) = getDirectionsSingleDemo(debug=True)
    # startLocation = [33.81489414711607, -117.92336969628036]
    # destinations = [[33.81052620294962, -117.9312339328883],[33.81056566718572, -117.94374315691087],[33.83251967706872, -117.94375113424839],[33.864090283604945, -117.96752883738218],[33.963051852302605, -118.08490947387466],[33.83248413374035, -118.0850334763591],[33.773112801081425, -118.00051913281155]]
    # multiData = json.dumps({"start" : startLocation, "destinations" : destinations})
    # (t, polyLine, estimatedDistance, keyCheck) = getDirectionsMultiple(startLocation,destinations,debug=False)
    #
    # # startLocation = [33.81489414711607, -117.92336969628036]
    # # destinations = [[33.81052620294962, -117.9312339328883]]
    # # singleData = json.dumps({"start": startLocation, "destinations": destinations})
    # # (t, polyLine, estimatedDistance, keyCheck) = getDirectionsSingle(startLocation,destinations, debug=False)
    # if not polyLine:
    #     print(t)
    # else:
    #     print(t)
    #     r = Path(polyLine)
    #     r.saveCords()
    test = Travelling()
    print(test.polyLine)
