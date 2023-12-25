import time
import networkx
import itertools

start_time = time.time()
file_path = 'input.txt'

with open(file_path, 'r') as file:
    seen_components = set()
    graph = networkx.Graph()
    edges = []
    for line in file:
        line = line.strip()
        line = line.replace(':', '')
        line = line.split(' ')
        start_component = line[0]
        if start_component not in seen_components:
            graph.add_node(start_component)
            seen_components.add(start_component)

        for node in line[1:]:
            if node not in seen_components:
                graph.add_node(node)
                seen_components.add(node)

            graph.add_edge(start_component, node)
            edges.append((start_component, node))
            print(f'\t"{start_component}" -> "{node}"')

# Copy the output into graph.dot
# Run dot -Tsvg .\graph.dot > graph.html
# Look at the graph for the 3 lines that split it
# Place the values below
# cut = [("sfm", "vmt"), ("vph", "mfc"), ("rmg", "fql")]

# Or if you've got time...
cut = networkx.minimum_edge_cut(graph)
sub_graphs = list(networkx.connected_components(graph))
if len(sub_graphs) == 2:
    print(f'found them: {len(sub_graphs[0]) * len(sub_graphs[1])}')

for edge in cut:
    graph.remove_edge(edge[0], edge[1])

sub_graphs = list(networkx.connected_components(graph))
print(f'found them: {len(sub_graphs[0]) * len(sub_graphs[1])}')
print(f'Took {time.time() - start_time} seconds')