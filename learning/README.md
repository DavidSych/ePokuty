# Learning Algorithm Description

Each finds an approximate solution to the Purgatory game, which models ordered queue of agents awaiting some punishment. In each step of the game, agents are given information about where in queue they are. Based on this information, the agent chooses a quantity of money to pay to some authority. However, with some probability which may differ between agents, they instead forget and pay nothing. Afterwards, the agents are ordered according to their average payment, i.e. the total amount they paid divided by total number of steps they spent in the queue. Agents who paid in total at least some publicly known quantity 'F', or spent at least 'T' steps in the queue are removed from the game. Among the rest, first 'k' with lowest average payment are selected and forced to pay F, plus a some additional fine penalty. Finally, a random number drawn from normal distributon with mean 'x_mean' and deviation 'x_sigma' of new agents are added at the end of the queue and the cycle repeats.

The 'main.py' script computes approximate best strategy in the Purgatory game. 
We use the PPO algorithm over 'train_sims' iterations, each using 'buffer_len' samples. 
Increasing the number of samples increases stability and computational time.
Optionally, the exploitability (NashConv) is computed if 'evaluate' is set to 'True'.

Different probability distributions from which the probability of ignorance is sampled can be selected using 'ignorance_distribution'.
Various parameters influencing the deep learning model can be set by user, which may have a significant efect on the training.

One of the outputs of the script is the percentage of agents leaving the queue after a given number of steps and total payment for each training iteration. 
Second output is the average payment of agents above the necessery minimum k * F each step for every training iteration.

Required packages: numpy > 1.23, tensorflow > 2.11, tensorflow-probability > 0.18, matplotlib > 3.6
