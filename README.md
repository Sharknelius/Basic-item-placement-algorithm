Programmed using Python 3.12.8.

The randomizer algorithms to place items in a game are bruteforce_algorithm.py and bfs_greedy_algorithm.py. Edit the create_game1() or create_game2() functions in the respective files to change the example game graphs and resources.
- Edit "game = Game(start='A', end='E')" with the names of the nodes you wish to start and end the traversal.
- To add named nodes, edit "for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            game.add_node(node)"
- Edit "resources = {'key', 'torch'}" to change the resources that can be placed during game generation. Note that resources are reusable.
- To create an edge, edit/add "game.add_edge('A', 'B')" where 'A' can be replaced with the name of the "from" node, and 'B' can be replaced with the name of the "to" node.
- You can also add a parameter to the add_edge() function to specify what resource is required to use that edge. Example: "game.add_edge('A', 'B', requires='key')"

Make sure all three .py files are in the same directory. Run the algorithm files to test it with the specified approach. The output will be printed to the console.
