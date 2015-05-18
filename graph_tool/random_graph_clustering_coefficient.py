from graph_tool.generation import random_graph
import graph_parser
import graph_tool
import numpy as np


def filter_main_component(graph):
    main_component = graph_tool.topology.label_largest_component(graph.graph)
    graph.graph.set_vertex_filter(main_component)
    graph.graph.purge_vertices()

def calc_L(graph):
    counts, bins = graph_tool.stats.distance_histogram(graph,
        float_count= False)
    counts = np.append(counts, 0)
    return sum([ a*b for (a,b) in zip(counts,bins) ]) / (graph.num_vertices() * (graph.num_vertices()-1))

filepath = "../data/cooc_wiki_sim.csv"

graph = graph_parser.file_to_graph(filepath)
graph.filter_main_component()


vertex_degrees = [v.in_degree() + v.out_degree() for v in graph.graph.vertices()]

def deg_sampler():
    return vertex_degrees.pop()

r_graph = random_graph(len(vertex_degrees), deg_sampler, directed=False)
print("clusteringcoefficient")
print("C_random")
c_random = graph_tool.clustering.global_clustering(r_graph)
print(c_random)
print("C_original")
c_original = graph_tool.clustering.global_clustering(graph.graph)
print(c_original)
print("quotient")
print(c_original[0]/c_random[0])

print("average shortest path length")
l_random = calc_L(r_graph)
print("L_random")
print(l_random)
l_original = calc_L(graph.graph)
print("L_original")
print(l_original)
print("quotient")
print(l_original/l_random)
print("sigma")
sigma = (c_original[0] / c_random[0]) / (l_original / l_random)
print(sigma)

# cooc_wiki_sim: (0.04836508152618817, 0.0064730643181345245)
# cooc_wiki_en:  (0.04906310588836009, 0.004693714628953113)
# cooc_nl:       (0.06654082373918595, 0.0029182368420710997)
# cooc_denews10k:(0.0690792859801145, 0.006716156468309491)
