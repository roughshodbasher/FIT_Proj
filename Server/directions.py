import json
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
    return (t,estimatedEmissions)

def getDirections(data):
    return





if __name__ == "__main__":
    print(getDirectionsDemo())