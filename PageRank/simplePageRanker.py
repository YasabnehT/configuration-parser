from bs4 import BeautifulSoup
import os

from collections import defaultdict


#Parse httml files
def parse_html_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')

    # extract anchor links
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links


#Build the graph
def build_graph(directory):
    graph = defaultdict(list)

    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            links = parse_html_file(file_path)
            page = os.path.basename(file_path)
            graph[page] = links
    return graph

#PageRank Implementation
def pagerank(graph, iterations=100, damping_factor=0.85):
    new_ranks = {page:1/len(graph) for page in graph}

    for _ in range(iterations):
        new_rank = {}
        for page in graph:
            incoming_links = [p for p, links in graph.items() if page in links]
            new_rank = (1-damping_factor)/len(graph)
            new_rank += damping_factor *sum(ranks[p]/len(graph[p]) for p in incoming_links)
            new_ranks[page] = new_rank
        ranks = new_ranks
    return ranks
    
# #Parsing html files
# file_path = '/workspaces/configuration-parser/PageRank/Andela.html'
# links = parse_html_file(file_path)
# print(f'Links found: {links}')

#Build the graph
directory = '/workspaces/configuration-parser/PageRank/html_files'
graph = build_graph(directory)
# print(f'Graph: {graph}')

#PageRank Implementation
ranks = pagerank(graph)
most_popular = max(ranks, key=ranks.get)
print(f'Most popular page: {most_popular} with rank {ranks[most_popular]}')