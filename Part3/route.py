#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Pete Fyffe (pfyffe)
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#
# ACKNOWLEDGEMENTS
# 1. __str__ method for Edge class completely copied from https://stackoverflow.com/a/33800620/16519580 user falsetru
# 2. distance_to_goal method is completely copied from https://www.geeksforgeeks.org/program-distance-two-points-earth/
#   with very slight refactoring. The Haversine library would have worked also.
# 3. The idea to use a "parentMap" to record a DFS traversal comes from 
#   https://stackoverflow.com/a/12864196/16519580 user amit.
#   Every line where their code was used is marked with a "see source #3".


# !/usr/bin/env python3
import sys
from math import radians, cos, sin, asin, sqrt, tanh
from queue import PriorityQueue

DANGER_SPEED_LIMIT = 50

class Edge:
    def __init__(self, dst, length, speedLimit, highway):
        self.dst = dst
        self.length = length
        self.speedLimit = speedLimit
        self.highway = highway

    #string method completely copied from https://stackoverflow.com/a/33800620/16519580 user falsetru
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    #end of code from falsetru
    
    #If two edges in the priority queue have equal priority, this compares them
    def __lt__(self, other):
        return self.length < other.length;

class LatLng:
    def __init__(self, lat, lng):
        self.lat = lat #latitude
        self.lng = lng #longitude
        
    def __str__(self):
        return '(%s, %s)' % (self.lat, self.lng)




def read_file(filename):
    with open(filename, "r") as f:
        return [line for line in f.read().split("\n")]


def assemble_graph():
    """
    Creates an adjacency list-style graph from a file where every key is a city or road name
    and every value is a list of Edge objects representing immediate neighbors.
    """
    fileContents = read_file("road-segments.txt")
    graph = {}
    for line in fileContents:
        pieces = line.split(" ")
        if (len(pieces) >= 5):
            city1 = pieces[0]
            city2 = pieces[1]
            length = float(pieces[2])
            speedLimit = float(pieces[3])
            highway = pieces[4]

            forwardEdge = Edge(city2, length, speedLimit, highway)
            backwardEdge = Edge(city1, length, speedLimit, highway)

            #Add the city1 to the city2's list of neighbors
            neighbors = []
            if city1 in graph:
                neighbors = graph[city1]
            else:
                graph[city1] = neighbors
            neighbors.append(forwardEdge)

            neighbors = []
            if city2 in graph:
                neighbors = graph[city2]
            else:
                graph[city2] = neighbors
            neighbors.append(backwardEdge)
    return graph


def locations_dictionary():
    """
    Reads a file and returns a dictionary where every key is a city name
    and every value is a LatLng object representing its location. 
    """
    fileContents = read_file("city-gps.txt")
    locations = {}
    for line in fileContents:
        pieces = line.split(" ")
        if (len(pieces) >= 3):
            cityName = pieces[0]
            lat = float(pieces[1])
            lng = float(pieces[2])

            loc = LatLng(lat, lng)
            locations[cityName] = loc

    return locations


def distance_to_goal(start, end):
    """
    Computes the distance between two points on earth using the Haversine Formula.
    This method was completely copied from https://www.geeksforgeeks.org/program-distance-two-points-earth/
    with very slight refactoring.
    """
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(start.lng)
    lon2 = radians(end.lng)
    lat1 = radians(start.lat)
    lat2 = radians(end.lat)
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in miles
    r = 3956
    # calculate the result
    return c * r
#end code from GeeksForGeeks



def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    if start == end:
        return {"total-segments" : 0, 
            "total-miles" : 0, 
            "total-hours" : 0, 
            "total-delivery-hours" : 0, 
            "route-taken" : []}

    #Load entire dataset
    graph = assemble_graph()
    locations = locations_dictionary()

    fringe = PriorityQueue()
    startEdge = Edge(start, 0, 0, None)
    fringe.put((0, startEdge))
    visited = []
    
    parentMap = dict()

    while fringe:
        (currPriority, currMove) = fringe.get()
        currCityName = currMove.dst
        if currCityName not in visited:
            visited.append(currCityName)
            for move in graph[currCityName]:
                #Record this tile as the predecessor of each next move
                if not parentMap.get(move):
                    parentMap[move] = currMove #put (key=child node, value=parent node), see source #3

                #If city is the goal
                if move.dst == end:
                    return readRoute(parentMap, startEdge, move)
                #If city is not visited yet
                elif move.dst not in visited:
                    #If the location does not have a lat/lng value, assume its dist. to the goal is 0
                    estimatedDistance = 0 
                    if move.dst in locations and end in locations: 
                        estimatedDistance = distance_to_goal(locations[move.dst], locations[end])
                        
                    nextCost = 0
                    if cost == "segments":
                        nextCost = 1 + currPriority #add number of roads/cities already visited
                    elif cost == "distance":
                        nextCost = move.length + currPriority #add length of road plus distance already traveled
                    elif cost == "time":
                        nextCost = (move.length / move.speedLimit) + currPriority #add time to travel new road plus time already spent travelling here
                    elif cost == "delivery":
                        #If there's a chance for a box to fall out,
                        #add the time taken to get to the road to
                        #the time to travel to and along the road 2 times (to account for the breakage) multiplied by a probability
                        if move.speedLimit >= DANGER_SPEED_LIMIT:
                            travelTime = move.length / move.speedLimit
                            nextCost = travelTime + tanh(move.length / 1000) * 2 * (travelTime + currPriority)
                    else:
                        raise ValueError("Invalid argument for 'cost' in get_route(...)")

                    priority = nextCost + estimatedDistance #cost plus heuristic
                    fringe.put((priority, move))
    return {}



def readRoute(parentMap, startKey, endKey):
    """
    Given a parentMap where every key is a city/road and its value is the previous road/city
    used to get there, returns the dictionary of output needed for get_route(...).
    startKey is the original Edge.
    endKey is the destination Edge.
    """
    #Order the edges used from start to end in a temporary list called routeTakenEdges
    curr = endKey
    routeTakenEdges = []
    while (curr != startKey):
        routeTakenEdges.append(curr)
        #Keep stepping backward from the end
        curr = parentMap[curr] #see source #3

    routeTaken = []
    totalMiles = 0
    totalHours = 0
    totalDeliveryHours = 0
    for i in range(0, len(routeTakenEdges)):
        edge = routeTakenEdges.pop()
        routeTaken.append((edge.dst, str(edge.highway)+" for "+str(edge.length)+" miles"))
        totalMiles += edge.length
        travelTime = edge.length / edge.speedLimit
        totalHours += travelTime
        if edge.speedLimit >= DANGER_SPEED_LIMIT:
            totalDeliveryHours += travelTime + tanh(edge.length / 1000) * 2 * (travelTime + totalDeliveryHours)
        else:
            totalDeliveryHours += travelTime

    return {"total-segments" : len(routeTaken),
            "total-miles" : totalMiles,
            "total-hours" : totalHours,
            "total-delivery-hours" : totalDeliveryHours, 
            "route-taken" : routeTaken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
