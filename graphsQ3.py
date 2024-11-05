import networkx as nx      

# Create a directed graph
sea_of_islands = nx.DiGraph()

# Add islands (nodes) with attributes
sea_of_islands.add_node("Aotearoa", population=5220000, kukui_nuts = 0, time_to_grow = 50)
sea_of_islands.add_node("Hawaii", population=1430000, kukui_nuts = 0, time_to_grow = 50)
sea_of_islands.add_node("Tahiti", population=191000, kukui_nuts = 0, time_to_grow = 50)
sea_of_islands.add_node("Rapanui", population=7700, kukui_nuts = 10, time_to_grow = 50)
sea_of_islands.add_node("Samoa", population=218000, kukui_nuts = 0, time_to_grow = 50)

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
    source = None
    destination = None
    resource = None
    time_of_move = 0

time = 0
canoes = []
total_canoes = 3
resource_to_distribute = 'kukui_nuts'

for num in range (0, total_canoes):
    canoes.append(Canoe())

while(time < 1000 and not is_Done):
    is_Done = True
    for canoe in canoes:
        if canoe.time_of_move == 0:
            distribute_resource(canoe)
    

    for canoe in canoes:
        if canoe.time_of_move != 0:
            canoe.time_of_move -= 1
            
    for node in sea_of_islands.nodes:   # Update kukui nut and set to end simulation if all islands have kukui nuts
        if node['kukui_nuts'] == 0:
            is_Done = False
        else:
            if(node['time_to_grow'] == 0):
                node['time_to_grow'] = 10
                node['kukui_nuts'] *= 2
            else:
                node['time_to_grow'] -= 1
    
    
    time += 1
print("Total time took: ", time)
