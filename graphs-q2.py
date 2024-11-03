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

print("Islands and their attributes:")
for island in sea_of_islands.nodes(data=True):
    print(island)

print("\nRoutes and travel times:")
for route in sea_of_islands.edges(data=True):
    print(route)

# feel free to use this graph to test out your functions

def distribute_resource(graph, source_island, resource, quantity):
    queue = PriorityQueue()
    queue.put((0, source_island, quantity))
    distributed = {island: 0 for island in graph.nodes}
    visited = set()
    while not queue.empty():
        dist, current_island, remaining_quantity = queue.get()
        if current_island in visited:
            continue
        visited.add(current_island)
        distribute_amount = min(remaining_quantity, quantity - distributed[current_island])
        distributed[current_island] += distribute_amount
        remaining_quantity -= distribute_amount
        neighbors = list(graph.neighbors(current_island))
        if neighbors and remaining_quantity > 0:
            share = remaining_quantity / len(neighbors)
            for neighbor in neighbors:
                travel_time = graph[current_island][neighbor]['travel_time']
                queue.put((dist + travel_time, neighbor, share))
    return distributed

distributed_resources = distribute_resource(sea_of_islands, "Hawaii", "kahelelani_shells", 100)
print("Distributed resources:", distributed_resources)

print("Islands and their attributes:")
for island in sea_of_islands.nodes(data=True):
    print(island)


