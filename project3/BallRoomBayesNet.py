from collections import defaultdict

class BallroomBayesNet():
    def __init__(self, m, n, debug = True):
        self.width = m
        self.height = n

        #dictionaries to store CPTs
        self.l_CPT = defaultdict(dict)
        self.c_CPT = defaultdict(dict)
        self.m1_CPT = defaultdict(dict)
        self.m2_CPT = defaultdict(dict)
        self.s_CPT = defaultdict(dict)
        self.possibleLocations = []
        self.DEBUG = debug

        for i in range(m):
            for j in range(n):
                self.possibleLocations.append((i,j))
        #initialize last location CPT and initialize current location CPT
        for location in self.possibleLocations:
            self.l_CPT[location] = (1.0 / (self.width*self.height))
            self._generate_c_prob(*location)
            self._generate_m1_prob(*location)
            self._generate_m2_prob(*location)
            self._generate_S_prob(*location)

        if self.DEBUG:
            self._print_last_location_dist()
            self._print_current_location_dist()
            self._print_m1_dist()
            self._print_m2_dist()
            self._print_s_dist()

    
    def _print_last_location_dist(self):
        print("Last location distribution:")
        for key in self.l_CPT:
            print("\t Last location: " + str(key) + ", prob: " + str(self.l_CPT[key]))
        print('\n')

    def _print_current_location_dist(self):
        print("Current location distribution: ")
        for lastLoc in self.c_CPT:
            print("\tLast location: " + str(lastLoc))
            for currLoc in self.c_CPT[lastLoc]:
                if self.c_CPT[lastLoc][currLoc] != 0.0:
                    print("\t\tCurrent location: " + str(currLoc) + ", prob: " + str(self.c_CPT[lastLoc][currLoc]))

        print('\n')
    def _print_m1_dist(self):
        print("Motion sensor #1 distribution: ")
        for currLoc in self.m1_CPT:
            print("\tCurrent location: " + str(currLoc) + ", True prob: " + str(self.m1_CPT[currLoc][True])
            + ", False prob: " + str(self.m1_CPT[currLoc][False]))
        print('\n')

    def _print_m2_dist(self):
        print("Motion sensor #2 distribution: ")
        for currLoc in self.m1_CPT:
            print("\tCurrent location: " + str(currLoc) + ", True prob: " + str(self.m2_CPT[currLoc][True])
            + ", False prob: " + str(self.m2_CPT[currLoc][False]))
        print('\n')

    def _print_s_dist(self):
        print("Sound sensor distribution: ")
        for currLoc in self.s_CPT:
            print("\tCurrent location: " + str(currLoc))
            for sLoc in self.s_CPT[currLoc]:
                if self.s_CPT[currLoc][sLoc] != 0.0:
                    print("\t\t Sound reported at: " + str(sLoc) + ", prob: " + str(self.s_CPT[currLoc][sLoc]))

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
        #set prob 0 for all tiles that can't be reached
        for loc2 in list(set(self.possibleLocations) - set(possibleNextLocations)):
            self.c_CPT[(x,y)][loc2] = 0.0
    
    #generates probability of M1=True given C (x,y)
    def _generate_m1_prob(self, x, y):
        #if monkey isn't in m1 line of sight, prob is 0.05
        if x != 0 and y != 0:
            self.m1_CPT[(x,y)][True] = 0.05
            self.m1_CPT[(x,y)][False] = 0.95
        else:
            if y == 0:
                val = 0.9 - (0.1*x)
                self.m1_CPT[(x,y)][True] = val
                self.m1_CPT[(x,y)][False] = 1.0 - val
            elif x == 0:
                val = 0.9 - (0.1*y)
                self.m1_CPT[(x,y)][True] = val
                self.m1_CPT[(x,y)][False] = 1.0 - val
    
    #generates probability of M2=True given C (x,y)
    def _generate_m2_prob(self, x, y):
        if x != self.width - 1 and y != self.height - 1:
            self.m2_CPT[(x,y)][True] = 0.05
            self.m2_CPT[(x,y)][False] = 0.95
        else:
            if y == self.height - 1:
                dist = (self.width-1) - x
                val = 0.9 - (0.1*dist)
                self.m2_CPT[(x,y)][True] = val
                self.m2_CPT[(x,y)][False] = 1.0 - val
            elif x == self.width - 1:
                dist = (self.height-1) - y
                val = 0.9 - (0.1*dist)
                self.m2_CPT[(x,y)][True] = val
                self.m2_CPT[(x,y)][False] = 1.0 - val

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
        #sum over all possible last locations
        prob = 0.0
        if self.DEBUG:
            print("Calculating total probability for current location (" + str(c_x) + ", " + str(c_y) + ")" )

        for l in self.possibleLocations:
            if self.DEBUG:
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

        #variable to store sum of un-normalized probabilities
        sum_of_unnormalized = 0.0

        #loop over all values on the board
        for loc in self.possibleLocations:
            unnormalized[loc] = self._calculate_prob_of_C(*loc, m1, m2, s_x, s_y)
            sum_of_unnormalized += unnormalized[loc]

        #dictionary to store normalized probabilities
        normalized = defaultdict(dict)

        #normalization
        for loc in unnormalized:
            normalized[loc] = (unnormalized[loc] / sum_of_unnormalized)

        if self.DEBUG:
            print("BEFORE NORMALIZATION:")
            for loc in unnormalized:
                print("\t Location: " + str(loc) + ", prob: " + str(unnormalized[loc]))
            print("AFTER NORMALIZATION:")

        for loc in normalized:
            print("\t Location: " + str(loc) + ", prob: " + str(normalized[loc]))

        #then, we set l_cpt equal to normalized
        self.l_CPT = normalized

