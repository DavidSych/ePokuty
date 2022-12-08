# ePokuty

Includes two main parts described in more detain in their respective folders
- basic rational strategy: agents use predefined atrategy and the result is observed
- learning: agents learn approximate best strategy against others

Each finds an approximate solution to the Purgatory game, which models ordered queue of agents awaiting some punishment.
In each step of the game, agents are given information about where in queue they are. 
Based on this information, the agent chooses a quantity of money to pay to some authority. 
However, with some probability which may differ between agents, they instead forget and pay nothing.
Afterwards, the agents are ordered according to their average payment, i.e. the total amount they paid divided by total number of steps they spent in the queue.
Agents who paid on total at least some publicly known quantity 'F', or spent at least 'T' steps in the queue are removed from the game. 
Amont the rest, first 'k' with lowest average payment are selected and forced to pay F, plus a some additional fine penalty.
Finally, a random number drawn from normal distributon with mean 'x_mean' and deviation 'x_sigma' of new agents are added at the end of the queue and the cycle repeats.

# Notes

- grant number
- authors
- affiliation
- copyright/licence (special file)

BRS
- description first, run instructions later
- don't save csv output
- put png files and other output in separate folder and gitignore it
- what python, libraries are required

Learning
- python version


