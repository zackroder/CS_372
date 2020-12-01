import random
from collections import defaultdict
#class to represent a game of Nim
#keeps track of pile sizes and determines which player wins
class NimGame():
    def __init__(self, pile1, pile2, pile3):
        self.pile1 = pile1
        self.pile2 = pile2
        self.pile3 = pile3
        #start with player A
        self.player = "A"

    def _end_of_game(self):
        if self.pile1 == 0 and self.pile2 == 0 and self.pile3 == 0:
            return True
        else:
            False

    def _update_player(self):
        if self.player == "A":
            self.player = "B"
        else:
            self.player = "A"

    #the functions to remove a stick from piles return true if it's end of game
    def remove_from_pile(self, pileNum, num_of_sticks):
        if pileNum == 1:
            self.pile1 -= num_of_sticks
        elif pileNum == 2:
            self.pile2 -= num_of_sticks
        else:
            self.pile3 -= num_of_sticks

        self._update_player()

        if self._end_of_game():
            return True
        else:
            return False
    
    def return_game_state_tuple(self):
        return (self.player, self.pile1, self.pile2, self.pile3)

#returns a random move (as a tuple (pile_num, numOfSticks)) given a game state tuple
def _pick_random_move(gameState):
    eligible_piles = []
    if gameState[1] != 0:
        eligible_piles.append(1)
    if gameState[2] != 0:
        eligible_piles.append(2)
    if gameState[3] != 0:
        eligible_piles.append(3)

    #list of tuples with (pile_num, amount_of_sticks) pairs
    possible_moves = []
    for pile in eligible_piles:
        for x in range(1, gameState[pile] + 1):
            possible_moves.append((pile, x))
    
    rand_move = random.choice(possible_moves)
    return rand_move

#returns lowest Q value given state S
def min_Q(Q_table, S):
    #verify that there exists an entry in the dict; if not, just return 0 (initial value for all Q[s,a])
    if S in Q_table:
        return min(Q_table[S].values())
    else:
        return 0
#highest Q value given state S
def max_Q(Q_table, S):
    if S in Q_table: 
        return max(Q_table[S].values())
    else:
        return 0


#returns a dictionary of Q-value 
def Q_learning(pile1, pile2, pile3, n):
    #dictionary of form Q["A123"]["01"] where A123 is state and 01 is action
    Q = defaultdict(dict)
    count = 0
    while count <= n:
        curr_game = NimGame(pile1, pile2, pile3)
        game_over = False
        while not game_over:
            gameState = curr_game.return_game_state_tuple()
            move = _pick_random_move(gameState)
            #execute move
            game_over = curr_game.remove_from_pile(*move)
            next_gameState = curr_game.return_game_state_tuple()

            #determine reward
            if game_over:
                if curr_game.player == "A":
                    r = 1000
                else:
                    r = -1000
            else:
                r = 0
            
            #have all Q values initialized to 0
            if gameState in Q and move in Q[gameState]:
                currQ = Q[gameState][move]
            else:
                currQ = 0

            #update Q value!
            if curr_game.player == "A":
                Q[gameState][move] = currQ + (r + 0.9*min_Q(Q, next_gameState) - currQ)
            else:
                Q[gameState][move] = currQ + (r + 0.9*max_Q(Q, next_gameState) - currQ)
        
        count += 1

    print(Q)

def main():
    Q_learning(0,1,2,100000)

if __name__ == "__main__":
    main()