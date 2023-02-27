import networkx as nx
import matplotlib.pyplot as plt
# Create empty
G = nx.DiGraph()
# Add graph vertices
G.add_nodes_from([1, 2, 3, 4, 5, 6])
# Add graph edges
G.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6)])
# Print graph vertices and edges
print("Graph vertices: ", G.nodes())
print("Graph edges: ",G.edges())
# FInd shortest path from vertex 2 to vertex 6
p = nx.shortest_path(G, source=2, target=6)

print("Shortest path:", p)
# Draw the graph
nx.draw(G, with_labels=True, pos=nx.spectral_layout(G))
plt.show()