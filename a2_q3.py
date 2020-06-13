from csp import *
from a2_q2 import *
from a2_q1 import *
import time

# create sub class to override unassign function
class CSP_Derived(CSP):
    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(variables, domains, neighbors, constraints)
        self.n_unassigns = 0

    # override unassign function to keep track of number of unassigned variables
    # modified from csp.py
    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            self.n_unassigns += 1
            del assignment[var]

# modifed to return object of derived class type
def MapColoringCSP_modified(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    graph = {}
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP_Derived(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)


def run_q3():

    f2 = open('q3.csv', 'w')

    # repeat 5 times to obtain 30 different solutions
    for k in range(5):

        graphs = []
        edge_counts = []

        # create 6 instances of random graphs with different probabilities (0.1 to 0.6)
        for i in range(6):
            graph, edges = rand_graph((i+1)/10, 31)
            graphs.append(graph)
            edge_counts.append(edges)
           
        for i in range(6):
            teams = [0]

            # start timer
            startTime = time.time()

            # start with 1 team and increase if unsolveable
            for j in range(31):
                
                # initialize csp problem
                csp = MapColoringCSP_modified(teams, graphs[i])

                # run arc consistancy algorithm to decrease the search 
                # space or reject unsolvable problems (ie only 1 team if 
                # at least one person has a friend)
                is_sol = AC3(csp)
                if  is_sol[0] == False:
                    teams.append(j+1)
                    continue

                # run backtracking algorithm and reject if no solution
                sol = backtracking_search(csp, mrv, lcv, forward_checking) 
                if sol is None:
                    teams.append(j+1)
                else:
                    # if the solution has been found, stop timer, 
                    # double check with check_teams() function,
                    # and print information to console
                    endTime = time.time()
                    print("Correct Solution: " + str(check_teams(graphs[i], sol)))
                    print("Number of Teams: %d" %len(teams))
                    print("Number of Assigns: %d" %csp.nassigns)
                    print("Number of Unassigns: %d" %csp.n_unassigns)
                    print("Number of Edges in Graph: %d" %edge_counts[i])
                    print("Time elapsed: " + str(endTime - startTime) + "\n")

                    # write data to .csv file for analysis
                    f2.write("%d;" %len(teams))
                    f2.write("%d;" %csp.nassigns)
                    f2.write("%d;" %csp.n_unassigns)
                    f2.write("%d;" %edge_counts[i])
                    f2.write(str(endTime - startTime))
                    f2.write("\n")
                    break

        f2.write("\n\n")

    f2.close()

run_q3()

    
