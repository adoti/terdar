# terdar

terdar is a manual trade placer, manager, and log.  

at the core of terdar is the Kelly Criterion, a formula that states that the size of a bet in relation to a bettor's bankroll should be equal to their edge divided by the odds.  the Kelly Criterion, well known by bettors of all types, has been proven as the most efficient way to grow a bankroll.  

generally, the formula implies that a bet should not be taken if the bettor has no edge over the paid odds.  as terdar makes no attempts to delve into AI/ML or any sort of quant trading algorithms in order to quantify an edge, the trader themselves is considered to provide the edge through their decision making.  although initial use of terdar assumes that the trader *does* have an edge, the continued use of terdar aims to quantify that edge as a function of the Risk:Reward ratio of any given trade, allowing the trader to better size their bets based on the R:R of that trade.

to illustrate using the most common Kelly example, assume a trader can win 60% of 1:1 Risk/Reward trades.  The Kelly Criterion would state that, under these assumptions, for any 1:1 trade, that bettor should risk 20% of their bankroll.  terdar would accurately size any bet using as much margin as necessary in order to risk 20% of the trader's bankroll for any given 1:1 RR trade, given the target and exit prices as provided by the trader.  terdar would then log that trade and its subsequent result, allowing for further refinement of the win percentage and the placement of even more accurate Kelly bets.

As with anything, the goal is to make the most money as fast and efficiently as possible.
