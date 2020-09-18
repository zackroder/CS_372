import math 
from pqueue import PQueue

DEBUG = True

#hashable dictionary to use in pqueue class
class hDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items)))
    def __eq__(self, other):
        return self.__key() == other.__key()

class RoadNetwork:
    def __init__(self):
        #adj list as dict
        self.adjList = {}

    def AddLocation(self, locId, longitude, latitude):
        if locId not in self.adjList:
            self.adjList[locId] = {"longitude": longitude, "latitude": latitude, "roads": []}
    
    def AddRoad(self, locId1, locId2, speedLimit, name):
        #append dict object with road info (destId, name, speed limit)
        self.adjList[locId1]["roads"].append({"name": name, "destId": locId2, "speedLimit": speedLimit})
        self.adjList[locId2]["roads"].append({"name": name, "destId": locId1, "speedLimit": speedLimit})

    def create_graph(self, fileName):
        try:
            f = open(fileName)
            lines = f.readlines()
        except IOError as e:  
            print("Invalid file name! Try again.")
            raise e

        #read through file line by line
        for l in lines:
            line = l.rstrip()
            lineSplit = line.split("|")
            if lineSplit[0] == 'location':
                self.AddLocation(lineSplit[1], lineSplit[2], lineSplit[3])
            elif lineSplit[0] == 'road':
                self.AddRoad(lineSplit[1], lineSplit[2], lineSplit[3], lineSplit[4])

    
    def PrintAdjLocations(self, locId):
        locId = str(locId)
        if locId in self.adjList.keys():
            print("Location " + locId + " has edges leading to:")
            for road in self.adjList[locId]["roads"]:
                print('\t' + road["destId"] + " " + road["speedLimit"] + " mph " + road["name"])
        else:
            print("Invalid location ID.")
    
    #compute distance using spherical coordinates
    def distBetweenTwoLocationsInMiles(self, loc1Id, loc2Id):
        lat1 = self.adjList["loc1Id"]["latitude"]
        lat2 = self.adjList["loc2Id"]["latitude"]

        long1 = self.adjList["loc1Id"]["longitude"]
        long2 = self.adjList["loc2Id"]["longitude"]

        degreesToRadians = math.pi/180.0

        phi1 = (90.0 - lat1)*degreesToRadians
        phi2 = (90.0 - lat2)*degreesToRadians

        theta1 = long1*degreesToRadians
        theta2 = long2*degreesToRadians

        #arclength
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
        arc = math.acos(cos)

        #multiply by radius of earth in miles to get mile distance
        return arc*3960.0

    #heuristic for A* search is time for straight-line travel time from n to goal state, driving at 65mph
    def heuristicFunction(self, nodeNId, goalNodeId):
        distance = self.distBetweenTwoLocationsInMiles(nodeNId, goalNodeId)
        return (distance / 65.0)

    def findBestPathByAStar(self, startId, goalId):
        frontier = PQueue()
        #enqueue start node
        frontier.enqueue(startId, 0)

        while not frontier.empty():
            #get item off queue  
            currLocId = frontier.dequeue()
            if DEBUG:
                print("Location " + currLocId + " popped off frontier.")
                print("\t g = ", g)
                print("\t h = ", h)
                print("\t f = ", f)

            if currLocId = goalId:
                break

            #loop through accessible roads and evaluate each one then add to priority queue
            for road in self.adjList[currLocId]:
                destId = road["destId"]
                speedLimit = float(road["speedLimit"])

                #f(n) = g(n) + h(n)
                g = self.distBetweenTwoLocationsInMiles(currLocId, destId) / speedLimit
                h = heuristicFunction(currLocId, goalId)
                f = g + h


                if not frontier.contains(destId):
                    #add it to frontier if it isnt already there
                    frontier.enqueue(destId, estSolCost)
                    if DEBUG:
                        print("Location " + destId + " added to frontier.")
                        print("\t g = ", g)
                        print("\t h = ", h)
                        print("\t f = ", f)
                elif frontier.contains(destId) and estSolCost < frontier.get_priority(destId):
                    #if it is already in the frontier but new cost is lower, update the frontier
                    frontier.change_priority(destId, estSolCost)




    def printAdjList(self):
        print(self.adjList)


def main():
    fileName = raw_input("Input filename (.txt): ")

    network = RoadNetwork()

    network.create_graph(fileName)

    locId = input("Enter a location ID (or 0 to quit): ")
    while (locId != 0):
        network.PrintAdjLocations(locId)
        locId = input("Enter a location ID (or 0 to quit): ")



if __name__ == "__main__":
    main()