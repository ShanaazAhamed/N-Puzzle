import sys

def read_from_txt(n,start,goal):
    start_list = []
    goal_list = []
    with open(start,"r") as start_config:
        for i in range(n):
            row = []
            #split by tab space
            for j in start_config.readline().strip().split('\t'):
                row.append(j)    
            start_list.append(row)

    with open(goal,"r") as goal_config:
        for i in range(n):
            row = []
            #split by tab space
            for j in goal_config.readline().strip().split('\t'):
                row.append(j)    
            goal_list.append(row)             
    
    return start_list,goal_list

def node(state,g,f,parent,direction):
    first_node = []
    temp_list =  [state,g,f,parent,direction]
    first_node.extend(temp_list)
    return first_node

def find_h_value(n,start,goal):
    h = 0
    for i in range(n):
        for j in range(n):
            if (start[i][j] != '-') and (start[i][j] != goal[i][j]):
                h +=1
    return h

def calculate_manhattan_distance(n,start,goal):
    
    def distance(value, a, b):
        for k in range(n):
            for l in range(n):
                if value == goal[k][l]:
                    return abs(k-a) + abs(l-b)
    total_dist = 0

    for i in range(n):
        for j in range(n):
            total_dist += distance(start[i][j],i,j)
    
    return total_dist

def find_misplaced_count(n,start,goal):
    count = 0
    for i in range(len(start)):
        for j in range(n):
            if start[i][j] != goal[i][j]:
                if start[i][j] != "-":
                    count +=1
    return count

def find_blank_space(state):
    bs_count = 0
    List = []
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == '-':
                List.append(i)
                List.append(j)
                bs_count += 1
                if (bs_count == 2):
                    return List[0], List[1], List[2], List[3]    

def move_blank_space(state, x1, y1, x2, y2):
    def copy():
        temp_list = []
        for i in state:
            temp = []
            for j in i:
                temp.append(j)
            temp_list.append(temp)
        return temp_list

    if (x2 < len(state) and x2 >= 0 and  y2 >= 0 and y2 < len(state) and x2 != "-" and y2 != "-"):
        new = []
        new = copy()
        temp = new[x2][y2]
        new[x2][y2] = new[x1][y1]
        new[x1][y1] = temp
        return new
    else:
        return None

def find_child_node(parent_node):
    children = []
    x1, y1, x2, y2 = find_blank_space(parent_node[0])  
    list1 = [[x1, y1-1, 'right'], [x1, y1+1, 'left'], [x1-1,
                                                           y1, 'down'], [x1+1, y1, 'up']]
    list2 = [[x2, y2-1, 'right'], [x2, y2+1, 'left'],
                 [x2-1, y2, 'down'], [x2+1, y2, 'up']]
    for val in list1:
        child = move_blank_space(parent_node[0], x1, y1, val[0], val[1])
        if child is not None:
            node1 = node(child, parent_node[1] + 1, 0, parent_node, [parent_node[0][val[0]][val[1]], val[2]])
            children.append(node1)

    for val in list2:
        child = move_blank_space(parent_node[0], x2, y2, val[0], val[1])
        if child is not None:
            node2 = node(child, parent_node[1] + 1, 0, parent_node, [parent_node[0][val[0]][val[1]], val[2]])
            children.append(node2)
    return children

def process(n,start,goal,user_input):
    opened_list,closed_list = [],[]
    count = 0
    opened_list.append(node(start, 0, 0, None, None))
    while True:
        current_node = opened_list[0]
        # print(current_node)
        h = find_h_value(n,current_node[0],goal)
        if (h == 0):
            rev_node = current_node
            moves = []
            while(rev_node[3] != None):
                moves.append(rev_node[4])
                rev_node = rev_node[3]
            moves.reverse()

            with open("output.txt","w") as output:
                data_list =[]
                for i in moves:
                    val = f"({i[0]},{i[1]})"
                    data_list.append(val)
                data = ",".join(data_list)
                output.write(data)
                output.write("\n")
            
            break

        children = find_child_node(current_node)
        valid = True

        for i in children:
            duplicate = False
            if user_input == 1:
                i[2] = i[1]+find_misplaced_count(n,i[0], goal)
            elif user_input == 2:
                i[2] = i[1]+calculate_manhattan_distance(n,i[0], goal)
            else:
                valid = False
                break
            for j in closed_list:
                if(j[0] == i[0]):
                    duplicate = True
                    break
            if(not(duplicate)):
                opened_list.append(i)
        if valid:
            closed_list.append(current_node)
            del opened_list[0]
            opened_list.sort(key=lambda x: x[2], reverse=False)
        else:
            exit()

        count += 1
    return count    



if __name__ == "__main__":
    try:
        n = int(input("Input the size of the puzzle: "))
        start = sys.argv[1]
        goal = sys.argv[2]
        start,goal = read_from_txt(n,start,goal)
        print("Choose relevant heuristic :\n1. number of misplaced tiles\n2. total manhattan distance\n")
    # try:
        user_input = int(input("Enter your choice: "))
        # print(start_arr)
        if start == goal:
            print("Start & Goal configurations are same")
        else:
            if user_input == 1:
                process(n,start,goal,user_input)
            elif user_input ==2:
                process(n,start,goal,user_input)
            else:
                print("Invalid Input")
        # except TypeError:
        #     print("Invalid Input!")

    except IndentationError:
        print("Invalid Argument passed!")