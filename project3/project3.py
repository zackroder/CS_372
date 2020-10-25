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
        if x != 0 and y != 0:
            print("hmmmm")
            self.m1_CPT[(x,y)][True] = 0.05
            self.m1_CPT[(x,y)][False] = 1.0 - self.m1_CPT[(x,y)][True]
        else:
            if y == 0:
                self.m1_CPT[(x,y)][True] = 0.9 - (0.1*x)
                self.m1_CPT[(x,y)][False] = 1.0 - self.m1_CPT[(x,y)][True]
            elif x == 0:
                self.m1_CPT[(x,y)][True] = 0.9 - (0.1*y)
                self.m1_CPT[(x,y)][False] = 1.0 - self.m1_CPT[(x,y)][True]
    
    #generates probability of M2=True given C (x,y)
    def _generate_m2_prob(self, x, y):
        if x != self.width - 1 and y != self.height - 1:
            self.m2_CPT[(x,y)][True] = 0.05
            self.m2_CPT[(x,y)][False] = 1.0 - self.m2_CPT[(x,y)][True]
        else:
            if y == self.height - 1:
                dist = (self.width-1) - x  
                self.m2_CPT[(x,y)][True] = 0.9 - (0.1*dist)
                self.m2_CPT[(x,y)][False] = 1.0 - self.m2_CPT[(x,y)][True]
            elif x == self.width - 1:
                dist = (self.height-1) - y
                self.m2_CPT[(x,y)][True] = 0.9 - (0.1*dist)
                self.m2_CPT[(x,y)][False] = 1.0 - self.m2_CPT[(x,y)][True]

    #generates probabilities for S given C (x,y)
    def _generate_S_prob(self, x, y):
        
        locationsOneAway = self._generate_list_of_locations_one_step_away(x,y)

        for loc in locationsOneAway:
            self.s_CPT[(x,y)][loc] = (0.30 / len(locationsOneAway))

        locationsTwoAway = self._generate_list_of_locations_two_steps_away(x,y)

        for loc in locationsTwoAway:
            self.s_CPT[(x,y)][loc] = (0.10 / len(locationsTwoAway))

        #assign all other possible locations not one or two away a prob of 0
        others = list(set(self.possibleLocations) - set(locationsOneAway) - set(locationsTwoAway))
        for loc in others:
            self.s_CPT[x,y][loc] = 0.0
        self.s_CPT[(x,y)][(x,y)] = 0.6
        #print(self.s_CPT)

    #calculates (un-normalized) probability for a given C (x,y) given m1, m2, and s
    def _calculate_prob_of_C(self, c_x, c_y, m1: bool, m2:bool, s_x, s_y):
        self._generate_m1_prob(c_x, c_y)
        self._generate_m2_prob(c_x, c_y)
        self._generate_S_prob(c_x, c_y)

        #sum over all possible last locations
        posibleLastLocations = self._generate_list_of_locations_one_step_away(c_x, c_y)
        prob = 0.0
        if DEBUG:
            print("Calculating total probability for current location (" + str(c_x) + ", " + str(c_y) + ")" )

        for l in posibleLastLocations:
            self._generate_c_prob(*l)
            if DEBUG:
                print("\tEvaluating for last location " + str(l))
                print("\t \t Multiplying: " + str(self.l_CPT[l]) + " " + str(self.c_CPT[l][(c_x, c_y)]) + " " +
                str(self.m1_CPT[(c_x, c_y)][m1]) + " " + str(self.m2_CPT[(c_x, c_y)][m2]) + " " +
                str(self.s_CPT[(c_x, c_y)][(s_x, s_y)]))

            prob += (self.l_CPT[l] * self.c_CPT[l][(c_x, c_y)] * self.m1_CPT[(c_x, c_y)][m1]
                    * self.m2_CPT[(c_x, c_y)][m2] * self.s_CPT[(c_x, c_y)][(s_x, s_y)])
        
        return prob
    
    #generates prob distribution over all possible values of C given values of m1, m2, and s
    def get_distrib_over_all_C(self, m1: bool, m2:bool, s_x, s_y):
        #dict to store un-normalized values to be normalized and stored in self.c_CPT
        unnormalized = defaultdict(dict)
        #loop over all values on the board
        for loc in self.possibleLocations:
            unnormalized[loc] = self._calculate_prob_of_C(*loc, m1, m2, s_x, s_y)

        print(unnormalized)




def main():
    test = BallroomBayesNet(3,3)

    #print(test.c_CPT)
    #print(test.l_CPT)
    print(test.get_distrib_over_all_C(False, False, *(0,1)))

    #locationsTwoAway = test._generate_list_of_locations_two_steps_away(2,0)
    #print(locationsTwoAway)

main()