import networkx as nx
import heapq

# Create a directed graph representing the sea of islands
sea_of_islands = nx.DiGraph()

# Add islands (nodes) with attributes including experiences and their times
sea_of_islands.add_node("Aotearoa", population=5220000, experiences={"canoe_ride": 1, "mountain_climb": 2})
sea_of_islands.add_node("Hawaii", population=1430000, experiences={"surfing": 3, "volcano_visit": 4})
sea_of_islands.add_node("Tahiti", population=191000, experiences={"snorkeling": 2, "cultural_tour": 1})
sea_of_islands.add_node("Rapanui", population=7700, experiences={"moai_tour": 3})
sea_of_islands.add_node("Samoa", population=218000, experiences={"beach_day": 2, "traditional_dance": 1})

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
