# Visualization of the A* Pathfinding Algorithm using Pygame

One of the main things computer scientists do is develop algorithms to make tasks more efficient and quick. It is extremely interesting to me to see how these algorithms work.

This program uses pygame to help visualize the A* Pathfinding Algorithm. Here it is some information about the algorithm.
- Nodes
    - Letter (A, B, C, D)
    - Anything in a graph that you can visit (ex: the nodes of a triangle would be the vertices, the edges would be the lines connecting them
    - Weighted Edge
        - It is a certain length, different from the others
- The Algorithm

    > Goal is to find the shortest path

    - Informed path, don't just brute force it
    - Only consider paths that algorithm deems optimal
    - Open Set - Keeps track of the nodes we want to look at next
        - Open = {(F score, node) }
        - After you select a node based on the open set, clear it then continue filling it out
    - F(n) = G(n) + H(n)
        - H(n) → H score gives us an estimate of the distance from the node 'n' and the end node
        - G(n) → G score gives us the current shortest distance from the start node to the node 'c' that we have already found
        - F score can help us prioritize nodes
            - Compare possible routes by taking the F score of the nodes around ("it will take us this distance to get to this next node (G score) and then this distance to get to the end (H score)")
