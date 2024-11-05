import networkx as nx
from heapq import heappush, heappop

# Create a directed graph
sea_of_islands = nx.DiGraph()

# Add islands (nodes) with attributes
sea_of_islands.add_node("Aotearoa", population=5220000, resources={"kahelelani_shells": 30, "ʻuala": 60, "kalo": 70, "kukui_nuts": 50})
sea_of_islands.add_node("Hawaii", population=1430000, resources={"kahelelani_shells": 20, "ʻuala": 90, "kalo": 85, "kukui_nuts": 75})
sea_of_islands.add_node("Tahiti", population=191000, resources={"kahelelani_shells": 70, "ʻuala": 50, "kalo": 60, "kukui_nuts": 40})
sea_of_islands.add_node("Rapanui", population=7700, resources={"kahelelani_shells": 15, "ʻuala": 20, "kalo": 30, "kukui_nuts": 10})
sea_of_islands.add_node("Samoa", population=218000, resources={"kahelelani_shells": 50, "ʻuala": 80, "kalo": 90, "kukui_nuts": 60})

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

# Priority queue to select the next island based on priority score
def calculate_priority(island, time_since_last_visit):
    return sea_of_islands.nodes[island]['population'] * time_since_last_visit

# Sample function to get the next travel plan
def get_travel_plan(islands, current_island, time_elapsed):
    priority_queue = []
    for island in islands.nodes:
        if island != current_island:
            priority_score = calculate_priority(island, time_elapsed[island])
            heappush(priority_queue, (-priority_score, island))  # Use negative for max-heap behavior

    # Generate travel plan
    travel_plan = []
    while priority_queue:
        _, island = heappop(priority_queue)
        travel_plan.append(island)
    return travel_plan

# First plan, all islands have a time_elapsed of 1, starting at Aotearoa
time_elapsed = {island: 1 for island in sea_of_islands.nodes}
current_island = "Aotearoa"
travel_plan = get_travel_plan(sea_of_islands, current_island, time_elapsed)
print("First Travel Plan:", travel_plan)

# Second plan, Tahiti has a time_elapsed of 10, starting at Aotearoa
time_elapsed = {island: (10 if island == "Tahiti" else 1) for island in sea_of_islands.nodes}
current_island = "Aotearoa"
travel_plan = get_travel_plan(sea_of_islands, current_island, time_elapsed)
print("Second Travel Plan:", travel_plan)

# Third plan, every island except Hawaii has a time_elapsed of 15, starting at Rapanui
time_elapsed = {island: (10 if (island == "Tahiti" or island == "Samoa" or island == "Aotearoa") else 1) for island in sea_of_islands.nodes}
current_island = "Rapanui"
travel_plan = get_travel_plan(sea_of_islands, current_island, time_elapsed)
print("Third Travel Plan:", travel_plan)