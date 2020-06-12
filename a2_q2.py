def check_teams(graph, csp_sol):

    i = 0

    for key, val in graph.items():
        team = csp_sol[key]

        # Check the teams of each person's friends
        for i in val:
            # if person key is on the same team as 
            # friend i, reject the solution
            if team == csp_sol[i]:
                return False

    # if the solution has not been rejected, it is
    # consistant and complete
    return True

#graph1 = {
#    '0' : [1, 2],
#    '1' : [0],
#    '2' : [0],
#    3' : []
#    }

#graph2 = {
#    '0' : 0,
#    '1' : 1,
#    '2' : 2,
#    '3' : 1
#    }

#print(str(check_teams(graph1, graph2)))