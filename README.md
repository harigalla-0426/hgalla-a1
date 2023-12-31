# a1-release

## Part 1

1i) This task was designed and implemented by Rohan and Hari.

- state space: The 'fringe' is prioritized by g(s) + h(s) where g is the cost function and h is the heuristic function. Each element in the fringe holds the state, path, and priority value.
- successor function: For every bird, there is a successor for each swap with its immediate neighbors (excluding duplicates).
- cost function: A constant is added (e.g. +1) for every move.
- the goal state: A list with values from 1-5 in order.
- heuristic function: This is just the sum of distances of the birds from their goal positions.

1ii) First, the algorithm puts the initial state into the fringe. While the fringe is not empty, a state is popped from the fringe and, if it is not the goal state, it is placed into the visited list. Then, all of the current state's successors are added to the fringe and sorted by priority (g(s) + h(s)).

1iii) Given the simplicity of this problem, it was not necessary to implement a visited array or removal of states from the fringe to make h(s) consistent. We also omitted starting over when no solution is found quickly enough.

## Part 2

2i) This task was implemented by Rohan and Hari, then Pete added 7.5 hours of effort to debug the heuristic not working for board2. Finally, the solutions was designed by Rohan and Hari by taking the manhattan distance in all 4 directioins as heuristic and choosing the least distance among them. For this, we have also taken into consideration the positions which can be reached through rotation - difference of 5 units multiples.

- state space: The 'fringe' is prioritized by g(s) + h(s) where g is the cost function and h is the heuristic function.
- successor function: For every board state, there are 24 possible moves which are returned as possible moves: U1-U5, R1-R5, L1-L5, D1-D5, Oc, Occ, Ic, and Icc.
- cost function: A constant is added (e.g. +1) for every move.
- the goal state: A board with values from 1-25 in order.
- heuristic function: Manhattan distance is the main heuristic, however, for each board element we caculate distance to the target in all 4 possible directions taking the rotations also into consideration.

2ii) First, the algorithm puts the initial_board into the fringe after checking if it is a goal state. While the fringe is not empty, a board is popped from the fringe and placed into the visited list. Then, all of the current state's successors are added to the fringe and sorted by priority (g(s) + h(s)). Each element in the fringe holds the board state, a list of moves made (e.g. ['U1','Oc']), and the priority value.

## Part 3

3i) This task was designed and implemented entirely by Pete.

- state space: The 'fringe' is prioritized by g(s) + h(s) where g is the cost function and h is the heuristic function. A 'visited' list is maintained to track the names of all cities popped from the fringe.
- successor function: The entire route dataset is loaded into a graph/dictionary at the start of the algorithm. It is an adjacency-list style graph, so one can get the list of Edge objects (which hold destination city names, road lengths, and highway names) from a city name.
  The entire graph is loaded in at the start of the algorithm, so the successors are just retrieved from the graph/dictionary.
- cost function: Implemented as a simple if-else statement based on what the assignment asks for.
- the goal state: The destination city name
- heuristic function: This is the Haversine distance between the lat/lng coordinates of two cities converted into miles and stored in estimatedDistance. If the source or destination is a road (i.e. not in the dataset), the distance is assumed to be 0.

3ii) First, both data files are loaded into dictionaries for easy access. A larger dataset might require database lookup. Then, the algorithm puts the start city into the fringe and gets its neighbors. From there, the algorithm continues to insert neighboring cities into the fringe until the goal city is found. The fringe is a priority queue that sorts based on cost + heuristic, and it does not allow insertion of successors that have already been visited.
As the algorithm collects successors, it also stores them and the source city into a 'parentMap' dictionary which is read into a list once the goal is found. That list is reversed so that the time, est. delivery time, length, and route can be returned.

3iii) There is no implementation of a "consistent" heuristic to remove successors already in the fringe. I tested my algorithm with a few distant cities (from Arizona to Kentucky or from Indiana to Michigan) and compared the results with Google Maps.
