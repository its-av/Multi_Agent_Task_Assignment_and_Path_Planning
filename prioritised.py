import time as timer
from path_astar_one import compute_heuristics, a_star, get_sum_of_cost

class PrioritizedPlanningSolver(object):
    def __init__(self, my_map, starts, goals):
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.CPU_time = 0
        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""
        start_time = timer.time()
        result = []
        constraints = []
        agent_priorities = range(self.num_of_agents)  # Linear ordering
        for ind,i in enumerate(agent_priorities):  # Find path for each agent          
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)
            for j in range(ind+1,len(agent_priorities)):
                agent = agent_priorities[j]
                for timestep in range(len(path)-1):
                    curr_loc = path[timestep]
                    next_loc = path[timestep + 1]
                    constraints.append({'agent': agent, 'loc': [curr_loc],
                                        'timestep': timestep,
                                        'type': 'vertex'})
                    constraints.append({'agent': agent, 'loc': [next_loc, curr_loc],
                                        'timestep': timestep + 1,
                                        'type': 'edge'})
                constraints.append({'agent': agent, 'loc': path[-1],
                                    'timestep': len(path)-1,
                                    'type': 'inf'})
        return result
