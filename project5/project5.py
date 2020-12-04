import random
from collections import defaultdict
#class to represent a game of Nim
#keeps track of pile sizes and determines which player wins
class NimGame():
    def __init__(self, pile0, pile1, pile2):
        self.pile0 = pile0
        self.pile1 = pile1
        self.pile2 = pile2
        #start with player A
        self.player = "A"

    def _end_of_game(self):
        if self.pile0 == 0 and self.pile1 == 0 and self.pile2 == 0:
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
        if pileNum == 0:
            self.pile0 -= num_of_sticks
        elif pileNum == 1:
            self.pile1 -= num_of_sticks
        else:
            self.pile2 -= num_of_sticks

        self._update_player()

        if self._end_of_game():
            return True
        else:
            return False
    
    def return_game_state_tuple(self):
        return (self.player, self.pile0, self.pile1, self.pile2)

#returns a random move (as a tuple (pile_num, numOfSticks)) given a game state tuple
def _pick_random_move(gameState):
    eligible_piles = []
    if gameState[1] != 0:
        eligible_piles.append(0)
    if gameState[2] != 0:
        eligible_piles.append(1)
    if gameState[3] != 0:
        eligible_piles.append(2)

    #list of tuples with (pile_num, amount_of_sticks) pairs
    possible_moves = []
    for pile in eligible_piles:
        for x in range(1, gameState[pile+1] + 1):
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

#returns the action with highest Q value given state S
def arg_max(Q_table, S):
    return max(Q_table[S], key=Q_table[S].get)
def arg_min(Q_table, S):
    return min(Q_table[S], key=Q_table[S].get)


#returns a dictionary of Q-value 
def Q_learning(pile0, pile1, pile2, n):
    #dictionary of form Q["A123"]["01"] where A123 is state and 01 is action
    Q = defaultdict(dict)
    count = 0
    while count <= n:
        curr_game = NimGame(pile0, pile1, pile2)
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
            #if current player is A that means B just played (very confusing )
            if curr_game.player == "A":
                Q[gameState][move] = (r + 0.9*max_Q(Q, next_gameState))
            else:
                Q[gameState][move] = (r + 0.9*min_Q(Q, next_gameState))
        
        count += 1

    return Q

def print_q_table(Q):
    print("Final Q-Values:")
    for state in Q:
        print("Q values for state " + str(state))
        for action in Q[state]:
            print('\t' + str(action) + " = " + str(Q[state][action]))

#plays a game (CPU vs AI) given a table of Q values
def play_game(Q, pile0, pile1, pile2):
    whos_first = int(input("Who moves first, (1) User or (2) CPU? "))
    game = NimGame(pile0, pile1, pile2)

    #user goes first
    if whos_first == 1:
        game_over = False
        while not game_over:
            curr_state = game.return_game_state_tuple()
            if game.player == 'A':
                print("\nPlayer A's (user) turn; current game state is " + str(curr_state))
                pile_num = int(input("Which pile? "))
                amount = int(input("How many? "))
                game_over = game.remove_from_pile(pile_num, amount)
            elif game.player == 'B':
                print("\nPlayer B's (AI) turn; current game state is " + str(curr_state))
                #choose move with argmin
                move = arg_min(Q, curr_state)
                print("Computer chooses pile " + str(move[0]) + " and removes " + str(move[1]))
                game_over = game.remove_from_pile(*move)

        
        print("Game over.")
        print("Winner is " + game.player + (" (AI)" if game.player == "B" else " (User)"))
    elif whos_first == 2:
        game_over = False
        while not game_over:
            curr_state = game.return_game_state_tuple()
            if game.player == 'B':
                print("\nPlayer B's (user) turn; current game state is " + str(curr_state))
                pile_num = int(input("Which pile? "))
                amount = int(input("How many? "))
                game_over = game.remove_from_pile(pile_num, amount)
            elif game.player == 'A':
                print("\nPlayer A's (AI) turn; current game state is " + str(curr_state))
                #choose move with argmin
                move = arg_max(Q, curr_state)
                print("Computer chooses pile " + str(move[0]) + " and removes " + str(move[1]))
                game_over = game.remove_from_pile(*move)
        
        print("Game over.")
        print("Winner is " + game.player + (" (AI)" if game.player == "A" else " (User)"))
    

def main():
    pile0 = int(input("Number in pile 0? "))
    pile1 = int(input("Number in pile 1? "))
    pile2 = int(input("Number in pile 2? "))
    n = int(input("Number of games to simulate? "))
    Q = Q_learning(pile0, pile1, pile2, n)
    print_q_table(Q)

    keep_going = True

    while keep_going:
        play_game(Q, pile0, pile1, pile2)
        again = int(input("Play again? (1) Yes or (2) No: "))
        keep_going = (again == 1)

if __name__ == "__main__":
    main()