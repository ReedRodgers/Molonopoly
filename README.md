# Molonopoly
Plan of Action: We’re going to incrementally build monopoly, in 3 different stages:

Stage 1: A single player game, with a smaller board, with fewer colours. It would look something like this:
 

We would have a single player, and make them move along the board. The following simplifications are made:
•	No money is earned; the player starts with enough money to buy 5 properties.
•	All properties have fixed equal value, regardless of colour.
•	The neural network will be presented with different attainable combinations of cash and properties, and asked to evaluate the value of said combination. 
•	The NN’s evaluation will be based on a heuristic which accounts for the ‘realizable’ rent value of the property.
•	After initial training, the NN will be run twice with the current and future state to make purchasing decisions.

We will have a neural net that takes as input the property ownership matrix, and the amount of cash owned by the player. It will output a binary number indicating whether or not to buy the property. 

The goal for this stage is to have the NN learn the effect of having multiple properties of the same colour.

Stage 2: One regular player, one pseudo-player

For this stage, we will change the rules a bit:
•	There is one regular player, and one pseudo-player (“The Bank”)
o	The Bank is a pseudo-player because they don’t make any moves.
•	There are a fixed number of turns
•	Properties have realistic values.
•	The real player starts with a fixed amount of cash
•	The player earns money if they land on their own property. 
•	The player can buy properties it lands on, but if they land on a property and decide to not buy it (or if they don’t own it), they will have to pay a small fee to the bank. 
o	The small fee is to encourage long term decision making

The purpose of the pseudo-player is to model the effects of a second player:
•	Model the effects of incoming cash flow due to rent, versus outgoing cash flow due to others’ owning property.
•	Add time constraints

Stage 3: Two regular players

For this stage, we would:
•	Have a full monopoly board.
•	Have two full players, each using the model trained in Stage 2.
•	Regular monopoly rules:
o	You don’t get money for landing on your own property.
o	You get money when your opponent lands on your property, and vice-versa.
o	There will be neutral squares, for when that property is unowned. 
•	NO negotiation/trade models yet

Stage 4:  Negotiation
•	If we have time, we will train a model for this using heuristics to cause semi-supervised learning.
