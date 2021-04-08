Hue Truong
CSC 383 -- Connect 383

Given a connect-4 like game, the intent of this project is to use different implementations of minimax to create
a bot.
There are four different agents aside from the human player implemented:
    1. Random Agent -- Randomly picks from available states
    2. Minimax Agent -- Uses minimax algorithm to determine utility value without a depth limit
    3. Minimax Heuristic Agent -- Depth-limited minimax algorithm with evaluation method
    4. Minimax Prune Agent -- Minimax algorithm with alpha-beta pruning method

Agents 2, 3, 4 are based off of textbook minimax algorithm that performs recursive calls to find the minimum of MAX best move,
or vice versa. The evaluation function of agent 3 uses the current state of the board, given the depth limit, to distribute a
utility score. The function uses characteristics of the board state, such as center control and unblocked streaks, to calculate
an evaluation score.

Evaluation method tested as follows:
The evaluation agent played the Random agent in a simulated game. 100 games were played in each trial. Totalling 10 trials,
win rate of the evaluation agent against the random bot is 88%, win rate of the random agent was 11.4%, and ties made up
.6% of the sample data.

'383_coding.pdf' - Project details
'agents.py' - file including agents and their methods
'connect383.py' - main file including game board and init 


