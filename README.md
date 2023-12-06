##  How to run the Program  

1- Go to the main.py and run 

2- you will get message in the terminal 
            ” Start Program 
              if you want to start playing press Y, if you want to train machine press T”  then choose y or choose t to train reinforcement q learning 
              if you chose “y,” and then you would get another message “If you would like to play multiplier press 1, or vs computer with Minimax pruning Algorithm press 2, or play with reinforcement computer                  press 3” 
              then you can play 

##  Mancala Game and Artificial Intelligence  
  

The game of Mancala is a two-player strategy game whose objective is to allow the player to determine which bin will give the maximum number of overlapping turns which will allow for the player to accumulate the maximum number of stones in the player’s home bin. The game begins with a predefined number of stones, which is usually four stones in each player’s array of bins. 

The board consists of 12 bins, 6 on each side, and 2 home bins with one on each player’s side for each player to collect stones. The board is laid out typically starting with four stones in each of the 12 bins, leaving the home bins empty. The first player should choose a bin on their side and collect all the stones from the bin and move anti-clockwise, placing one stone in each bin including the home bin until all stones have been placed. The player must not put a stone on the opposing player’s home bin. If the last stone is placed in the player’s home bin, the player should choose a new bin on their side to take stones from and repeat the process again. If the last stone is placed in an empty bin, the player’s turn has ended. If a player does not have stones left in their side of the board, their turn is skipped. The player with the maximum number of stones in their home bin is the winner. This literature review will cover the adversarial algorithms and strategies of the game to assist players in gaining the maximum number of stones in the home bin. 
  
  

<div align="center">
<img src="https://i.etsystatic.com/15406866/r/il/c81d23/4745769361/il_1588xN.4745769361_qm6m.jpg" align="center" height="250" width="400" />
</div>  
  

### Adversarial Search Algorithms   

  

There are two algorithm techniques within the game Mancala. The first algorithm is the Minimax Algorithm. The Minimax algorithm operates by constructing a game tree, representing all moves and their consequences, and then recursively evaluating the nodes of the tree to determine the best move at each level. The Minimax Algorithm can find an optimal solution even if the game tree is finite. Time and space complexity is O(b^m), where b is the average number of moves per state, and m is the maximum depth of the game tree. The pseudo code of the algorithm. The primary challenge with the Minimax Algorithm lies in its requirement to evaluate an exponentially increasing number of game states as the depth of the game tree increases. While we cannot eliminate the exponential growth, we can effectively cut it in half and compute the correct minimax decision without looking at every node in the game tree. This leads us to the Minimax Alpha-beta pruning algorithm.  
  
  

**function minimax(node, depth, maximizingPlayer) is  
&nbsp;&nbsp;if depth ==0 or node is a terminal node then  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return static evaluation of node👍
  
&nbsp;&nbsp;if MaximizingPlayer then      // for Maximizer Player  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; maxEva= -infinity            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  for each child of node do  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; eva= minimax(child, depth-1, false)🔃 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;maxEva= max(maxEva,eva)        //gives Maximum of the values  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return maxEva👍
  
&nbsp;&nbsp;&nbsp; else                         // for Minimizer player  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;minEva= +infinity   
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for each child of node do  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; eva= minimax(child, depth-1, true)  🔃 <br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;minEva= min(minEva, eva)         //gives minimum of the values  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return minEva 👍**  
  

The Mini max Alpha-Beta Pruning Algorithm is an idea based on the pruning concept which reducing the number of branches searched during a traversal of the tree and ignores parts of the tree from consideration without having to examine them. This algorithm is a Mini max algorithm with two parameters, alpha and beta. Alpha, being the highest-value option discovered thus far along the path for the maximum player, and Beta, being the lowest-value option identified up to this point along the path for the minimum player. The technique of alpha–beta pruning that has been applied to the Mini max tree, returns the same moves but ignores parts of the tree that is impossible to visit. Mini max alpha-beta pruning algorithm minimizes the exponential to half, time & space complexity is O(b^m/2). The below figure shows pseudo code of the algorithm.  
  

function minimax(node, depth, alpha, beta, maximizingPlayer) is  
&nbsp;&nbsp;&nbsp;&nbsp;if depth ==0 or node is a terminal node then  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return static evaluation of node  👍
  
&nbsp;&nbsp;&nbsp;&nbsp;if MaximizingPlayer then      // for Maximizer Player  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; maxEva= -infinity            
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for each child of node do  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  eva= minimax(child, depth-1, alpha, beta, False)  🔃 <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; maxEva= max(maxEva, eva)   
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; alpha= max(alpha, maxEva)      
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if beta<=alpha  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; return maxEva  👍
    
&nbsp;&nbsp;&nbsp;&nbsp;else                         // for Minimizer player  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;minEva= +infinity   
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for each child of node do  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  eva= minimax(child, depth-1, alpha, beta, true)  🔃 <br/>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;minEva= min(minEva, eva)   
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; beta= min(beta, eva)  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; if beta<=alpha  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break          
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return minEva  👍  
  

### Reinforcement Technique  
  

In the Q-Learning algorithm, the goal is to learn iteratively the optimal Q-value function using the Bellman Optimality Equation. To do so, we store all the Q-values in a table that we will update at each time step using the Q-Learning iteration:  
  

<div align="center">
<img src="https://miro.medium.com/v2/resize:fit:786/format:webp/1*y0V_OFDJIcamdP7kCw7v5Q.png" align="center" height="" width="" />
</div>  
  

where α is the learning rate, an important hyperparameter that we need to tune since it controls the convergence.  
  

<div align="center">
<img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*qksGasRhHjthcDgQFTodJg@2x.png" align="center" style="width: 100%" />
</div>  
  

### Class diagrams   
  

<div align="center">

<img src="![class diagram mancala drawio (1)](https://github.com/MarkGeorge10/Mancala-Game-AI/assets/34999954/e9081922-3902-4f73-aacf-d1d71a030546)" align="center" height="500" width="" />
</div>  
  


