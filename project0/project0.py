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

        #open file
        f = open(fileName)
        lines = f.readlines()

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
                print(road["destId"] + " " + road["speedLimit"] + " mph " + road["name"])
        else:
            print("Invalid location ID.")
    
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