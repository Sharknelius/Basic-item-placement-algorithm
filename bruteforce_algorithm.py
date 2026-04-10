# Brute-force random item placement algorithm
import random
from game import Game

# Randomization mapping
def generate_item_placement(game: Game, resources: set[str]) -> bool:
    print(f"{"---" * 5} Brute-force Algorithm {"---" * 5}")

    # n^r * (n + m)
    max_iterations = len(game.nodes) ** len(resources) * (len(game.nodes) + len(game.edges))
    for iteration in range(max_iterations):
        # Generate a whole new random placement each iteration
        for node in game.nodes:
            game.node_item[node] = None # Clear all placements

        # Randomly map resources to nodes
        rand_nodes = random.sample(sorted(game.nodes), len(resources)) # Get random nodes
        for item, node in zip(resources, rand_nodes):
                print(f"Placing item {item} in node {node}")
                game.place_item(node, item)
        
        # Reset inventory and Vreach after placement
        inventory = set()
        vreach = game.compute_reachable(inventory)
        # Collect items
        inventory = game.collect_items_from(vreach)
        vreach = game.compute_reachable(inventory)

        print(f"\nIteration {iteration+1}\nVreach={sorted(vreach)}\ninventory={sorted(inventory)}")

        if game.end in vreach:
            print(f"\nEnd node '{game.end}' is reachable, game is finishable")
            return True
        print("Game is not finishable with these placements, trying again...\n")

    print(f"\nCould not place all required items or game cannot be solved.")
    return False

# Update these values to test different game structures and resource sets
def create_game1() -> tuple[Game, set[str]]:
    game = Game(start='A', end='E')

    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        game.add_node(node)

    resources = {'key', 'torch'}

    game.add_edge('A', 'B')
    game.add_edge('B', 'C', requires='key')   # Need 'key' to go B -> C
    game.add_edge('A', 'F')
    game.add_edge('F', 'A')
    game.add_edge('F', 'G', requires='key') # Need 'key' to go F -> G
    game.add_edge('G', 'C')
    game.add_edge('C', 'D')
    game.add_edge('D', 'E', requires='torch') # Need 'torch' to go D -> E

    return game, resources

# Update these values to test different game structures and resource sets
def create_game2() -> tuple[Game, set[str]]:
    game = Game(start='A', end='F')

    for node in ['A', 'B', 'C', 'D', 'E', 'F']:
        game.add_node(node)

    resources = {'key', 'rope'}

    game.add_edge('A', 'B')
    game.add_edge('B', 'C', requires='key')
    game.add_edge('C', 'A')
    game.add_edge('C', 'B')
    game.add_edge('D', 'A')
    game.add_edge('D', 'F', requires='rope')

    return game, resources

if __name__ == '__main__':
    game, resources = create_game1()
    print(f"{"---" * 5} Initial Game Structure {"---" * 5}")
    print(game)
    print(f"\nResource set R: {sorted(resources)}")

    success = generate_item_placement(game, resources)

    print(f"\n{"---" * 5} Final Game State {"---" * 5}")
    print(game)
    print(f"\nFinishable: {success}")