# ePokuty

In this work, we design a game mechanism to help collecting traffic
fines.
In large cities, there is a huge number of traffic violations, highly
exceeding the capacity of state employees assigned to manage the fines.

Next, we include a short description of our work with links to the
enclosed files.

1. Our work starts with the analysis of the database of traffic
violations in Prague in three consecutive years. The database was
provided for us by the city of Prague and thus we did not need to do the
anonymization by ourselves. That is why the original software product
`TL05000450-V14 software Anonymizátor vybrané databáze` was replaced by
the analysis of this database. We enclose the analysis as a separate file.

The conclusion of our analysis is very clear:

The assigned state employees should primarily concentrate on serious
violations and frequent violators. However, a huge number of minor
non-repetative violations are still to be settled which makes the prime
task of the assigned employees impossibly harder. Practically, fines for
minor non-repetative offenses can be enforced in a small fraction of
cases, this information becomes a common knowledge and the traffic, law
and order suffers.

A common sense strategy is to try finding mechanisms to free the
precious well-qualified state employees of the burden of administering
fines for minor non-repetative offenses.

We suggest such a mechanism. We call it Purgatory game. The definition of Purgatory game is included in each of the provided ziped directories.

We consider sequences S(t), t= 0, 1, ... w (w is a sufficiently large
number) where each S(t) is a sequence of players (sinners)  and it is
obtained from S(t-1) by a process described in detail in the definition of Purgatory. 
A critical part of this process is that at each step t, an
initial segment of the current sequence of sinners is admitted to hell.
The sinners may avoid hell by paying, and by staying long enough in the
sequence.



The length of the "sequence of sinners" may be much larger comparing to
the number of poor souls admitted to the hell in each step. The most
rational strategy for the sinners is to cooperate. If they share the
fines of the few who get to hell, the payment of each is negligible.
Hence, the design of Purgatory explores non-cooperation for the
benefit of the designer.

We use the Purgatory game for modelling two mechanisms for improving
collection of fines. These mechanisms are analysed as next outputs of
the project.

2. The variant of Purgatory called 'One-Reminder' provides a mechanism
for making more people pay the assigned fine before starting
'spravni rizeni'. This variant can be analysed without numerical
experiments. The findings are included as as separate file.

The general Purgatory Game is modelling the mechanism described below
which we call Fines-Charity. This is our suggestion for resolving long
queues of violations where 'spravni rizeni' has been initiated. These
long queues effectively mean that a majority of such violations are not
processed in time.

We suggest that the magistrates
a. Implements One-Reminder immediately since it clearly agrees with the
current legislation
b. Makes a pilot implementation of Fines-Charity: here the view of legal
experts is divided as to whether such mechanism complies with the
current legislation.
