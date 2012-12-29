sandpile-game
=============
This is a small toy project to simulate the sandpile game, sometimes known as the chip-firing game. It's generally studed for its interesting mathematical properties, but this is a game version instead.

Rules:
Two players, can play on any graph.
On each turn, that player adds a grain of sand to any node. This gives ownership of that node to that player.
  If (# grains on that node) >= (degree of that node), that node becomes unstable and "fires", sending 1 grain to each of its neighbors.
  This can trigger a chain reaction if a neighbor becomes unstable. In certain configurations, this can create an infinite loop; still deciding on best way to deal with it.
The number of points a player has is the total number of sand grains on nodes that player controls.
The first one to reach some score wins (currently undetermined).

So far, only the underlying game state has been made. No graphic interface as of yet.
