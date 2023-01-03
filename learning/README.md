# Definition

Our motivation has been to design a game mechanism to help collecting traffic fines.
In large cities, there is a huge number of traffic violations, highly exceeding the capacity of state employees assigned to manage the fines.

The assigned state employees should primarily concentrate on serious violations and frequent violators. However, a huge number of minor violations are still to be settled which makes their prime task impossibly harder. Practically, fines for minor offenses are enforced in a small fraction of cases, this sweet information becomes a common knowledge and the traffic, law and order suffers.

A common sense strategy is to try finding mechanisms to free the precious well-qualified state employees of the burden of fines for minor offenses. The purgatory game is our attempt to define and analyse such a mechanism.


The purgatory has been extensively modelled by various artistic or philosophical means. Here is an attempt to a mathematical model. We consider sequences $S(t), t= 0, 1, \ldots, w$ (
$w$ is a sufficiently large number reflecting the end of our universe) where each $S(t)$ is a sequence of players (sinners)  and it is obtained from $S(t-1)$ by a process described below. 

The length of the "sequence of sinners" may be much larger comparing to the number of poor souls admitted to the hell in each step. The most rational strategy for the sinners is to cooperate. If they share the fines of the few who get to hell, the payment of each is negligible. Hence, the design of Purgatory *explores non-cooperation for the benefit of the designer*. 

It is natural to seek a measurement which would
indicate how well Purgatory explores non-cooperation. We call this an *avelanche effect*.

## Basic Notation

We let $X$ be the set of all players appearing in the game. Each element of each $S(t)$ belongs to $X$.
For $t= 0, 1, \ldots, w$ we denote by $n(t)$ the length of $S(t)$ and let 
$S(t)= (s(t,i))_{i=1}^{n(t)}$. We introduce, for each player $r\in X$, a pair of numbers $(r_1,r_2)$ so that player $r$ appears first in sequence $S(r_1)$, and in  $S(r_1)$, $r$ is in position $r_2$, i.e., $r= s(r_1, r_2)$. Let $r_3$ be the smallest integer bigger than $r_1$ such that $r$ is not in $S(r_3)$.
We will have non-negative integers $P(r,t), t\geq 0$ associated with each player $r$. For $t> r_1$, $P(r,t)$ represents the penance of player $r$ in the $t$-th sequence $S(t)$. These numbers are initially zero for each $r$ and are dynamically updated during the game. 

## Definition of Purgatory

*Input* consists of 
- the set $X$ of players,
- positive integer constants $w,T,K,c$, 
- initial *empty* sequence $S(0)$ of players,
- Integer function $F: X\rightarrow N$ representing the fine, i.e., the hellish numerical representation of the r-th sin,
- Integer function $Q: N\rightarrow N$ on $X$ representing the cost of paying the fine,
typically $Q(F)= F+const$,
- probabilities $p(r)$, for $r\in X$, 
- positive integer constants $x(t), t=1, \ldots, w$.

We let *P(r,t)= 0* for $t= 0, \ldots, r_1$.
The game consists of $w$ steps. *In each step, each player receives its position in the current sequence.*

In $(t+1)$-step (
$t= 0, \ldots, w-1$
), sequence $S(t+1)$ is constructed from sequence $S(t)$ and numbers $P(r,t+1), r\in X$ are obtained as follows:
- With probability $1-p(r)$, each player $r= s(t,i)$ of $S(t)$ acts as follows:  it chooses a non-negative integer, denoted by $q(t,i)$, and let $P(r,t+1):= P(r,t)+ q(t,i)$. With probability $p(r)$, player $r$ does nothing.
- If $P(r,t+1)\geq F(r)$ then we delete player $r$ since $r$ repented enough and assents to the heaven,
- We rearrange the updated $S(t)$ by the *stable sort* according to either (1) the numbers $P(r,t+1)$ or (2) the fractions $P(r,t+1)+c/(t-r_1+1)$,
- The first $K$ players of the current sequence go to the hell, 
- We add $x(t+1)$ new players to the end of the current sequence in an arbitrary order,
- If player $r$ stays long enough in the Purgatory, i.e., if $t+1-r_1\geq T$ then $r$ is deleted from the current sequence and assents to the heaven,
- We let $S(t+1)$ be the resulting sequence.
- A *pure (mixed respectively) strategy* with parameter $I$ is a collection $P_I= (P(r), r\in X)$ where $I$ is an input of Purgatory and each $P(r)$ is the pure (mixed respectively) strategy of player $r\in X$ in the Purgatory with the input $I$. A *pure strategy* of a player $r$ is defined as $P(r)= (P(r,0), \ldots, P(r,w))$. A *mixed strategy* of a player $r$ is defined as $P'(r)= (P'(r,0), \ldots, P'(r,w))$ where $P'(r,t)$ is a probability distribution on $\{0, \ldots, F(r)\}$.
- Given a pure strategy $P(r)$, its *payoff* $v(P(r))$ is calculated after the end of the universe, is non-positive and is defined as follows:  if $r$ got to hell then $v(P(r))= -P(r,r_3)-Q(F(r))$ , otherwise $v(P(r))= -P(r,r_3)$.

This finishes the definition of the Purgatory. The probabilities $p(r), r\in X$ are crucial parameters of the game. We call $p(r)$ the *probability of ignorance*.


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
