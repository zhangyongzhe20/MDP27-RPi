# MDP27-RPi
 The repo serves the development of RPi.
 
 ## Message Flows:
 ###  Exploration leaderboard & Image Recognition:
 * Arduino -> Robots: Explorating path
 * Arduino -> PC: Mapping of the maze; Arduino -> PRi: trigger camera; PRi -> PC: label result
 * PC-> PRi -> Android: Map info(include label result)
 ### Fatest path leaderboard:
 * Android -> PC: waypoint coordinates
 * PC-> Arduino: fatest path
### Functional checklist:
* Android -> Arduino: basic commands

 ## Software Requirements:
 * `python`: 2.7

## References:
* Multithreading in python [Link](https://github.com/HarveyLeo/cz3004-mdp-grp2/tree/master/Raspberry%20Pi)
* Header Flags of different types of messages [Link](https://github.com/rohitsm/ntu.sce.mdp.2)
* Image Recognition(rank number 4) [Link](https://github.com/jiachin1995/CZ3004)

