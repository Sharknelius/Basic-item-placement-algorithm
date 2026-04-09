# Basic Game creation and item placement algorithm

import random
from collections import deque

"""
    A directed graph where:
    - Each node can hold at most one item from resource set R
    - Each edge may require an item to traverse
    - The player collects items from visited nodes and uses them to unlock new edges
"""
class Game:
    def __init__(self, start: str, end: str):
        # start and end nodes
        self.start = start
        self.end = end
        self.nodes: set[str] = set()           # All nodes in the graph
        self.edges: dict[str, list[str]] = {}  # node -> list of successor nodes
        self.edge_req: dict[tuple, str] = {}  # (from, to) -> required item
        self.node_item: dict[str, str | None] = {}    # node -> item located there

    def add_node(self, name: str):
        self.nodes.add(name) # Lettered name
        self.node_item[name] = None # Empty by default

    def add_edge(self, from_node: str, to_node: str, requires: str | None = None):
        # If from node is not in the graph, add it
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
        # Optionally requires an item to traverse
        if requires is not None:
            self.edge_req[(from_node, to_node)] = requires

    def place_item(self, node: str, item: str):
        if node not in self.nodes: # Node should be in graph
            raise ValueError(f"Cannot place item, node {node} doesn't exist.")
        self.node_item[node] = item

    def get_traversable_edges(self, inventory: set[str]) -> list[tuple]:
        # Given the player's inventory
        # Return list of traversable edges
        traversable = []
        for from_node, neighbors in self.edges.items():
            for to_node in neighbors:
                required = self.edge_req.get((from_node, to_node))
                if required is None or required in inventory:
                    traversable.append((from_node, to_node)) # Edge is traversable

        return traversable

    def compute_reachable(self, inventory: set[str]) -> set[str]:
        # Find traversable edges based on current inventory
        traversable = set(self.get_traversable_edges(inventory))
        reachable = set()
        # Queue of nodes to explore
        # Start with the initial node
        queue = deque([self.start])
        # Explore (BFS) until no more nodes can be reached
        while queue:
            node = queue.popleft() # Get next node to explore

            if node in reachable: # Skip if already visited
                continue

            reachable.add(node)

            for neighbor in self.edges.get(node, []): # Get all neighbors of the current node
                if (node, neighbor) in traversable and neighbor not in reachable:
                    queue.append(neighbor)

        return reachable

    def collect_items_from(self, nodes: set[str]) -> set[str]:
        # Return set of items from all given nodes
        return {self.node_item[n] for n in nodes if self.node_item[n] is not None}

    def find_essential_items(self, vreach: set[str], inventory: set[str]) -> set[str]:
        # Find required set of items for edges where u is in Vreach and v is not, and filter to those not already in inventory
        essential = set()
        for node in vreach: # node u
            for neighbor in self.edges.get(node, []):
                if neighbor not in vreach: # node v
                    required = self.edge_req.get((node, neighbor))
                    if required is not None and required not in inventory:
                        essential.add(required)
        return essential

    def __str__(self):
        lines = [f"Game(start={self.start}, end={self.end})"]
        lines.append("Nodes:")
        for n in sorted(self.nodes):
            item = self.node_item.get(n)
            lines.append(f"  {n}: item={item}")
        lines.append("Edges:")
        for from_node, neighbors in self.edges.items():
            for to_node in neighbors:
                req = self.edge_req.get((from_node, to_node))
                req_str = f" [requires: {req}]" if req else ""
                lines.append(f"  {from_node} -> {to_node}{req_str}")
        return "\n".join(lines)

# Randomization mapping
def generate_item_placement(game: Game, resources: set[str], seed: int | None = None) -> bool:
    if seed is not None:
        random.seed(seed)

    available_resources = set(resources)

    # Step 1: Start
    vreach = game.compute_reachable(inventory=set())
    inventory = game.collect_items_from(vreach)
    vreach = game.compute_reachable(inventory)

    print(f"\n{"---" * 10} Basic algorithm {"---" * 10}")
    print(f"Initial Vreach: {sorted(vreach)}")
    print(f"Initial inventory: {sorted(inventory)}")

    # (n + m) * r
    max_iterations = len(game.nodes) + len(game.edges) * len(resources)
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
def create_game() -> tuple[Game, set[str]]:
    game = Game(start='A', end='E')

    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        game.add_node(node)

    resources = {'key', 'torch', 'key'}

    game.add_edge('A', 'B')
    game.add_edge('B', 'C', requires='key')   # Need 'key' to go B -> C
    game.add_edge('A', 'F')
    game.add_edge('F', 'G', requires='key') # Need 'key' to go F -> G
    game.add_edge('G', 'C')
    game.add_edge('C', 'D')
    game.add_edge('D', 'E', requires='torch') # Need 'torch' to go D -> E

    return game, resources

if __name__ == '__main__':
    game, resources = create_game()
    print(f"{"---" * 5} Initial Game Structure {"---" * 5}")
    print(game)
    print(f"\nResource set R: {sorted(resources)}")

    success = generate_item_placement(game, resources, seed=42)

    print(f"\n{"---" * 5} Final Game State {"---" * 5}")
    print(game)
    print(f"\nFinishable: {success}")