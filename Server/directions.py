import json
import urllib.request
import math
import numpy as np
import timeit
# import numpy.linalg as np.linalg
"""
API Documentation
https://developers.google.com/maps/documentation/directions/get-directions
"""
class Path:
    def __init__(self,polyline='',tolerance=10):
        self.polyline = polyline
        self.coordBoxes = []
        self.tolerance = tolerance*0.000009009
        coords = self.polylineToLinearCoords(self.polyline)
        print(coords)
        for i in range(len(coords)-1):
            self.coordBoxes.append(self.CoordBox(coords[i],coords[i+1],self.tolerance))

    def onRoute(self,pos):
        for box in self.coordBoxes:
            if box.inBox(pos):
                return True
        return False

    def polylineToLinearCoords(self,polys):
        coords = []
        for poly in polys:
            coords.append(decodePolyline(poly))
        flatCoords = []
        for subcord in coords:
            for c in subcord:
                if not (c in flatCoords):
                    flatCoords.append(c)
        return flatCoords

    def decodePolyline(self,poly='', precision=5):
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
        def __init__(self,pos1,pos2,tolerance):
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
            self.minY -= tolerance
            self.minX -= tolerance
            self.maxY += tolerance
            self.maxX += tolerance
        def inBox(self,pos,primitave=True):
            if self.minX < pos[0] and self.minY < pos[1] and self.maxX > pos[0] and self.maxY > pos[1]:
                if primitave:
                    return True
            return False

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




if __name__ == "__main__":
    """test data"""
    onRouteLoc1 = [33.8161014800008, -117.9225146125875]
    onRouteLoc2 = [33.82157343203593, -117.92277292780344]
    offRouteLoc = [33.8353080852262, -117.92214664830355]
    0.000009009

    testRoute = [[33.8161014800008, -117.9225146125875], [33.82157343203593, -117.92277292780344], [33.8353080852262, -117.92214664830355],[33.8821008,-118.0249616]]
    """ end test data"""
    (t, routeRaw, polyLine, estimatedEmissions) = getDirectionsDemo()

    r = Path(polyLine)
    for i in range(1000):
        for p in testRoute:
            r.onRoute(p)
