
import heapq as Q
#importing the queue data structure to store the unvisited neighbouring nodes in variable open_node

def convert_number(source):


#converting the map matrix into a cost matrix
    int_matrix = source
    for i in range(0, len(source)):
        for j in range(0, len(source)):
            if int_matrix[i][j] == 'p':
                int_matrix[i][j] = 10
            elif int_matrix[i][j] == 's':
                int_matrix[i][j] = 30
            elif int_matrix[i][j] == 'm':
                int_matrix[i][j] = 100
            else:
                break

    return int_matrix



def path_route(int_matrix, goal):
    # prints the path taken, compares the co-ordinates with its previous step and checks the direction
    # if the x of current node is less than the next taken node then it prints out that it has traversed East

     if int_matrix.index(int_matrix[0][0]) < goal.index(goal[0]):
        print("E")

     elif int_matrix[0][0] > goal[0]:
        print("w")

     elif int_matrix[1][0] > goal[1]:
        print("N")

     elif int_matrix[1][0] < goal[1]:
        print("S")

def return_direction(start, end):
    x, y = start
    if (x, y+1) == end:
        return "E"
    elif (x, y-1) == end:
        return "W"
    elif (x+1, y) == end:
        return "S"
    elif (x-1, y) == end:
        return "N"
    else:
        return "D"




def heuristic_fun(source, dest):
# the heuristic is a manhattan distance from the start state to the goal state

    num_steps = abs((abs(source[0] - dest[0])) + (abs(source[1] - dest[1]))) # abs seperate
    return num_steps


def is_valid_index(idx, rows, cols):

    x = idx[0]
    y = idx[1]
    if x < 0 or x >= rows:
        return False
    if y < 0 or y >= cols:
        return False
    return True

def neighbour_nodes(matrix, node):
# generates the neighbouring nodes of the current selected node. Avoided cases like taking negative nodes
    rows = len(matrix)
    cols = len(matrix[0])
    x = node[1][0]
    y = node[1][1]
    left = (x, y-1)
    right = (x, y+1)
    up = (x+1, y)
    down = (x-1, y)
    valid_indexs = []
    if is_valid_index(left, rows, cols):
        valid_indexs.append(left)
    if is_valid_index(right, rows, cols):
        valid_indexs.append(right)
    if is_valid_index(up, rows, cols):
        valid_indexs.append(up)
    if is_valid_index(down, rows, cols):
        valid_indexs.append(down)

    return valid_indexs


def lowest(open_node):
# The function returns the lowest value in the open node
    k = Q.heappop(open_node)

    return k


def check_in_heap(heap, nbr):
    for i, ele in enumerate(heap):
        if ele[1] == nbr:
            return True, i
    return False, -1

def give_parent(closed_nodes, node):
    for ele in closed_nodes:
        if ele[1] == node:
            return ele[2]
    return node

def get_path(closed_nodes, start, goal):
    result = []
    result.append(goal)
    parent_node = give_parent(closed_nodes, goal)
    while parent_node != start:
        result.append(parent_node)
        parent_node = give_parent(closed_nodes, parent_node)
    result.append(parent_node)
    result = result[::-1]


    final_path = ""
    for i in range(0, len(result)-1):
        final_path = final_path + return_direction(result[i], result[i+1])
    return final_path




def a_star(start, goal, source):
#initialising the f(n), g(n), closed_node and open_nodes
#closed node to store the list of nodes already visited, open node is a list who have not yet been visited

    closed_node = []
    another_parent_node = []
    open_node = []
    source_tuple = (0, start, ("parent", ))
    Q.heappush(open_node, source_tuple)
    f_fun = {}
    g_fun = convert_number(source)
    f_fun[start] = g_fun[start[0]][start[1]] + heuristic_fun(start, goal)
    reference = {}
    reference[start] = source_tuple
    #once the all the nodes have been visited exit the loop
    while open_node != 0:

        #taking the lowest neighbour as current node

        current_node = lowest(open_node)
        closed_node.append(current_node)
        if current_node[1] == (2,0):
            pass
        if current_node[1] == goal:
            return get_path(closed_node, start, goal)
            #return path_route(source, goal)
        for nbr in neighbour_nodes(source, current_node):

            has, index = check_in_heap(open_node, nbr)
            has_closed, index_closed = check_in_heap(closed_node, nbr)
            if has:
                existing_node = open_node[index]
                open_node[index] = open_node[-1]
                open_node.pop()
                Q.heapify(open_node)
                # confusion wether to take current_node or nbr
                try:
                    temp = current_node[0]+g_fun[nbr[0]][nbr[1]] + heuristic_fun(nbr, goal)
                except IndexError as e:
                    raise e
                if temp < existing_node[0]:
                    new_node = (temp, nbr, current_node[1])
                    Q.heappush(open_node, new_node)
                else:
                    Q.heappush(open_node, existing_node)


            elif has_closed:
                continue
            else:

                temp = current_node[0] + g_fun[nbr[0]][nbr[1]] + heuristic_fun(nbr, goal)
                Q.heappush(open_node, (temp, nbr, current_node[1]))
                f_fun[nbr] = g_fun[current_node[1][0]][current_node[1][1]] + heuristic_fun(current_node[1], nbr) + g_fun[nbr[0]][nbr[1]]
    return closed_node



closed_node = a_star((2,2),(0,0),[['m', 'm', 'm', 's'], ['m', 'm', 'm', 's'], ['m', 'm', 'm', 's'], ['p', 'p', 'p', 'p']])

print(closed_node)

