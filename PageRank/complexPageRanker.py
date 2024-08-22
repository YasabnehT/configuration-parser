import numpy as np


def initialize_pagerank(nodes):
    
    """
    initialize the PageRank values to 1/N for each node
    """ 
    N = len(nodes)
    pagerank = {node:1.0/N for node in nodes}
    return pagerank

def build_transition_matrix(graph,nodes):
    """
    Build  a transition probability matrix for the graph
    """
    N = len(nodes)
    matrix = np.zeros((N,N))
    node_index = {node: i for i, node in enumerate(nodes)}

    for node in nodes:
        if len(graph[node]) == 0: #Handling dangling node, nodes with no out-links
            for other_node in nodes:
                matrix[node_index[node]][node_index[other_node]] = 1.0/N

        else:
            for neighbor in graph[node]:
                matrix[node_index[node]][node_index[neighbor]] = 1.0/len(graph[node])
    return matrix

def compute_pagerank(matrix, pagerank, dampling_factor=0.85, max_iterations=100, tolerance=1e-6):
    """
    Iteratively compute pagerank values
    """
    N = len(pagerank)
    pagerank_values = np.array(list(pagerank.values()))
    uniform_distribution = np.ones(N)/N

    for iteration in range(max_iterations):
        new_pagerank_values = dampling_factor * np.dot(matrix.T, pagerank_values) + (1-dampling_factor) * uniform_distribution

        #check for convergence
        if np.linalg.norm(new_pagerank_values-pagerank_values,1)<tolerance:
            print(f'Converged afrer {iteration+1} iterations')
            break
        
        pagerank_values = new_pagerank_values

    # update the dictionary with dinal pagerank values
    for i, node in enumerate(pagerank.keys()):
        pagerank[node] = pagerank_values[i]
    return pagerank

def normalize_pagerang(pagerank):
    """
    Normalize the PageRank values to ensure they sum to 1
    """
    total = sum(pagerank.values())
    for node in pagerank:
        pagerank[node]/= total
    return pagerank

def pagerank(graph, dampling_factor=0.85, max_iterations = 100, tolerance=1e-6):
    """
    calculate the pagerank of each node in the graph    
    """
    nodes = list(graph.keys())
    pagerank_values  = initialize_pagerank(nodes)
    transition_matrix = build_transition_matrix(graph, nodes)
    pagerank_values = compute_pagerank(transition_matrix, pagerank_values, dampling_factor, max_iterations, tolerance)
    pagerank_values = normalize_pagerang(pagerank_values)
    return pagerank_values

# Example
if __name__ == '__main__':
    graph = {
        'A':['B','C'],
        'B':['C'],
        'C':['A'],
        'D':['C'],
    }

pagerank_values = pagerank(graph)
for node,rank in pagerank_values.items():
    print(f'Node {node} has PageRank: {rank:.4f}')


