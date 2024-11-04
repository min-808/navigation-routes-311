import networkx as nx
from collections import deque

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

def find_shortest_route(graph, start_island):
    # Precompute the total experience time for each island
    experience_times = {node: sum(data.get("experiences", {}).values()) for node, data in graph.nodes(data=True)}
    islands = list(graph.nodes)
    n = len(islands)
    best_time = float('inf')
    best_route = None

    # Use a queue for BFS traversal
    queue = deque()
    # Each queue item: (current_node, visited_islands_set, total_time, route_list, visited_experiences_set)
    initial_time = experience_times[start_island]
    queue.append((start_island, set([start_island]), initial_time, [start_island], set([start_island])))

    while queue:
        current_node, visited_islands, total_time, route, visited_experiences = queue.popleft()

        # If all islands have been visited, check if this route is the best
        if len(visited_islands) == n:
            if total_time < best_time:
                best_time = total_time
                best_route = route
            continue

        # Explore all possible next islands
        for neighbor in graph.successors(current_node):
            travel_time = graph[current_node][neighbor]['travel_time']
            new_total_time = total_time + travel_time

            # Add experience time only if the experiences at the neighbor haven't been done yet
            if neighbor not in visited_experiences:
                new_total_time += experience_times[neighbor]
                new_visited_experiences = visited_experiences | {neighbor}
            else:
                new_visited_experiences = visited_experiences.copy()

            # Revisit islands if necessary to reach unvisited ones
            new_visited_islands = visited_islands | {neighbor}
            new_route = route + [neighbor]

            # Prune paths that are already longer than the best found
            if new_total_time >= best_time:
                continue

            queue.append((neighbor, new_visited_islands, new_total_time, new_route, new_visited_experiences))

    if best_route is not None:
        return best_route, best_time
    else:
        return [], "No valid route found"

# Example usage
if __name__ == "__main__":
    # Starting island
    start_island = "Samoa"

    # Find the shortest route
    route, total_time = find_shortest_route(sea_of_islands, start_island)

    # Output the result
    if route:
        print(f"The best route starting from {start_island} is {route} with a total time of {total_time}")
    else:
        print(f"{total_time}")
