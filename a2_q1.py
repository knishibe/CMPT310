import random

def rand_graph(p, n):
    
    connected = [[] for i in range(n)]
    graph = {}
    random.seed()

    for i in range(n):
        for j in range(n):
            r = random.randint(0, 100);
            if(j > i and r < p*100):
                connected[i].append(j)
                connected[j].append(i)

    for i in range(0, n-1):
        graph.update({str(i) : connected[i]})

    return graph

print(rand_graph(0.5, 4))
