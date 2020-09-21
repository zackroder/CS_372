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
            self.adjList[locId] = {"longitude": float(longitude), "latitude": float(latitude), "roads": []}
    
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
        lat1 = self.adjList[loc1Id]["latitude"]
        lat2 = self.adjList[loc2Id]["latitude"]

        long1 = self.adjList[loc1Id]["longitude"]
        long2 = self.adjList[loc2Id]["longitude"]

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

    def reconstructuPath(self, cameFrom, current):
        path = []

        while current in cameFrom.keys():
            current = cameFrom[current]
            path.insert(0, current)
        
        return path 
    def findBestPathByAStar(self, startId, goalId):
        frontier = PQueue()
        if DEBUG:
            print("Routing from " + startId + " to " + goalId)

        #dictionaries to keep track of path costs as we proceed!
        #for locId n, cameFrom[n] is location Id immediately
        #proceeding it on cheapest path from startId
        cameFrom = {}
        #for locId n, gScore[n] returns currently known cheapest g path
        gScore = {}
        #for locId n, hScore[n] returns currently known cheapest h path
        hScore = {}

        #enqueue start node
        frontier.enqueue(startId, 0)

        hScore[startId] = self.heuristicFunction(startId, goalId)
        gScore[startId] = 0.0
        while not frontier.empty():
            #get item off queue  
            currLocId = frontier.dequeue()
            #retrieve g and h values
            g = gScore[currLocId]
            h = hScore[currLocId]
            f = g+h
            if DEBUG:
                print("Location " + currLocId + " popped off frontier.")
                print("\t g = ", g)
                print("\t h = ", h)
                print("\t f = ", f)

            #we found it!
            if currLocId == goalId:
                #reconstruct path and return it
                return self.reconstructuPath(cameFrom, currLocId)

            #loop through accessible roads and evaluate each one then add to priority queue
            for road in self.adjList[currLocId]["roads"]:
                destId = road["destId"]
                speedLimit = float(road["speedLimit"])

                #f(n) = g(n) + h(n)

                #straight line distance is equal to length of the road, since we assume only line segment roads
                gTemp = gScore[currLocId] + (self.distBetweenTwoLocationsInMiles(currLocId, destId) / speedLimit)
                hTemp = self.heuristicFunction(currLocId, goalId)
                fTemp = g + h


                if not frontier.contains(destId):
                    #add it to frontier if it isnt already there
                    frontier.enqueue(destId, fTemp)
                    
                    #add to cameFrom
                    cameFrom[destId] = currLocId

                    #store g and h values for future lookup
                    gScores[destId] = gTemp
                    hScores[destId] = hTemp
                    if DEBUG:
                        print("Location " + destId + " added to frontier.")
                        print("\t g = ", gTemp)
                        print("\t h = ", hTemp)
                        print("\t f = ", fTemp)
                elif frontier.contains(destId) and estSolCost < frontier.get_priority(fTemp):
                    #if it is already in the frontier but new cost is lower, update the frontier
                    frontier.change_priority(destId, fTemp)
                    if DEBUG:
                        print("Location " + destId + " priority updated.")
                        print("==Old costs==")
                        print("\t g = ", gScore[destId])
                        print("\t h =", hScore[destId])
                        print("\t f = ", gScore[destId] + hScore[destId])
                        print("==Updated Costs==")
                        print("\t g = ", gTemp)
                        print("\t h =", hTemp)
                        print("\t f = ", fTemp)
                    #store updated and h values for future lookup
                    gScore[destId] = gTemp
                    hScore[destId] = hTemp

                    #better path found; update cameFrom
                    cameFrom[destId] = currLocId


    def printAdjList(self):
        print(self.adjList)


def main():
    fileName = input("Input filename (.txt): ")

    network = RoadNetwork()

    network.create_graph(fileName)

    locId1 = input("Enter one location ID: ")
    locId2 = input("Enter another location ID: ")
    
    path = network.findBestPathByAStar(locId1, locId2)
    print(path)



if __name__ == "__main__":
    main()