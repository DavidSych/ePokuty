# purgatorybsr



Run simulation.py

Input: Number of players to start with:
    F (payment that allows a player to go to heaven):
    Q (fine imposed on hell-bound players):
    K (first K players go to hell):
   T (players that survive T iterations go to heaven):
    integer p between 0 and 999 (each player forgets to play with probability p/1000):
    
Runs 10000 iterations of purgatory game with basic rational strategy i.e., at every iteration a player's strategy is increased/decreased by 1 by a trend over previous 10 iterations.

Outputs Total Money collected, Average money collected, Average no of sinners going to hell.

Also output graphs: Length of queue, payment of heaven bound sinners, stats of heaven bound sinners, stats of hell bound sinners, total money collected, proportional distribution of strategy among sinners
