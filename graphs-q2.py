from queue import PriorityQueue
import networkx as nx

# Create a directed graph
sea_of_islands = nx.DiGraph()

# Add islands (nodes) with attributes
sea_of_islands.add_node("Aotearoa", population=5220000, resources={"kahelelani_shells": 0, "ʻuala": 60, "kalo": 70, "kukui_nuts": 50})
sea_of_islands.add_node("Hawaii", population=1430000, resources={"kahelelani_shells": 120, "ʻuala": 90, "kalo": 85, "kukui_nuts": 75})
sea_of_islands.add_node("Tahiti", population=191000, resources={"kahelelani_shells": 0, "ʻuala": 50, "kalo": 60, "kukui_nuts": 40})
sea_of_islands.add_node("Rapanui", population=7700, resources={"kahelelani_shells": 0, "ʻuala": 20, "kalo": 30, "kukui_nuts": 10})
sea_of_islands.add_node("Samoa", population=218000, resources={"kahelelani_shells": 0, "ʻuala": 80, "kalo": 90, "kukui_nuts": 60})

# Add directed routes (edges) with travel times
sea_of_islands.add_edge("Aotearoa", "Hawaii", travel_time=20)
sea_of_islands.add_edge("Aotearoa", "Tahiti", travel_time=18)
sea_of_islands.add_edge("Aotearoa", "Samoa", travel_time=12)

sea_of_islands.add_edge("Hawaii", "Tahiti", travel_time=10)
sea_of_islands.add_edge("Hawaii", "Samoa", travel_time=10)

sea_of_islands.add_edge("Tahiti", "Aotearoa", travel_time=18)
sea_of_islands.add_edge("Tahiti", "Hawaii", travel_time=10)
sea_of_islands.add_edge("Tahiti", "Rapanui", travel_time=18)
sea_of_islands.add_edge("Tahiti", "Samoa", travel_time=10)

sea_of_islands.add_edge("Rapanui", "Tahiti", travel_time=18)

sea_of_islands.add_edge("Samoa", "Aotearoa", travel_time=12)
sea_of_islands.add_edge("Samoa", "Hawaii", travel_time=10)
sea_of_islands.add_edge("Samoa", "Tahiti", travel_time=10)

print("Resource distribution BEFORE:")
for island in sea_of_islands.nodes(data=True):
    print(island)
print('\n')

# print("\nRoutes and travel times:")
# for route in sea_of_islands.edges(data=True):
#     print(route)

# feel free to use this graph to test out your functions
def distribute_resource(graph, source_island, resource, quantity, canoe_capacity):
    """
    Distributes a specified quantity of a resource from a source island to other islands in a graph.

    Parameters:
    graph (networkx.DiGraph): The directed graph representing the islands and routes between them.
    source_island (str): The starting island from which the resource distribution begins.
    resource (str): The type of resource to be distributed.
    quantity (float): The total quantity of the resource to be distributed.
    canoe_capacity (float): The maximum capacity of the canoe used for transporting the resource.

    Returns:
    None

    The function calculates the target resource level for each island based on its population and 
    distributes the resource from the source island to other islands using a priority queue to 
    ensure the shortest travel time. It updates the resource levels of the islands as it traverses 
    the graph.
    """
    # Calculate the total population to determine the even distribution amount
    total_population = sum(graph.nodes[island]['population'] for island in graph.nodes())
    target_per_capita_resource = quantity / total_population

    # Set target resource levels for each island based on population
    target_resource = {
        island: target_per_capita_resource * graph.nodes[island]['population']
        for island in graph.nodes()
    }
    
    # Priority queue for processing islands in order of shortest travel time
    queue = PriorityQueue()
    queue.put((0, source_island))  # (travel_time, island)
    
    # Track visited islands to avoid redundant processing
    visited = set()
    
    # Distribute resources as we traverse the graph
    while not queue.empty():
        current_time, current_island = queue.get()
        if current_island in visited:
            continue
        visited.add(current_island)
        
        # Calculate the amount needed to reach the target for the current island
        current_quantity = graph.nodes[current_island]['resources'].get(resource, 0)
        needed_quantity = target_resource[current_island] - current_quantity
        
        # Determine the transfer amount, considering canoe capacity and fractional loading
        if needed_quantity > 0:
            transfer_quantity = min(needed_quantity, canoe_capacity)
            graph.nodes[current_island]['resources'][resource] = current_quantity + transfer_quantity
            quantity -= transfer_quantity
            graph.nodes[source_island]['resources'][resource] -= transfer_quantity
        
        # Push neighboring islands to the priority queue with updated travel times
        for neighbor in graph.neighbors(current_island):
            travel_time = graph.edges[current_island, neighbor]['travel_time']
            queue.put((current_time + travel_time, neighbor))
            
distribute_resource(sea_of_islands, "Hawaii", "kahelelani_shells", 120, canoe_capacity=120)

print("Resource distribution AFTER:")
for island in sea_of_islands.nodes(data=True):
    print(island)