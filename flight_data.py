import csv
from collections import defaultdict
from datetime import datetime, timedelta
import sys


FILE_PATH = sys.argv[1]


# Function to create list of flight
def create_list(FILE_PATH):
    list_of_records = []
    with open(FILE_PATH, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            list_of_records.append(row)
    return list_of_records


# Function to build the graph
def build_graph():
    edges = create_list(FILE_PATH)
    graph = defaultdict(list)
    # Loop to iterate over every edge of the graph
    for edge in edges:
        # Order exchange
        edge[0], edge[1] = edge[1], edge[0]
        edge.append(edge[0])
        # Creating the graph as adjacency list
        graph[edge[0]].append(edge[1:])
    return graph
     
 
# Function to find the shortest path between two nodes of a graph
def BFS_SP(graph, start, goal):
    explored = []
     
    queue = [[start]]
    queue_price = [[]]
     
    # If the start and finish are the same place
    if start == goal:
        print(f"You have selected the same start and end point \n ({start})")
        exit()

    # Resulting dictionary of possible flights
    possible_flights = {}

    while queue:
        path = queue.pop(0)
        path_price = queue_price.pop(0)
        node = path[-1]
        # It examines all the nodes one by one
        if node not in explored:
            neighbours = graph[node]
            for num, neighbour in enumerate(neighbours):
                # List of flights
                new_path = list(path)
                new_path.append(neighbour[1])
                queue.append(new_path)
                # List of prices
                new_path_price = list(path_price)
                new_path_price.append(neighbour)
                queue_price.append(new_path_price)

                if neighbour[1] == goal:
                    possible_flights[num] = new_path_price

            explored.append(node)

    return possible_flights

# Function to layover time control
def layover_time(start, end):
    possible_flights = BFS_SP(build_graph(), start, end)
    print(possible_flights)   
    for value, key in enumerate(possible_flights):
        for num, y in enumerate(possible_flights[key]):
            # Only for flights that have a layover
            try:
                first_time, second_time = datetime.fromisoformat(possible_flights[key][num+1][2]), datetime.fromisoformat(possible_flights[key][num][3])
                # In case of a combination of A -> B -> C, the layover time in B should not be less than 1 hour and more than 6 hours.
                if ((first_time - second_time) < timedelta(hours = 1)) or ((first_time - second_time) > timedelta(hours = 6)) or (first_time - second_time) < timedelta(hours = 0):
                    possible_flights[key] = []
            # This is a flight without layover
            except IndexError:
                pass
    
    # Removes items that did not meet the time condition
    possible_flights = {key:val for key, val in possible_flights.items() if val != []}
    
    return possible_flights

# Function to sort the dictionary according to the price
def sort_by_price(start, end):
    possible_flights = layover_time(start, end)
    # Adding total price for flights
    for i in possible_flights:
        price = 0
        for y in possible_flights[i]:
            price += float(y[4])
        possible_flights[i].append(price)

    # Sorting by total price
    sorted_dict = dict(sorted(possible_flights.items(), key=lambda item: item[1][-1], reverse=False))
    return sorted_dict

# Function to create output
def output(start, end):
    possible_flights = sort_by_price(start, end)
    output = []
    for i in possible_flights:
        output.append({
            "flights": []
        })
        # Initial variable for luggage
        bags_allowed = 99
        for value in possible_flights[i]:
            if type(value) == list:
                # Adds individual flight information
                output[-1]['flights'].append({
                    "flight_no": value[0],
                    "origin": value[7],
                    "destination": value[1],
                    "departure": value[2],
                    "arrival": value[3],
                    "base_price": value[4],
                    "bag_price": value[5],
                    "bags_allowed": value[6]
                })
                # Looking for the least amount of luggage on the flight
                if bags_allowed > int(value[6]):
                    bags_allowed = int(value[6])

            # If it is not a list, it will save the total price per flight        
            else:
                price = value

        # Adds summary information about flights        
        output[-1]["bags_allowed"] = bags_allowed
        output[-1]["destination"] = end
        output[-1]["origin"] = start
        output[-1]["total_price"] = price
        output[-1]["travel_time"] = str((datetime.fromisoformat(output[-1]["flights"][-1]['arrival'] + '+00:00') - datetime.fromisoformat(output[-1]["flights"][0]['departure'] + '+00:00')))
    
    # If there is no connection
    if len(output) == 0:
        return f"There is no connection between these places! \n(place A: {start}, place B: {end})"
    return output


if __name__ == "__main__":     
    print(output(sys.argv[2], sys.argv[3]))
