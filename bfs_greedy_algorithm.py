# BFS random item placement algorithm
import random
from game import Game

# Randomization mapping
def generate_item_placement(game: Game, resources: set[str]) -> bool:
    available_resources = set(resources)

    # Compute the initial reachable nodes and inventory
    vreach = game.compute_reachable(inventory=set())
    inventory = game.collect_items_from(vreach)
    vreach = game.compute_reachable(inventory)

    print(f"{"---" * 5} BFS-Greedy Algorithm {"---" * 5}")
    print(f"Initial Vreach: {sorted(vreach)}")
    print(f"Initial inventory: {sorted(inventory)}")

    # |v| * |e|
    max_iterations = len(game.nodes) * len(game.edges) * 5
    for iteration in range(max_iterations):
        if game.end in vreach:
            print(f"\nEnd node '{game.end}' is reachable, game is finishable")
            return True

        # Find essential items
        essential = game.find_essential_items(vreach, inventory)
        if not essential:
            print(f"\nNo essential items found but end node unreachable")
            return False

        # Filter to items available in R
        placeable_essential = essential & available_resources
        if not placeable_essential:
            print(f"\nEssential items {essential} are not in remaining resources")
            return False

        # Randomly select essential item and reachable empty node to map to
        chosen_item = random.choice(sorted(placeable_essential))
        empty_reachable = [n for n in vreach if game.node_item[n] is None]

        if not empty_reachable:
            print(f"\nNo empty reachable nodes to place '{chosen_item}'")
            return False

        chosen_node = random.choice(empty_reachable)
        # Place item and remove from available resources
        game.place_item(chosen_node, chosen_item)
        available_resources.discard(chosen_item)

        print(f"\nIteration {iteration + 1}: Placed '{chosen_item}' in node '{chosen_node}'")

        # Update Vreach and inventory after placement
        inventory = game.collect_items_from(vreach)
        vreach = game.compute_reachable(inventory)

        print(f"Updated Vreach: {sorted(vreach)}")
        print(f"Updated inventory: {sorted(inventory)}")

    print(f"\nCould not place all required items.")
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