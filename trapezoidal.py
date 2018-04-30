import numpy as np
import math
from collections import defaultdict, deque
import pygame

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
LIGHT_BLUE = (0, 255, 255)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)
RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Class for class of Connectivity Graph for Dijkstra's algorithm
class constructGraph(object):
    def __init__(self):
        self.vertex = set()
        self.distances = {}
        self.edges = defaultdict(list)

    def add_vertex(self, value):
        self.vertex.add(value)

    def add_edge(self, src, dst, distance):
        self.edges[src].append(dst)
        self.edges[dst].append(src)
        self.distances[(src, dst)] = distance
        self.distances[(dst, src)] = distance

# Calculation of path
def calculate_path(graph, initial):
    visited = {initial: 0}
    path = {}

    vertex = set(graph.vertex)

    while vertex:
        minimum_node = None
        for node in vertex:
            if node in visited:
                if minimum_node is None:
                    minimum_node = node
                elif visited[node] < visited[minimum_node]:
                    minimum_node = node
        if minimum_node is None:
            break

        vertex.remove(minimum_node)
        current_weight = visited[minimum_node]

        for edge in graph.edges[minimum_node]:
            try:
                weight = current_weight + graph.distances[(minimum_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = minimum_node

    return visited, path

# Finding shortest oath from graph
def shortest_path(graph, origin, destination,ret_dist):
    visited, paths = calculate_path(graph, origin)
    full_path = deque()
    dest = paths[destination]

    while dest != origin:
        full_path.appendleft(dest)
        dest = paths[dest]

    full_path.appendleft(origin)
    full_path.append(destination)

    if ret_dist==1:
        return visited[destination]
    elif ret_dist==0:
        print ("Distance from", origin,"to", destination , "is",visited[destination])
        print ("The path from ",origin,"to",destination,"is", list(full_path))
        return full_path

# Class for outer boundary
class Environment():
    def __init__(self,vertices,edges):
        self.wallvertices_np = vertices
        self.edges = {}
        for index, edge in enumerate(edges):
            self.edges[index] = edge

        self.wallvertices = {}
        for i,vertex in enumerate(vertices):
            self.wallvertices["V"+str(i+1)] = vertex

        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

        for vertex in self.wallvertices_np:
            if vertex[0] > self.x_max:
                self.x_max = vertex[0]
            if vertex[1] > self.y_max:
                self.y_max = vertex[1]
            if vertex[1] < self.y_min:
                self.y_min = vertex[1]
        self.x_min = 0

        self.outer_edges = {}
        for i in range(len(self.wallvertices)):
            if i == len(self.wallvertices)-1:
                self.outer_edges[i] = [self.wallvertices["V" + str(i + 1)], self.wallvertices["V" + str(1)]]
            else:
                self.outer_edges[i] = [self.wallvertices["V"+str(i+1)],self.wallvertices["V"+str(i+2)]]

# Class for inner obstacles
class Obstacle():
    def __init__(self,vertices,edges):
        self.vertices_np = vertices
        self.edges = {}
        self.edges_list = []
        for index,edge in enumerate(edges):
            self.edges[index] = edge
            self.edges_list.append(edge)

# Method to convert points to a homogeneous format of edges which is: [slope,-1,y-intercept] for computation of midpoint
def do_edge_equation(edge):
    edge_equations = np.zeros(3)
    div = float(edge[1][0] - edge[0][0])
    if div == 0:
        m = 10**10
    else:
        m = float(edge[1][1] - edge[0][1]) / div
    c = edge[1][1] - (m * edge[1][0])
    edge_equations[0] = m
    edge_equations[1] = -1
    edge_equations[2] = c
    return edge_equations

# Method to 
def on_segment(pi,pj,pk):
    if((min(pi[0],pj[0])<=pk[0] and pk[0]<=max(pi[0],pj[0])) and  (min(pi[1],pj[1])<=pk[1] and pk[1]<=max(pi[1],pj[1]))):
        return True
    else:
        return False

# Method to calculate cross product(Used in determining if lines intersect
def cross_product(pi,pj,pk):
    return (pk[0]-pi[0])*(pj[1]-pi[1]) - (pj[0]-pi[0])*(pk[1]-pi[1])


# Method to check intersection of lines
def segments_intersect(p1,p2,p3,p4):
    d1 = cross_product(p3,p4,p1)
    d2 = cross_product(p3,p4,p2)
    d3 = cross_product(p1, p2, p3)
    d4 = cross_product(p1,p2,p4)

    if((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
        return True

    if(d1==0 and on_segment(p3,p4,p1)):
        return True

    if (d2 == 0 and on_segment(p3, p4, p2)):
        return True

    if (d3 == 0 and on_segment(p1, p2, p3)):
        return True

    if (d4 == 0 and on_segment(p1, p2, p4)):
        return True

    else:
        return False

# Method to get point of intersection of two lines. Takes two lists which each contain endpoints of the two lines
def point_of_intersection(p1,p2):
    p2 = -p2
    x = - (p2[2]+p1[2])/(p2[0] + p1[0])
    y = (p1[0] * x) + p1[2]
    return [x,y]

# Sort points in the connectivity graph in increasing order of their x coordniates
def bubbleSort(nlist):
    for passnum in range(len(nlist)-1,0,-1):
        for i in range(passnum):
            if nlist[i][0][1]>nlist[i+1][0][1]:
                temp = nlist[i]
                nlist[i] = nlist[i+1]
                nlist[i+1] = temp
    return nlist

# Method for computation of Euclidean distance of two points
def euclidean(a,b):
    return np.sqrt(np.square(a[0] - b[0]) + np.square(a[1] - b[1]))

#
def text_objects(text,font):
    textSurface = font.render(text,True,BLACK)
    return (textSurface,textSurface.get_rect())

# Helper function to scale the original dimensions of the work space to a higher coordinate system which is used for pygame animations. Pass your lists here to convert scale up
def scale(arg):
    scale = 60
    shift_x = 200
    shift_y = 400
    x = shift_x + (scale*arg[0])
    y =  shift_y + (scale*arg[1])
    return [x,y]

# Function which handles all graphics related computations and rendering using pygame
def render(env,obstacles,trapezium_edges,midpoints,connecting_edges,roadmap):

    pygame.init()
    # Set the height and width of the screen
    size = [1200, 1200]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Exact Cell Decomposition")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()


    # For scaling of the outer boundary
    boundary = []
    for vertex in env.wallvertices_np:
        boundary.append(scale(vertex))
    boundary.append(boundary[0])

    # For scaling of obstacles
    obstacle_bounds = []
    for obstacle in obstacles:
        obstacle_boundary = []
        for vertex in obstacle.vertices_np:
            obstacle_boundary.append(scale(vertex))
        obstacle_boundary.append(obstacle_boundary[0])
        obstacle_bounds.append(obstacle_boundary)

    # For scaling trapezium edges(cell boundaries)
    plot_trapeziums = []
    for edge in trapezium_edges:
        temp = []
        for point in edge:
            temp.append(scale(point))
        plot_trapeziums.append(temp)

    # For scaling midpoints of cell boundary midpoints
    plot_midpoints = []
    for i in range(len(midpoints)):
        plot_midpoints.append(scale(midpoints[i]))

    # For connecting edges of the graph
    plot_connectors = []
    for edge in connecting_edges:
        temp = []
        for point in edge:
            temp.append(scale(point))
        plot_connectors.append(temp)

    # For the roadmap of the robot from start to end
    roadmap_plot = []
    for i in roadmap:
        roadmap_plot.append(scale(i))

    # Flags for maintaing the state of the variables in the while loop
    green_flag = 0
    blue_flag = 0
    red_flag = 0
    ind = 0
    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        # render outer boundary
        pygame.draw.lines(screen, BLACK, False, boundary, 5)

        # render obstacles
        for obstacle in obstacle_bounds:
            pygame.draw.lines(screen, BLACK, False, obstacle, 5)

        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()


        # Green Button controller
        if 100+100 > mouse[0] > 100 and 750+50 > mouse[1] > 750:
            pygame.draw.rect(screen, LIGHT_GREEN, (100, 750, 100, 50))
            if clicked[0] == 1:
                # For trapeziums
                green_flag = 1
                for edge in plot_trapeziums:
                    pygame.draw.line(screen, GREEN, edge[0], edge[1], 5)

        else:
            pygame.draw.rect(screen, GREEN, (100, 750, 100, 50))

        # Blue Button controller
        if 100+100 > mouse[0] > 100 and 850+50 > mouse[1] > 850:
            pygame.draw.rect(screen, BLUE, (100, 850, 100, 50))
            if clicked[0] == 1:
                blue_flag = 1
                # For midpoints
                for point in plot_midpoints:
                    pygame.draw.circle(screen, BLUE, [int(point[0]), int(point[1])], 5)
                    # screen.set_at((int(point[0]), int(point[1])), BLUE)

                # For trapeziums
                for edge in plot_connectors:
                    pygame.draw.line(screen, LIGHT_BLUE, edge[0], edge[1], 5)

        else:
            pygame.draw.rect(screen, LIGHT_BLUE, (100, 850, 100, 50))

        # Red Button Controller
        if 300 + 100 > mouse[0] > 300 and 750 + 50 > mouse[1] > 750:
            pygame.draw.rect(screen, LIGHT_RED, (300, 750, 100, 50))
            if clicked[0] == 1:
                red_flag = 1
                pygame.draw.lines(screen, LIGHT_RED, False, roadmap_plot, 5)

        else:
            pygame.draw.rect(screen, RED, (300, 750, 100, 50))

        # Yellow Button Controller
        if 300 + 100 > mouse[0] > 300 and 850 + 50 > mouse[1] > 850:
            pygame.draw.rect(screen, YELLOW, (300, 850, 100, 50))
            if clicked[0] == 1:
                red_flag = 0
                green_flag = 0
                blue_flag = 0

        else:
            pygame.draw.rect(screen, YELLOW, (300, 850, 100, 50))


        # Sustain actions after the clicking of Green, Blue and Red buttons. These actions would be undone when the yellow button is clicked
        if green_flag == 1:
            for edge in plot_trapeziums:
                pygame.draw.line(screen, GREEN, edge[0], edge[1], 5)

        if blue_flag == 1:
            # For midpoints
            for point in plot_midpoints:
                pygame.draw.circle(screen, BLUE, [int(point[0]), int(point[1])], 5)
                # screen.set_at((int(point[0]), int(point[1])), BLUE)

            # For trapeziums
            for edge in plot_connectors:
                pygame.draw.line(screen, LIGHT_BLUE, edge[0], edge[1], 5)

        if red_flag == 1:
            pygame.draw.lines(screen, LIGHT_RED, False, roadmap_plot, 5)

        smallText = pygame.font.Font("freesansbold.ttf",20)

        textSurfGreen, textGreen = text_objects("SWEEP",smallText)
        textGreen.center = ((100 + (100 / 2), (750 + (50 / 2))))
        screen.blit(textSurfGreen,textGreen)


        textSurfBlue, textBlue = text_objects("GRAPH", smallText)
        textBlue.center = ((100 + (100 / 2), (850 + (50 / 2))))
        screen.blit(textSurfBlue, textBlue)

        textSurfRed, textRed = text_objects("PATH", smallText)
        textRed.center = ((300 + (100 / 2), (750 + (50 / 2))))
        screen.blit(textSurfRed, textRed)

        textSurfYellow, textYellow = text_objects("CLEAR", smallText)
        textYellow.center = ((300 + (100 / 2), (850 + (50 / 2))))
        screen.blit(textSurfYellow, textYellow)

        pygame.display.flip()

    pygame.quit()


def main():
    # The env and obsn objects should be in a specific format. The first list is for all vertices of the shape written in coordinates in clockwise order. The second list is a list of edges wherein each individual list is the
    # coordinates of the endpoints of the edges, ie. the pairs of vertices of the shape

    env = Environment([[0, 0], [10, 10], [15, 5] ,[13, -6], [6, -2]] , [[[0,0],[10,10]],[[10,10],[15,5]],[[15,5],[13,-6]],[[13,-6],[6,-2]],[[6,-2],[0,0]]])             # Make changes here to edit the boundary of the workspace

    # Add obstacle objects here
    obs1 = Obstacle([[4,0],[7,3],[6,0],[8,-1]] , [[[4,0],[7,3]],[[7,3],[6,0]],[[6,0],[8,-1]],[[8,-1],[4,0]]])
    obs2 = Obstacle([[11, -2],[12, 3],[14, 1]] , [[[11,-2],[12,3]],[[12,3],[14,1]],[[14,1],[11,-2]]])
    obs3 = Obstacle([[9, 8],[7, 6],[10, 6]] , [[[9,8],[7,6]],[[7,6],[10,6]],[[10,6],[9,8]]])
    obs4 = Obstacle([[8, 4], [7, 0], [10, 4]], [[[8, 4], [7, 0]], [[7, 0], [10, 4]], [[10, 4], [8, 4]]])
    obs5 = Obstacle([[13, 4], [10, 3], [11, 5]], [[[13, 4], [10, 3]], [[10, 3], [11, 5]], [[11, 5], [13, 4]]])
    obstacles = [obs1,obs2,obs3,obs4,obs5]                            # Dont forget to add all the obstcale objects in this list


    # create list for all vertices
    all_vertices = []
    for vertex in env.wallvertices_np:
        all_vertices.append(vertex)

    for obstacle in obstacles:
        for vertex in obstacle.vertices_np:
            all_vertices.append(vertex)


    #create list for all edges
    all_edges = []
    obstacle_edges = []

    for i in range(len(env.outer_edges)):
        all_edges.append(env.outer_edges[i])

    for obstacle in obstacles:
        for i in range(len(obstacle.edges)):
            all_edges.append(obstacle.edges[i])
            obstacle_edges.append(obstacle.edges[i])

    trapezium_edges = []

    #This for loop sweeps a line over the workspace and finds the trapezoidal regions (Represented by the green lines)
    for x in range(env.x_max+1):
        for row in all_vertices:
            if row[0] == x:                 # This is an event
                poi_edge = []
                sweepline = [[x, env.y_min - 1], [x, env.y_max + 1]]
                for edge in all_edges:
                    if(x != 0):
                        if not (row[0] == edge[0][0] or row[0] == edge[1][0]):
                            if segments_intersect(sweepline[0],sweepline[1],edge[0],edge[1]):
                                poi_edge.append([point_of_intersection(do_edge_equation(sweepline),do_edge_equation(edge)),edge])
                index_of_event = 0
                if(len(poi_edge) > 1):
                    poi_edge = bubbleSort(poi_edge)
                for i,elem in enumerate(poi_edge):
                    if(elem[0][1] > row[1]):
                        index_of_event = i
                        break

                #Get the object for the obstacle
                obstacle_obj = None
                if row not in env.wallvertices_np:         # vertex belongs to an obstacle
                    for obstacle in obstacles:
                        if row in obstacle.vertices_np:
                            obstacle_obj = obstacle

                    if(len(poi_edge)) > 1:

                        #for vertices above event_vertex
                        if poi_edge[index_of_event][1] in obstacle_obj.edges_list:
                            if poi_edge[index_of_event+1][1] in obstacle_obj.edges_list:
                                trapezium_edges.append([row,poi_edge[index_of_event][0]])

                        else:
                            trapezium_edges.append([row, poi_edge[index_of_event][0]])

                        #for vertices below event vertex
                        if poi_edge[index_of_event-1][1] in obstacle_obj.edges_list:
                            if poi_edge[index_of_event - 2][1] in obstacle_obj.edges_list:
                                trapezium_edges.append([row, poi_edge[index_of_event][0]])

                        else:
                            trapezium_edges.append([row, poi_edge[index_of_event-1][0]])

                    if(len(poi_edge) == 1):
                        # Code for adding the edge to graph
                        trapezium_edges.append([row,poi_edge[0][0]])

                else:                       #vertex belongs to boundary
                    if(len(poi_edge) != 0):
                        if(index_of_event == 0):
                            trapezium_edges.append([row,poi_edge[index_of_event][0]])
                        else:
                            trapezium_edges.append(([row,poi_edge[index_of_event-1][0]]))
    for edge in trapezium_edges:
        for point in edge:
            if(math.ceil(point[0])-point[0] < 0.1):
                point[0] = float(math.ceil(point[0]))

    graph_points = {}
    for i in range(len(trapezium_edges)):
        edge = trapezium_edges[i]
        mid_x = (edge[0][0] + edge[1][0]) / 2
        mid_y = (edge[0][1] + edge[1][1]) / 2
        graph_points[i] = [mid_x,mid_y]

    # for finding connectivity graph sweep line again
    row = []
    for i in range(len(graph_points)):
        row.append(0.0)
    connectivity_graph = []
    for i in range(len(graph_points)):
        connectivity_graph.append(row)

    x = graph_points[0][0]
    connectivity_graph_edges = []
    previous_graph_points = []
    while x <= graph_points[len(graph_points)-1][0]:

        for row in all_vertices:
            if row[0] == x:                 # This is an event

                if(x == graph_points[0][0]):                # Do nothing if sweep line is at first graph point
                    for i in range(len(graph_points)):
                        if graph_points[i][0] == x:
                            previous_graph_points.append(graph_points[i])
                    break

                else:
                    #Code for obstacle edges goes here
                    current_graph_points = []
                    for i in range(len(graph_points)):
                        if(graph_points[i][0] == x):                                #Check if point in connectivity graph is at sweep line location
                            for point in previous_graph_points:
                                flag = 0
                                for obs_edge in obstacle_edges:
                                    if(segments_intersect(point,graph_points[i],obs_edge[0],obs_edge[1]) == True):
                                        # add that segment connecting point and graph_points[i] in the graph
                                        flag = 1
                                        break
                                for edge in trapezium_edges:
                                    if not (edge[0][0] == point[0]  or edge[0][0] == x):
                                        if (segments_intersect(point, graph_points[i], edge[0], edge[1]) == True):
                                            # add that segment connecting point and graph_points[i] in the graph
                                            flag = 1
                                            break
                                if(flag == 0):
                                    connectivity_graph_edges.append([point, graph_points[i]])
                                    flag2 = 0
                                    for point1 in current_graph_points:
                                        if point1 == graph_points[i]:
                                            flag2 = 1
                                            break
                                    if flag2 == 0:
                                        current_graph_points.append(graph_points[i])

                    for point in current_graph_points:
                        previous_graph_points.append(point)
                    for i in range(len(graph_points)):
                        if graph_points[i][0] == x:
                            repeat_flag = 0
                            for point in previous_graph_points:
                                if point[1] == graph_points[i][1]:
                                    repeat_flag = 1
                            if repeat_flag == 0:
                                previous_graph_points.append(graph_points[i])

        x += 1.0

    conn = np.zeros([len(graph_points),len(graph_points)])
    for edge in connectivity_graph_edges:
        x1 = 0
        x2 = 0
        for i in range(len(graph_points)):

            if edge[0] == graph_points[i]:
                x1 = i
            if edge[1] == graph_points[i]:
                x2 = i
        distance = euclidean(edge[0],edge[1])
        conn[x1,x2]  = distance

    #Following code computes the shortest path in the connectivity graph from the start to the goal
    graph = constructGraph()
    for node in range(len(graph_points)):
        graph.add_vertex(node)

    for i in range(len(conn)):
        for j in range(len(conn)):
            if conn[i,j] != 0:
                graph.add_edge(i, j, conn[i][j])

    start  = [1,0]                  # Edit the start point of the robot here
    end = [6.5,0]                   # edit the end point (goal) of the robot here

    # For calculating the closest point from the connectivity graph from the start and end points respectively. Then the Dijkstra's function is called to get the shortest path from the connectivity graph built.
    closest_from_start = 0
    closest_from_end = 0
    closest = 999.0
    for i in range(len(graph_points)):
        if (closest > euclidean(start,graph_points[i])):
            intersect_flag = 0
            for edge in obstacle_edges:
                if segments_intersect(edge[0],edge[1],start,graph_points[i]):
                    intersect_flag = 1
                    break
            if intersect_flag == 0:
                closest = euclidean(start,graph_points[i])
                closest_from_start = i
    closest = 999.0
    for i in range(len(graph_points)):
        if closest > euclidean(end, graph_points[i]):
            intersect_flag = 0
            for edge in obstacle_edges:
                if segments_intersect(edge[0], edge[1], end, graph_points[i]):
                    intersect_flag = 1
                    break
            if intersect_flag == 0:
                closest = euclidean(end, graph_points[i])
                closest_from_end = i

    # Call to the shortest path (Dijkstra) function
    path = shortest_path(graph, closest_from_start, closest_from_end, 0)
    roadmap = [start]
    for point in path:
        roadmap.append(graph_points[point])
    roadmap.append(end)
    # Function call to graphics module
    render(env,obstacles,trapezium_edges,graph_points,connectivity_graph_edges,roadmap)

if __name__ == "__main__":
    main()