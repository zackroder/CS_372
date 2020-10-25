import numpy as np
from collections import defaultdict

DEBUG = True

class BallroomBayesNet():
    def __init__(self, m,n):
        self.width = m
        self.height = n

        #dictionaries to store CPTs
        self.l_CPT = defaultdict(dict)
        self.c_CPT = defaultdict(dict)
        self.m1_CPT = defaultdict(dict)
        self.m2_CPT = defaultdict(dict)
        self.s_CPT = defaultdict(dict)
        self.possibleLocations = []
        
        for i in range(m):
            for j in range(n):
                self.possibleLocations.append((i,j))
        #initialize last location CPT 
        for location in self.possibleLocations:
            self.l_CPT[location] = (1.0 / (self.width*self.height))
    
    def _generate_list_of_locations_one_step_away(self,x,y):
        output = []
        if x - 1 >= 0:
            output.append((x-1, y))
        if x + 1 < self.width:
            output.append((x+1, y))

        if y - 1 >= 0:
            output.append((x, y-1))
        if y + 1 < self.height:
            output.append((x, y+1))

        return output
    
    def _generate_list_of_locations_two_steps_away(self, x,y):
        output = []
        if x - 2 >= 0:
            output.append((x-2, y))
        if x + 2 < self.width:
            output.append((x+2, y))

        if y - 2 >= 0:
            output.append((x, y-2))
        if y + 2 < self.height:
            output.append((x, y+2))

        toCheck = [(1,1), (-1,1), (1,-1), (-1,-1)]
        for i in toCheck:
            if x + i[0] >= 0 and x + i[0] < self.width:
                if y + i[1] >= 0 and y + i[1] < self.height:
                    output.append((x + i[0], y + i[1]))
        
        return output
     
     #generates probabilities for C given L (x,y)
    def _generate_c_prob(self, x, y):
        possibleNextLocations = self._generate_list_of_locations_one_step_away(x,y)
        for loc2 in possibleNextLocations:
            self.c_CPT[(x,y)][loc2] = (1.0 / len(possibleNextLocations))
    
    #generates probability of M1=True given C (x,y)
    def _generate_m1_prob(self, x, y):
        #if monkey isn't in m1 line of sight, prob is 0.05
        if x != 0 or y != 0:
            self.m1_CPT[(x,y)] = 0.05
        else:
            if y == 0:
                self.m1_CPT[(x,y)] = 0.9 - (0.1*x)
            elif x == 0:
                self.m1_CPT[(x,y)] = 0.9 - (0.1*y)
    
    #generates probability of M2=True given C (x,y)
    def _generate_m2_prob(self, x, y):
        if x != self.width - 1 or y != self.height - 1:
            self.m2_CPT[(x,y)] = 0.05
        else:
            if y == self.height - 1:
                dist = (self.width-1) - x  
                self.m2_CPT[(x,y)] = 0.9 - (0.1*dist)
            elif x == self.width - 1:
                dist = (self.height-1) - y
                self.m2_CPT[(x,y)] = 0.9 - (0.1*dist)

    #generates probabilities for S given C (x,y)
    def _generate_S_prob(self, x, y):
        self.s_CPT[(x,y)][(x,y)] = 0.6
        locationsOneAway = self._generate_list_of_locations_one_step_away(x,y)

        for loc in locationsOneAway:
            self.s_CPT[(x,y)][loc] = (0.30 / len(locationsOneAway))

        locationsTwoAway = self._generate_list_of_locations_two_steps_away(x,y)

        for loc in locationsTwoAway:
            self.s_CPT[(x,y)][loc] = (0.10 / len(locationsTwoAway))


def main():
    test = BallroomBayesNet(2,2)
    test._generate_c_prob(0,1)
    test._generate_m1_prob(1,1)
    test._generate_m2_prob(1,1)
    test._generate_S_prob(1,1)

    print(test.c_CPT)
    print(test.l_CPT)
    print(test.m1_CPT)
    print(test.m2_CPT)
    print(test.s_CPT)

main()