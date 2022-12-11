The program adds n players to the queue. Each player added has the following properties:
+ player remembers payment history
+ player has a strategy which decides what to pay in next iteration (in any iteraton player's payment increases by stratregy).
+ player knows her total payment.
+ player knows time spent in queue (initialised at t=0)
+ player knows her position in the queue
+ with probability (1-p) he has paid 1 and has strategy of paying 1 on entering the queue.

Each iteration runs as follows:
+ First K players in the queue are marked for removal and forced to pay Q. (going to hell)
+ Players from K+1 onwards pay their strategy with probability (1-p).
+ Each player's time spent is increased by 1.
+ Players whose total payment has reached F or time spent has reached T are marked for removal. (going to heaven)
+ Players marked for removal are removed from the queue.
+ The Queue is sorted as per the quantity (total payment + c)/(time spent) for each player. (c=T/10)
+ For each player the change of position over the last 10 iterations is considered. If the rate of this change indicates that the player goes to hell then her strategy is increased by 1 otherwise it is decreased by 1.
+ A random number of new players enter the queue. Again each new player has the same properties as the players added at the beginning of the game.


Run simulation.py --args

args:

+ --seed:  default=42, type=int, help="Seed for random sampling"
+ --n:  default=1000, type=int, help="Length of queue at the beginning of the game"
+ --F:  default=50, type=int, help="Fine to pay for going to heaven."
+ --Q:  default=0, type=int, help="Additional penalty for going to hell."
+ --T:  default=100, type=int, help="Time to survive in queue for going to heaven."
+ --K:  default=5, type=int, help="How many people go to hell in each time step."
+ --x_mean:  default=100, type=float, help="Mean number of people entering the queue at each time step."
+ --x_std:  default=15, type=float, help="Standard deviation of the number of people entering the queue at each time step."
+ --ignorance_distribution:  default=1, type=int, help="Distribution to use to sample probability of ignorance for each player. Supported: 1 (uniform), 2 (fixed), 3 (beta)."
+ --prob:  default=0.7, type=float, help="Probability of ignorance, if fixed."
+ --p_min:  default=0.7, type=float, help="Minimum probability of ignorance, if uniform."
+ --a:  default=7, type=float, help="Shape parameter of Beta(a,b) distribution for sampling probability ignorance."
+ --b:  default=3, type=float, help="Shape parameter of Beta(a,b) distribution for sampling probability of ignorance."
+ --total_time:  default=10000, type=int, help="How many time steps to run"

Outputs Total Money collected, Average money collected, Average no of sinners going to hell.

Also output graphs: Length of queue, payment of heaven bound sinners, stats of heaven bound sinners, stats of hell bound sinners, total money collected, proportional distribution of strategy among players.


Requirements: python3.7, matplotlib>=3.0.2, numpy>=1.16.2, pandas>=0.23.3+dfsg
