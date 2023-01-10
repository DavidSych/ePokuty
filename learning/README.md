# Learning Algorithm Description

The 'main.py' script computes approximate best strategy in the Purgatory game. 
We use the PPO algorithm over 'train_sims' iterations, each using 'buffer_len' samples. 
Increasing the number of samples increases stability and computational time.
Optionally, the exploitability (NashConv) is computed if 'evaluate' is set to 'True'.

Different probability distributions from which the probability of ignorance is sampled can be selected using 'ignorance_distribution'.
Various parameters influencing the deep learning model can be set by user, which may have a significant efect on the training.

One of the outputs of the script is the percentage of agents leaving the queue after a given number of steps and total payment for each training iteration. 
Second output is the average payment of agents above the necessery minimum k * F each step for every training iteration.

Required packages: numpy > 1.23, tensorflow > 2.11, tensorflow-probability > 0.18, matplotlib > 3.6

## Usage 

Run simulation.py --args

args:

+ --seed:  default=42, type=int, help="Seed for random sampling"
+ --n:  default=1000, type=int, help="Length of queue at the beginning of the game"
+ --F:  default=50, type=int, help="Fine to pay for going to heaven."
+ --fined_penalty:  default=0, type=int, help="Additional penalty for going to hell."
+ --T:  default=100, type=int, help="Time to survive in queue for going to heaven."
+ --K:  default=5, type=int, help="How many people go to hell in each time step."
+ --x_mean:  default=100, type=float, help="Mean number of people entering the queue at each time step."
+ --x_std:  default=15, type=float, help="Standard deviation of the number of people entering the queue at each time step."
+ --ignorance_distribution:  default='uniform', type=str, help="What distribuin to use to sample probability of ignorance. Supported: fixed, uniform, beta."
+ --p:  default=0.7, type=float, help="Probability of ignorance, if fixed."
+ --p_min:  default=0.7, type=float, help="Minimum probability of ignorance, if uniform."
+ --a:  default=7, type=float, help="Shape parameter of Beta(a,b) distribution for sampling probability ignorance."
+ --b:  default=3, type=float, help="Shape parameter of Beta(a,b) distribution for sampling probability of ignorance."

Outputs Total Money collected, Average money collected, Average no of sinners going to hell.

Also output graphs: Length of queue, payment of heaven bound sinners, stats of heaven bound sinners, stats of hell bound sinners, total money collected, proportional distribution of strategy among players.


Requirements: python > 3.6, numpy > 1.23, tensorflow > 2.11, tensorflow-probability > 0.18, matplotlib > 3.6

