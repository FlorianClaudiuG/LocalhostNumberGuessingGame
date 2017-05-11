# LocalhostNumberGuessingGame
Year 2 Networks and Security assignment. We were tasked with creating a server, a client and an admin client for a number guessing game.

Everything related to the game is done server-side. 

The clients, in this version of the game, connect to the same computer via localhost,although it can be expanded for external internet 
connections as well. After a series of handshakes (that were part of the assignment spec), the game is run for each client on a separate 
thread. 

The admin client uses a separate port when connecting. It is able to request the list of current players on the server.

A flowchart detailing the process was also part of the submission.
