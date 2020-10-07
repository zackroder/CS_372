##HEURISTIC INFO##

My heuristic function assigns value to n-1 pieces in a row and n-2 pieces in a row.
It evaluates the whole board and assigns the following values:
    3 points for n-2 in-a-row (3 total)
    7 additional points for n-1 in-a-row (10 total)

Thus, the algorithim seeks out moves that put it in a position to win (n-1 in-a-row)

It seems to work best at depth of 6 or greater.