* Othello AI

        This is an AI program designed to play the game of Othello. 
        Othello, also known as Reversi, is a two-player strategy board game. 
        The goal of the game is to have the majority of 
        your colored pieces on the board at the end of the game.

* How to Play

       Clone the repository: git clone https://github.com/your-username/othello-ai.git
       Navigate to the project directory: cd othello-ai
       Run the program: python othello.py
       Follow the prompts to indicate the initial player and make your moves.
* Game Rules 
  
       - The game board is a 8x8 grid.
       - The initial board setup consists of two black and two white pieces placed diagonally in the center.
       - Players take turns placing their colored pieces on the board, with black always starting.
       - A player must place their piece in such a way that there is at least one straight 
         (horizontal, vertical, or diagonal) line between the new piece and another piece of their own color.
       - Any opponent's pieces that are in a straight line between the new piece and another piece of the player's color 
         are flipped to the player's color.
       - If a player cannot make a valid move, their turn is skipped.
       - The game ends when no more valid moves can be made by either player or when the board is completely filled.
       - The player with the most pieces of their color on the board at the end of the game wins.

* AI Algorithm

       The AI algorithm used in this program is a variant of the Minimax algorithm, 
       combined with the Alpha-Beta Pruning optimization.
       It searches through the game tree to find the best possible move for the computer player. 
       The evaluation function uses several heuristics, including the difference in the number of pieces, 
       the number of surrounded pieces, the mobility of each player, the control of the center, 
       and the control of the corners.

* Credits

       The Othello AI program is implemented using Python and is based on the 
       Othello game implementation by Evyatar Baruch and Sapir Bashan.
       If you have any questions or feedback, 
      please feel free to contact us at [sapirbashan1@gmail.com or evyatarmader@gmail.com]
       Enjoy playing Othello against the AI!

