# Python3 program to demonstrate
# working of Alpha-Beta Pruning

# Initial value_arr of Alpha and Beta
MAX, MIN = 1000, -1000


# Returns optimal value_arr for current player
# (Initially called for root and maximizer)
def minimax(depth, node_index, maximizing_player, value_arr, alpha, beta):
    # Terminating condition. i.e
    # leaf node is reached
    if depth == 3:
        return value_arr[node_index]

    if maximizing_player:

        best = MIN

        # Recur for left and right children
        for i in range(0, 2):
            val = minimax(depth + 1, node_index * 2 + i,False, value_arr, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best
    else:
        best = MAX

        # Recur for left and
        # right children
        for i in range(0, 2):
            val = minimax(depth + 1, node_index * 2 + i,True, value_arr, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best
