from csp import *
from a2_q2 import *
from a2_q1 import *

graphs = [rand_graph(0.1, 31), rand_graph(0.2, 31), rand_graph(0.3, 31),
          rand_graph(0.4, 31), rand_graph(0.5, 31), rand_graph(0.6, 31)]
teams = [str(i) for i in range(31)]

for i in range(6):
    csp = MapColoringCSP(teams, graphs[0])
    AC3(csp)
    csp = backtracking_search(csp)