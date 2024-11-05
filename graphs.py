import networkx as nx
import heapq

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

# QUESTION 1:
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

# QUESTION 2:
def distribute_resource(graph, source_island, resource, quantity, canoe_capacity, canoe_count):
    """
    Distributes a specified quantity of a resource from a source island to other islands in a graph.

    Parameters:
    graph (networkx.DiGraph): The directed graph representing the islands and routes between them.
    source_island (str): The starting island from which the resource distribution begins.
    resource (str): The type of resource to be distributed.
    quantity (float): The total quantity of the resource to be distributed.
    canoe_capacity (float): The maximum capacity of the canoe used for transporting the resource.
    canoe_count (int): The number of canoes available.

    Returns:
    None

    The function calculates the target resource level for each island based on its population and 
    distributes the resource from the source island to other islands using a priority queue to 
    ensure the shortest travel time. It updates the resource levels of the source_island as it traverses 
    the graph.
    """
    # Calculate the total population to determine the even distribution amount
    total_population = sum(graph.nodes[island]['population'] for island in graph.nodes())
    resource_per_person = quantity / total_population

    # Set target resource levels for each island based on population
    target_resource = {
        island: resource_per_person * graph.nodes[island]['population']
        for island in graph.nodes()
    }
    
    # Priority queue for processing islands in order of shortest travel time
    queue = PriorityQueue()
    queue.put((0, source_island))
    
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
            transfer_quantity = min(needed_quantity, canoe_capacity * canoe_count)
            transfer_quantity = round(transfer_quantity)  # Round to the nearest whole number
            graph.nodes[current_island]['resources'][resource] = current_quantity + transfer_quantity
            quantity -= transfer_quantity
            graph.nodes[source_island]['resources'][resource] -= transfer_quantity
        
        # Push neighboring islands to the priority queue with updated travel times
        for neighbor in graph.neighbors(current_island):
            travel_time = graph.edges[current_island, neighbor]['travel_time']
            queue.put((current_time + travel_time, neighbor))

# QUESTION 3:

class Canoe:
    source = sea_of_islands.nodes["Rapanui"]
    destination = None
    resource = None
    time_of_move = -1 # -1 for not moving
    
def find_shortest_path(graph, source, destinations):
    node_distance = []
    for node in graph.nodes():
        if node in source_islands:
            node_distance.append(0)
        else:
            node_distance.append(float('inf'))
    prev = {node: None for node in graph.nodes()}
    
    # Min-heap priority queue for selecting the node with the smallest distance
    priority_queue = [(0, source)]  # (distance, node)
    
    for current_node in range(0, len(source_islands)):
        # Pop the node with the smallest tentative distance
        current_dist, node = heapq.heappop(priority_queue)
        
        # If the distance is not optimal anymore, skip it
        if current_dist > node_distance[current_node]:
            continue
        
        # Explore the neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            # Get the weight of the edge from current_node to neighbor
            edge_weight = graph[current_node][neighbor].get('travel_time', 1)  # Default weight = 1
            
            # Calculate the tentative distance to the neighbor
            alternative_dist = current_dist + edge_weight
            
            # If a shorter path is found to the neighbor, update its distance and previous node
            if alternative_dist < node_distance[neighbor]:
                node_distance[neighbor] = alternative_dist
                prev[neighbor] = current_node
                heapq.heappush(priority_queue, (alternative_dist, neighbor))
    
    # Reconstruct the paths and distances for the specified destinations
    destination_paths = {}
    destination_distances = {}
    
    for dest in destinations:
        minDistance = float('inf')
        if node_distance[dest] != float('inf'):  # If there's a valid path to the destination
            # Reconstruct the path from source to the destination
            path = []
            current = dest
            while current is not None:
                path.append(current)
                current = prev[current]
            
            path.reverse()  # Reverse the path to get it from source to destination
            destination_paths[dest] = path
            destination_distances[dest] = node_distance[dest]
            if minDistance > destination_distances[dest]:
                minPath = destination_paths[dest]
                minDistance = destination_distances[dest]
                destination = dest
    
    
    return destination, minDistance    

time = 0
canoes = []
total_canoes = 3
resource_to_distribute = 'kukui_nuts'
islands_left = []
source_islands = []
is_Done = False

for num in range (0, total_canoes):
    canoes.append(Canoe())
    
for node, attributes in sea_of_islands.nodes(data=True):       # Seperate sources and destinations
    if attributes.get('kukui_nuts') == 0:
        islands_left.append(node)
    elif attributes.get('kukui_nuts') > 1:
        source_islands.append(node)

while(time < 1000 and not is_Done):
    is_Done = False
    for canoe in canoes:   # Update canoe status
        
        if canoe.time_of_move == 0:
            canoe.destination['kukui_nuts'] += 1
            canoe.source = canoe.destination
            canoe.destination = None
            canoe.resource = None
            
        if canoe.time_of_move == -1:
            if(getattr(canoe.source, 'kukui_nuts', 0) == 1):   # Must find a new source
                canoe.destination, canoe.time_of_move = find_shortest_path(sea_of_islands, canoe.source, source_islands)
            else:
                canoe.resource = 'kukui_nuts'
                canoe.source['kukui_nuts'] -= 1
                canoe.destination, canoe.time_of_move = find_shortest_path(sea_of_islands, canoe.source, islands_left)    
                
        else:
            canoe.time_of_move -= 1            
            
    for node in sea_of_islands.nodes:   # Update kukui nut and set to end simulation if all islands have kukui nuts
        if node['kukui_nuts'] == 0:
            is_Done = True
        else:
            if(node['time_to_grow'] == 0):
                node['time_to_grow'] = 10
                node['kukui_nuts'] *= 2
            else:
                node['time_to_grow'] -= 1
    
    
    time += 1
print("Time took: ", time)

# QUESTION 4:
# Dijkstra's algorithm to find the shortest route with unique experiences
def find_shortest_route(graph, start_island):
    # Precompute experience times for each island
    experience_times = {node: sum(data.get("experiences", {}).values()) for node, data in graph.nodes(data=True)}
    islands = list(graph.nodes)
    n = len(islands)
    best_time = float('inf')
    best_route = None

    # Initialize the priority queue
    priority_queue = []
    initial_time = experience_times[start_island]
    heapq.heappush(priority_queue, (initial_time, start_island, set([start_island]), [start_island], set([start_island])))

    while priority_queue:
        total_time, current_node, visited_islands, route, visited_experiences = heapq.heappop(priority_queue)

        # If all islands are visited, update the best time if this path is shorter
        if len(visited_islands) == n:
            if total_time < best_time:
                best_time = total_time
                best_route = route
            continue

        # Explore all neighboring islands
        for neighbor in graph.successors(current_node):
            travel_time = graph[current_node][neighbor]['travel_time']
            new_total_time = total_time + travel_time

            # Add experience time if and only if this island’s experiences are new
            if neighbor not in visited_experiences:
                new_total_time += experience_times[neighbor]
                new_visited_experiences = visited_experiences | {neighbor}
            else:
                new_visited_experiences = visited_experiences.copy()

            # Update the visited islands and route
            new_visited_islands = visited_islands | {neighbor}
            new_route = route + [neighbor]

            # Only add to the queue if this path is shorter than the best time found
            if new_total_time < best_time:
                heapq.heappush(priority_queue, (new_total_time, neighbor, new_visited_islands, new_route, new_visited_experiences))

    return best_route, best_time if best_route else ("No valid route found",)

# ***Testing***
if __name__ == "__main__":
    # Starting island
    start_island = "Tahiti"

    # Find the shortest route
    route, total_time = find_shortest_route(sea_of_islands, start_island)

    # Output the result
    if route:
        print(f"The best route starting from {start_island} is {route} with a total time of {total_time}")
    else:
        print(total_time)
