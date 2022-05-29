from copy import deepcopy
from cbs import CBSSolver
#from prioritized import PrioritizedPlanningSolver
from visualize import Animation
from single_agent_planner import get_sum_of_cost, path
import itertools
import heapq

def min_cost_task_assn(starts,tasks):
    _tasks = list(itertools.permutations(tasks))
    _len = len(starts)
    starts_set=[]
    tasks_set=[]
    for t in _tasks:
        starts_set.append(starts)
        tasks_set.append(list(t))
    paths_with_cost = []
    for i, j in zip(starts_set, tasks_set):
        cbs = CBSSolver(my_map, i, j)
        _paths = cbs.find_solution(True, CBSSolver.NORMAL)
        _cost = get_sum_of_cost(_paths)
        paths_with_cost.append((_paths, _cost))
    _min_path = min(paths_with_cost, key=lambda x: x[1])
    return _min_path[0],_min_path[1]

def read_input(filename):
    f = open(filename, 'r')
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@' or cell == 'T':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    line = f.readline()
    num_agents = int(line)
    agent_loc=[]
    task_start=[]
    task_goal=[]
    print(num_agents)
    for a in range(num_agents):
        line=f.readline()
        sx, sy = [int(x) for x in line.split(' ')]
        agent_loc.append((sx,sy))
    line = f.readline()
    num_tasks = int(line)
    for a in range(num_tasks):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        task_start.append((sx,sy))
        task_goal.append((gx,gy))
    line = f.readline()
    aaa,ttt=[],[]
    if(int(line)>0):
        for i in range(int(line)):
            line = f.readline()
            x,y = [int(x) for x in line.split(' ')]
            aaa.append(x)
            ttt.append(y)
    f.close()
    return my_map,agent_loc,task_start,task_goal,aaa,ttt

print("Case 1: PickUp And Delivery of Single Task")
my_map, agent_loc,task_start, task_goal,a,t = read_input('test_1.txt')
print("Total Agents = {}".format(len(agent_loc)))
print("Total Tasks = {}".format(len(task_start)))
paths1,cost = min_cost_task_assn(agent_loc, task_start)
ttt=[]
for i in range(len(paths1)):
    ttt.append(paths1[i][-1])
cbs = CBSSolver(my_map, ttt, task_goal)
paths2 = cbs.find_solution(True, CBSSolver.NORMAL)
cost = get_sum_of_cost(paths2)
for i in range(len(paths2)):
    paths1[i]=paths1[i]+paths2[i]
print("***Test paths on a simulation***")
print('Tasks Completed')
animation = Animation(my_map, agent_loc, task_goal, paths1,task_start,task_goal)
animation.show()

print("Case 2: PickUp And Delivery Based on Weight of Task and Capacity of Agents")
my_map, agent_loc,task_start, task_goal,a,t = read_input('test_2.txt')
print("Total Agents = {}".format(len(agent_loc)))
print("Total Tasks = {}".format(len(task_start)))
prep_a=[]
for i in range(len(a)):
    prep_a.append((a[i],i))
prep_t=[]
for i in range(len(t)):
    prep_t.append((t[i],i))
heapq.heapify(prep_a)
heapq.heapify(prep_t)
fff,ggg,hhh=[],[],[]
for i in range(len(agent_loc)):
    zz=heapq.heappop(prep_a)
    yy=heapq.heappop(prep_t)
    if(zz[0]>=yy[0]):
        fff.append(agent_loc[zz[1]])
        ggg.append(task_start[yy[1]])
        hhh.append(task_goal[yy[1]])
    else:
        break
print("Total Tasks Allocated Based on Agent Capacity= {}".format(len(fff)))
paths1,cost = min_cost_task_assn(fff, ggg)
ttt=[]
for i in range(len(paths1)):
    ttt.append(paths1[i][-1])
cbs = CBSSolver(my_map, ggg, hhh)
paths2 = cbs.find_solution(True, CBSSolver.NORMAL)
cost = get_sum_of_cost(paths2)
for i in range(len(paths2)):
    paths1[i]=paths1[i]+paths2[i]
print("***Test paths on a simulation***")
print('Tasks Completed')
animation = Animation(my_map, fff, hhh, paths1,ggg,hhh)
animation.show()

print("Case 3: PickUp And Delivery of Multiple Task")
my_map, agent_loc,task_start, task_goal,a,t = read_input('test_3.txt')
print("Total Agents = {}".format(len(agent_loc)))
print("Total Tasks = {}".format(len(task_start)))
cbs = CBSSolver(my_map, agent_loc, task_start[:len(agent_loc)])
paths1 = cbs.find_solution(True, CBSSolver.NORMAL)
cbs = CBSSolver(my_map, task_start[:len(agent_loc)], task_goal[:len(agent_loc)])
paths2 = cbs.find_solution(True, CBSSolver.NORMAL)
cost = get_sum_of_cost(paths2)
for i in range(len(paths2)):
    paths1[i]=paths1[i]+paths2[i]
time=len(task_start)//len(agent_loc)-1
temp=paths1
while(time>0):
    time-=1
    st=task_goal[:len(agent_loc)]
    tar=task_start[len(agent_loc):]
    cbs = CBSSolver(my_map, st, tar)
    paths1 = cbs.find_solution(True, CBSSolver.NORMAL)
    cbs = CBSSolver(my_map,task_start[len(agent_loc):],task_goal[len(agent_loc):])
    paths2 = cbs.find_solution(True, CBSSolver.NORMAL)
    cost = get_sum_of_cost(paths2)
    for i in range(len(paths2)):
        paths1[i]=paths1[i]+paths2[i] 
for i in range(len(paths1)):
    temp[i]=temp[i]+paths1[i]
print("***Test paths on a simulation***")
print('Tasks Completed')
animation = Animation(my_map, agent_loc, task_goal[len(agent_loc):], temp,task_start,task_goal[:len(agent_loc)])
animation.show()

print("Case 4: Miscellaneous Warehouse")
my_map, agent_loc,task_start, task_goal,a,t = read_input('misc.txt')
print("Total Agents = {}".format(len(agent_loc)))
print("Total Tasks = {}".format(len(task_start)))
paths1,cost = min_cost_task_assn(agent_loc, task_start)
ttt=[]
for i in range(len(paths1)):
    ttt.append(paths1[i][-1])
cbs = CBSSolver(my_map, ttt, task_goal)
paths2 = cbs.find_solution(True, CBSSolver.NORMAL)
cost = get_sum_of_cost(paths2)
for i in range(len(paths2)):
    paths1[i]=paths1[i]+paths2[i]
print("***Test paths on a simulation***")
print('Tasks Completed')
animation = Animation(my_map, agent_loc, task_goal, paths1,task_start,task_goal)
animation.show()