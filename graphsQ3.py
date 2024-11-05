import networkx as nx   
import heapq   

# Create a directed graph
sea_of_islands = nx.DiGraph()

# Add islands (nodes) with attributes
sea_of_islands.add_node("Aotearoa", population=5220000, kukui_nuts = 0, time_to_grow = 10)
sea_of_islands.add_node("Hawaii", population=1430000, kukui_nuts = 0, time_to_grow = 10)
sea_of_islands.add_node("Tahiti", population=191000, kukui_nuts = 0, time_to_grow = 10)
sea_of_islands.add_node("Rapanui", population=7700, kukui_nuts = 10, time_to_grow = 10)
sea_of_islands.add_node("Samoa", population=218000, kukui_nuts = 0, time_to_grow = 10)

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
