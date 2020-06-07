def check_teams(graph, csp_sol):

    i = 0

    for key, val in graph.items():
        team = csp_sol[key]
        for i in val:
            if team == csp_sol[str(i)]:
                return False

    return True

graph1 = {
    '0' : [1, 2],
    '1' : [0],
    '2' : [0],
    '3' : []
    }

graph2 = {
    '0' : 0,
    '1' : 1,
    '2' : 2,
    '3' : 1
    }

print(str(check_teams(graph1, graph2)))