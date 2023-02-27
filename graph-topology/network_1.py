import networkx as nx
import matplotlib.pyplot as plt
# Create empty
G = nx.Graph()
# Add graph vertices
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
# Add graph edges
G.add_edge(1, 2)
G.add_edge(1, 5)
G.add_edge(2, 3)
G.add_edge(2, 5)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(4, 6)
# Print graph vertices and edges
print("Graph vertices: ", G.nodes())
print("Graph edges: ",G.edges())
# Draw the graph
nx.draw(G, with_labels=True, pos=nx.spectral_layout(G))
plt.show()