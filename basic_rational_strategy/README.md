# purgatorybsr



Run simulation.py

The program does the following

Input: n Number of players to start with:
    F (payment that allows a player to go to heaven):
    Q (fine imposed on hell-bound players):
    K (first K players go to hell):
   T (players that survive T iterations go to heaven):
    integer p between 0 and 999 (each player forgets to play with probability p/1000):

The program adds n players to the queue. Each player added has the following properties:
-player remembers payment history
-player has a strategy which decides what to pay in next iteration (in any iteraton player's payment increases by stratregy).
-player knows her total payment.
-player knows time spent in queue (initialised at t=0)
-player knows her position in the queue
-with probability p/1000 he has paid 1 and has strategy of paying 1 on entering the queue.

Each iteration runs as follows:
First K players in the queue are marked for removal and forced to pay Q. (going to hell)
Players from K+1 onwards pay their strategy with probability p/1000.
Each player's time spent is increased by 1.
Players whose total payment has reached F or time spent has reached T are marked for removal. (going to heaven)
Players marked for removal are removed from the queue.
The Queue is sorted as per the quantity (total payment + c)/(time spent) for each player. (c=T/10)
For each player the change of position over the last 10 iterations is considered. If the rate of this change indicates that the player goes to hell then her strategy is increased by 1 otherwise it is decreased by 1.
A random number of new players enter the queue (Gaussian with mean 100 and std 15). Again each new player has the same properties as the players added at the beginning of the game.

    
simulation.py runs 10000 iterations of the above procedure.

Outputs Total Money collected, Average money collected, Average no of sinners going to hell.

Also output graphs: Length of queue, payment of heaven bound sinners, stats of heaven bound sinners, stats of hell bound sinners, total money collected, proportional distribution of strategy among sinners.
