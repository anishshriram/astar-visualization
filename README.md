# Visualization of the A* Pathfinding Algorithm using Pygame

One of the main things computer scientists do is develop algorithms to make tasks more efficient and quick. It is extremely interesting to me to see how these algorithms work.

This program uses pygame to help visualize the A* Pathfinding Algorithm. The algorithm goes through series of nodes, comparing their calculated scores, and based on that finding the shortest path to the end node. Here it is some information to help understand that.
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

I also used a couple Python packages and libraries. Pygame (a computer graphics and sound library), and Priority Queue, which helps sort the open set for me.

Outline of the Project

1. created a class, Node, to set up the attributes of each node in the board
2. created a series of functions to make and draw the grid, find the position of the mouse, etc
3. created a main function to check events that are happening during the visualization process (if mouse or keys are clicked, etc)
4. created the actual algorithm function, explained above.

As allways, all functions and code was commented thoroughly for ease of understanding

Resources Used:
- Priority Queue Intro: https://www.geeksforgeeks.org/priority-queue-set-1-introduction/
- A* Algorithm Explanation: https://www.youtube.com/watch?v=-L-WgKMFuhE
Next one really really important. Tech With Tim helped with a lot of the issues I came accross while writing this, tried to keep it as original as possible. But the visualization part credit largely goes to him / his tutorial because I have little experience with pygame
- Visualization Tutorial (for pygame): https://www.youtube.com/watch?v=JtiK0DOeI4A

Goals/What I plan to do with this:

I think I can create some sort of mapping app with this algo, should be a good project.
