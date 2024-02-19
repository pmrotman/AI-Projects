import numpy as np

class Node():
    def __init__(self, state, x_coordinate, y_coordinate):
        self.state = state
        self._x = x_coordinate
        self._y = y_coordinate
        self.children = {}

    def add_connection(self, city):
        d = self.distance(city)
        self.children[city] = d
        city.children[self] = d

    def distance(self, city):
        x1 = self._x * np.pi / 180
        x2 = city._x * np.pi / 180
        y1 = self._y * np.pi / 180
        y2 = city._y * np.pi / 180


        havlat = np.sin((x2-x1)/2)**2
        havlon = np.sin((y2-y1)/2)**2

        hav = havlat + np.cos(x1)*np.cos(x2)*havlon        

        return 2 * 3958.8 * np.arcsin(np.sqrt(hav))

def BeFS(start, goal, f = abs):
    visited = set()
    queue = [(0, start, [start])]
    while queue:
        queue.sort(key = lambda x: f(x[0]))
        cost, current, path = queue.pop(0)
        if current == goal:
            return path, len(visited)
        for n,c in current.children.items():
            if n not in visited or c < cost:
                visited.add(n)
                new_path = path + [n]
                queue.append((c, n, new_path))

    return None, None



def UCS(start, goal):
    visited = set()
    queue = [(0, start, [start])]
    while queue:
        queue.sort(key = lambda x: x[0])
        cost, current, path = queue.pop(0)
        if current == goal:
            return path, len(visited)
        if current not in visited:
            visited.add(current)
            for n, c in current.children.items():
                new_cost = cost + c
                new_path = path + [n]
                queue.append((new_cost, n, new_path))
    return None, None
def BFS(start, goal):
    visited = set()
    queue = [(start, [start])]
    while queue:
        current, path = queue.pop(0)
        if current == goal:
            return path, len(visited)
        if current not in visited:
            visited.add(current)
            for n, _ in current.children.items():
                new_path = path + [n]
                queue.append((n, new_path))

    return None, None

def DFS(start, goal):
    visited = set()
    stack = [(start, [start])]
    while stack:
        current, path = stack.pop()
        if current == goal:
            return path, len(visited)
        if current not in visited:
            visited.add(current)
            for n, _ in current.children.items():
                new_path = path + [n]
                stack.append((n, new_path))
    return None, None

def BiS(start, goal):
    visited_s = set()
    visited_g =set()
    queue_s = [(0, start, [start])]
    queue_g = [(0, goal, [goal])]
    while queue_s or queue_g:
        current_s = queue_s.pop(0)
        current_g = queue_g.pop(0)
    


    return None
def search(start, goal, method):
    path, total_visited = method(start, goal)
    print(str(method))
    print(f"Path: {[city.state for city in path]}")
    print(f"Cost: {sum([path[i].children[path[i+1]] for i in range(len(path)- 1)])}, Number Visited: {total_visited}\n")


def main():
    cities = { "Miami":(25.76, 80.19), "Orlando":(28.54, 81.38),"Tallahassee":(30.44, 84,28), "Jacksonville":(30.33, 81,66), "Tampa":(27.95, 82.46), 
              "Atlanta":(33.75, 84.39), "Macon":(32.84, 83.63), "Savannah":(32.08, 81.09), "Columbia":(34.00, 81.03), "Charleston SC":(32.78, 79.93), 
              "Raleigh":(35.78, 78.64), "Charlotte":(35.23, 80.84), "Wilmington NC":(34.21, 77.89), "Asheville":(35.60, 82.55), "Montgomery":(32.38, 86.31), "Mobile":(30.70, 88.04), 
              "Jackson":(32.30, 90.18), "Nashville":(36.16, 86.78), "Memphis":(35.15,90.05), "Baton Rouge":(30.45, 91.19), "New Orleans":(29.95, 90.07), 
              "Dallas":(32.78, 96.80), "San Antonio":(29.43, 98.49), "Austin":(30.27, 97.74), "Houston":(29.76,95.37), "Little Rock":(34.74, 92.29), "Oklahoma City":(35.47, 97.52), "Tulsa":(36.15, 95.99),
                "St. Louis":(38.63, 90.20), "Kansas City":(39.10, 94.58), "Lexington":(38.04, 84.50), "Louisville":(38.25, 85.76), "Charleston":(38.35, 81.63), "Richmond":(37.54, 77.44),
                "Virginia Beach":(36.85, 75.98), "Washington":(38.91, 77.04), "Baltimore":(39.30, 76.61), "Annapolis":(38.98, 76.49), "Philadelphia":(39.95, 75.16), "Pittsburgh":(40.44, 80.00), 
                "Dover":(39.16,75.52), "Trenton":(40.22, 74.76), "Atlantic City":(39.36, 74.42), "New York":(40.71, 74.01), "Albany":(42.65, 73.76), "Buffalo":(42.89, 78.88), "Hartford":(41.77, 72.67),
                "Providence":(41.82, 71.41), "Boston":(42.36, 71.06), "Worcester":(42.26, 71.80), "Concord":(43.21, 71.54), "Augusta":(33.47, 82.01), "Portland ME":(43.66, 70.26), "Bangor":(44.80,68.77),
                "Montpelier":(44.26, 72.58), "Cleveland":(41.50,81.69), "Columbus":(39.96, 83.00), "Cincinatti":(39.10, 84.51), "Indianapolis":(39.77,86.16), "Detroit":(42.33, 83.05), "Lansing":(42.73, 84.56), 
                "Chicago":(41.88, 87.63), "Springfield":(39.78, 89.65), "Milwaulkee":(43.04, 87.91), "Madison":(43.07, 89.40), "Green Bay":(44.51, 88.01), "St. Paul":(44.95, 93.09), "Des Moines":(41.59, 93.62), 
                "Topeka":(39.05, 95.68), "Lincoln":(40.81, 96.70), "Omaha":(41.26, 95.93), "Pierre":(44.37, 100.35), "Bismarck":(46.80, 100.79), "Fargo":(46.88, 96.79), "Santa Fe":(35.69, 105.94), "Albuquerque":(35.08, 106.65),
                "Phoenix":(33.45, 112.07), "Tuscon":(32.35, 110.97), "Flagstaff":(35.20,111.65), "Denver":(39.74,104.99), "Colorado Springs":(38.83,104.82), "Cheyenne":(41.14, 104.82), "Helena":(46.59,112.04),
                "Boise":(43.52, 116.20), "Salt Lake City":(40.76,111.89), "Las Vegas":(36.17,115.14), "Carson City":(39.16, 119.77), "Reno":(39.53, 119.81), 
                "Seattle":(47.61, 112.33), "Olympia":(47.04, 122.90), "Spokane":(47.66, 117.42), "Portland":(45.52, 112.68), "Salem":(44.94, 123.04), 
                "Sacramento":(38.38, 121.49), "San Francisco":(37.77,122.42), "Los Angeles":(34.05, 118.24), "San Diego":(32.72, 117.16),
                "Juneau":(58.30,134.42), "Nome":(64.50, 165.41), "Honolulu":(21.31,157.86)}
    nodes = []
    for city in cities:
        coords = cities[city]
        x = coords[0]
        y = coords[1]
        nodes.append(Node(city, x, y))
    for i in range(len(nodes)):
        city = nodes[i]
        children = city.children
        for n in nodes:
            if n!=city and city.distance(n) < 500:
                if n not in children:
                    city.add_connection(n)
    city_nodes = {}
    i = 0
    for city in list(cities.keys()):
        city_nodes[city] = nodes[i]
        i+=1



    
    while True:
        search_type = input("Enter search type: BFS, DFS, UCS, BeFS or 0 for exit.")
        if search_type == 0:
            break
        searchdict = {"BFS":BFS, "DFS":DFS, "UCS":UCS, "BeFS":BeFS}
        search_type = searchdict[search_type]
        start = city_nodes[input("What city will you start from?")]
        goal = city_nodes[input("What is you end city?")]
        search(start, goal, search_type)
main()