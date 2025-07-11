import pandas as pd
import heapq
from termcolor import colored
import copy
import tkinter as tk
import random
import threading

# read graph data from and excel file which contains two sheets: 
#   1) Distances sheet (necessary)
#   2) Delays sheet (optional)
# graph data will save a structure like this: { origin_city: ( terminal_delay, { destination_city: travel_time })}
def read_from_excel() :

    path = input("excel file path: \n")

    try:
        xls = pd.ExcelFile(path)
        print(colored("Excel file imported successfully", "green"))
    except:
        print(colored("Could't import Excel file", "red"))
        exit()

    try:
        distances_df = xls.parse("Distances", header=0, index_col=0)
        print(colored("Distances sheet found", "green"))
    except:
        print(colored("Distances sheet not found", "red"))
        exit()

    # read first row as city names
    cities = distances_df.head()

    try:
        delays_df = xls.parse("Delays",)
        print(colored("Delays sheet found", "green"))
        map_graph = {city:(int(delays_df.loc[0, city]), {}) for city in cities}
    except:
        print(colored("Delays sheet missing or bad, setting all delays = 0", "yellow"))
        map_graph = {city:(0, {}) for city in cities}
    
    for origin in cities:
        for destination in cities:
            distance = int(distances_df.loc[origin, destination])
            if distance<0:
                continue
            map_graph[origin][1].update({destination: distance})    

    return map_graph

# find the best way between two terminals based on time
# here i used dijkstra algorithm to find the best way
def find_best_way(start, end, speed, graph):

    # based on dijkstra initially we set reach time unlimited for each location except origin 
    reach_time = {city: float('inf') for city in graph}
    reach_time[start] = 0

    previous_city = {city: None for city in graph}
    queue = [(0, start)]

    while queue:
        elapsed_time, city = heapq.heappop(queue)
        if city == end:
            break
        
        # we shouldn't consider start and end delays
        terminal_delay = graph[city][0] if city != start and city != end else 0

        for neighbor_city in graph[city][1]:
            travel_distance = graph[city][1][neighbor_city]

            # to convert distance to time: time(minutes) = distance(Km) / speed(Km/h) * 60
            travel_time = travel_distance/speed*60

            new_reach_time = elapsed_time + travel_time + terminal_delay

            if new_reach_time<reach_time[neighbor_city]:
                reach_time[neighbor_city] = new_reach_time
                previous_city[neighbor_city] = city
                heapq.heappush(queue, (new_reach_time, neighbor_city))
    
    route = []
    node = end

    # the reason for ignoring the start is that to add it later while we want to connect road pieces later
    while node != start:
        route.append(node) 
        node = previous_city[node]

    route.reverse()
    elapsed_time = reach_time[end]
    return route

# get a list of terminals and map graph to calculate route time(minutes) and distance(Km)
def calc_time_and_distance(route, graph):
    total_time = 0
    total_distance = 0
    terminal_delay = 0
    start = route[0]
    for end in route[1:]:
        travel_distance = graph[start][1][end]
        travel_time = travel_distance/100*60
        total_time += travel_time + terminal_delay
        total_distance += travel_distance
        start = end
        terminal_delay = graph[start][0]

    return (total_time, total_distance)

# sets a random position for vertexes to show it graphically
def set_positions(graph, canvas_size):

    positions = {}

    # creates a percentage range between 4 to 96 i divided it by 80/len(graph) to prevent alongside locations
    x_range = list(range(4, 96, int(80/len(graph))))
    y_range = list(range(4, 96, int(80/len(graph))))

    #select a percentage and pop it to avoid boilerplate locations
    for node in graph:
        i = random.choice(range(len(x_range) -1 ))
        x = x_range.pop(i)
        i = random.choice(range(len(y_range) -1 ))
        y = y_range.pop(i)

        # convert percentage to a location coordinates
        positions.update({node: (x*canvas_size/100, y*canvas_size/100)})

    return positions

    # shows graph (draw it on a tkinter canvas)
def generate(canvas, node_positions, way):

    canvas.delete("all")

    for node in graph:
            x1, y1 = node_positions[node]
            for neighbor in graph[node][1]:
                if neighbor == node:
                    continue

                x2, y2 = node_positions[neighbor]
                distance1 = graph[node][1][neighbor]

                # get backward distance if is possible
                try:
                    distance2 = graph[neighbor][1][node]
                except:
                    distance2 = -1

                # draws edges
                canvas.create_line(
                    x1, y1, x2, y2,
                    smooth = True,
                    fill = "skyblue"
                )

                # shows distances
                canvas.create_text(
                    (x1+x2)/2,
                    (y1+y2)/2,
                    text = f"{sorted((distance1, distance2))}",
                    fill = "white",
                    font = ("Arial", 7)
                )

    # redraw to show best way    
    for i in range(len(way)-1):
        v = way[i]
        u = way[i+1]
        x1, y1 = node_positions[v]
        x2, y2 = node_positions[u]
        canvas.create_line(
            x1, y1, x2, y2,
            smooth = True,
            fill = "yellow"
        )

    node_radius = 20
    for node in graph:
        x, y = node_positions[node]

        # draw vertexes
        canvas.create_oval (
            x - node_radius,
            y - node_radius,
            x + node_radius,
            y + node_radius,
            fill='skyblue',
        )

        terminal_delay = str(graph[node][0])

        canvas.create_text(
            x,
            y,
            text=node[:3]+"\n"+terminal_delay,
            font=("Arial", 10),
            justify = "center"
        )

    canvas.update()

# prepares a tkinter to show graphs     
def draw_graph(graph, way, tittle):
    way = way[1]
    canvas_size = 800
    
    root = tk.Tk()
    root.title(tittle)
    root.configure(bg="black")
    
    button = tk.Button(
        root,
        text="regenerate",
        command=lambda: generate(canvas, set_positions(graph, canvas_size), way)
    )

    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='black')

    generate(canvas, set_positions(graph, canvas_size), way)

    button.pack()
    canvas.pack()
    root.mainloop()
    
###########################################################################


graph = read_from_excel()
cities = graph.keys()

requested_ways = input(f"Enter your travel ways for example: Tabriz-Isfahan-Zahedan \ncities: {cities}\n")
requested_terminals_list = requested_ways.split('-')

speed = float(input("enter average speed(Km/H): \n"))

all_ways = []
best_way = []
start = requested_terminals_list[0]

# to find the best way first we calculate it for each pieces means if we have a midway terminal we calculate
# best way from origin to midway then find the best way from origin to end terminal the we connect them to gether
# to create full way
best_way.append(start)
for end in requested_terminals_list[1:]:
    a_piece_of_way = find_best_way(start, end, speed, graph)
    best_way.extend(a_piece_of_way)
    start = end

all_ways.append((calc_time_and_distance(best_way, graph), best_way))

# to find alternate way, every time we remove each edges of best way from map graph and calculate the best way again 
# and save it then we sort them and get the way with lowest distance
v = best_way[0]
for u in best_way[1:]:
    modified_graph = copy.deepcopy(graph)
    modified_graph[v][1].pop(u)

    alternate_way = []

    start = requested_terminals_list[0]
    alternate_way.append(start)
    for end in requested_terminals_list[1:]:
        a_piece_of_way = find_best_way(start, end, speed, modified_graph)
        alternate_way.extend(a_piece_of_way)
        start = end

    heapq.heappush(all_ways, (calc_time_and_distance(alternate_way, modified_graph), alternate_way))
    v = u

for i, way in enumerate(all_ways):
    if i>1:
        break
    print(colored(f"way{i+1}: ", "green"))
    total_time, total_distance = way[0]
    total_terminals = way[1]
    
    print(f"{colored("terminals", "light_cyan")}: {" -> ".join(total_terminals)}")
    print(f"{colored("total time", "light_cyan")}: {total_time}")
    print(f"{colored("total distance", "light_cyan")}: {total_distance}")

yes_or_no = input(colored("do you want to show the graphs? (y, n)\n", "yellow")).lower()
if yes_or_no != "y" and yes_or_no != "yes":
    exit()

for i, way in enumerate(all_ways):
    if i>1:
        break
    t = threading.Thread(target=draw_graph, args=(graph, way, f"way{i+1}'s graph"))
    t.start()

# developed by Amirhossein Foorjanizadeh



