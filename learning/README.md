Learning Algorithm Description

The 'main.py' script computes approximate best strategy in the Purgatory game. 
We use the PPO algorithm over 'train_sims' iterations, each using 'buffer_len' samples. 
Increasing the number of samples increases stability and computational time.
Optionally, the exploitability (NashConv) is computed if 'evaluate' is set to 'True'.

Different probability distributions from which the probability of ignorance is sampled can be selected using 'ignorance_distribution'.
Various parameters influencing the deep learning model can be set by user, which may have a significant efect on the training.

One of the outputs of the script is the percentage of agents leaving the queue after a given number of steps and total payment for each training iteration. 
Second output is the average payment of agents above the necessery minimum k * F each step for every training iteration.

Required packages: numpy > 1.23, tensorflow > 2.11, tensorflow-probability > 0.18, matplotlib > 3.6
