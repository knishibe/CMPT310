import random

def rand_graph(p, n):
    
    connected = [[] for i in range(n)]
    graph = {}
    random.seed()
    edges = 0

    for i in range(n):
        for j in range(n):
            r = random.randrange(100);

            # j > i to ensure no repeats
            # r < p*100 to ensure proper probability
            if(j > i and r < p*100):

                # make j a friend of i
                # and i a friend of j
                connected[i].append(j)
                connected[j].append(i)
                edges += 1

    # create graph
    for i in range(n):
        graph.update({i : connected[i]})

    # return the graph and the number of edges the graph has
    return graph, edges


