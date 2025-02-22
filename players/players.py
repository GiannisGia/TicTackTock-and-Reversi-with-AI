"""
## players.py

It contains several types of players for a game, each with a different strategy:

Functions:
- manual_player(game, state): A player that manually inputs their move.
- minmax_player(game, state): A player that uses the Minimax algorithm to decide their move.
- random_player(game, state): A player that randomly selects their move.
- alpha_beta_player(game, state): A player that uses the Alpha-Beta pruning algorithm to decide their move.
- mcts_player(game, state): A player that uses the Monte Carlo Tree Search algorithm to decide their move.

Each player function takes a game object and a state object as parameters and returns a move.

Authors: 
- Giannopoulos Georgios
- Giannopoulos Ioannis
"""
import numpy as np
import random

from gamestate.gamestate import GameState
from game.game import Game
from game.tic_tac_toe import TicTacToe
from game.reversi import Reversi
from monte_carlo.monte_carlo_tree_search import monte_carlo_tree_search

def manual_player(game, state):
    """A manual player."""
    game.display(state)
    actions = game.actions(state)
    while True:
        action = input("Enter your move (e.g., 2,3): ")
        try:
            action = action.split(',')
            action = [int(v) for v in action]
            action = tuple(action)
            if action not in actions:
                print('invalid action!!')
            else:
                return action
        except:
            print('invalid action!!')

def minmax_player(game, state):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))

def random_player(game, state):
    """
    Randomly selects a move from the list of legal moves in the given game state.

    Args:
        game: The game object representing the game being played.
        state: The current state of the game.

    Returns:
        The randomly selected move.
    """
    legal_moves = game.actions(state)
    # count the number of legal moves
    num_legal_moves = len(legal_moves)
    # choose a random move
    # random_move = np.random.choice(num_legal_moves, 
    #                                p=[1/num_legal_moves for _ in range(num_legal_moves)])
    random_move = np.random.choice(num_legal_moves)
    # print(f"Debug: random_move = {game.actions(state)[random_move]}\nprobability: {[1/num_legal_moves for _ in range(num_legal_moves)]}")
    return game.actions(state)[random_move]

def alpha_beta_player(game, state):
    """
    Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states using alpha-beta pruning.

    Args:
        game: The game object representing the game being played.
        state: The current state of the game.
    
    Returns:
        The best move for the given state.
    """

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    alpha = -np.inf
    beta = np.inf
    best_score = -np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), alpha, beta)
        alpha = max(alpha, v)
        if v > best_score:
            best_score = v
            best_action = a
    
    return best_action  

def mcts_player(game, state):
    """
    A player that uses Monte Carlo Tree Search (MCTS) algorithm to make decisions.

    Parameters:
    - game: The game object representing the game being played.
    - state: The current state of the game.

    Returns:
    - The best move determined by the MCTS algorithm.

    """
    return monte_carlo_tree_search(state, game)

def alpha_beta_cutoff_player(game, state, depth=3):
    """
    This function represents an alpha-beta cutoff player that uses the alpha-beta cutoff search algorithm and 
    an evaluation function to make decisions in a game.

    Parameters:
    - game: The game object representing the game being played.
    - state: The current state of the game.
    - depth: The maximum depth to search in the game tree (default=3).

    Returns:
    - The best move determined by the alpha-beta cutoff search algorithm and the .
    """
    return game.alpha_beta_cutoff_search(state, depth)