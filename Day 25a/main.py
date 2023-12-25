import time
import networkx

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

a = ("sfm", "vmt")
b = ("vph", "mfc")
c = ("rmg", "fql")

temp_graph = graph.copy()
temp_graph.remove_edge(a[0], a[1])
temp_graph.remove_edge(b[0], b[1])
temp_graph.remove_edge(c[0], c[1])

sub_graphs = list(networkx.connected_components(temp_graph))
if len(sub_graphs) == 2:
    print(f'found them: {len(sub_graphs[0]) * len(sub_graphs[1])}')

print(f'Took {time.time() - start_time} seconds')
