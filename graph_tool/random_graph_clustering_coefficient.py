from graph_tool.generation import random_graph
import graph_parser
import graph_tool


def filter_main_component(graph):
    main_component = graph_tool.topology.label_largest_component(graph.graph)
    graph.graph.set_vertex_filter(main_component)
    graph.graph.purge_vertices()
    
filepath = "../data/cooc_wiki_sim.csv"

graph = graph_parser.file_to_graph(filepath)
graph.filter_cooccurrence_threshold(1/12)
filter_main_component(graph)


vertex_degrees = [v.in_degree() + v.out_degree() for v in graph.graph.vertices()]

def deg_sampler():
    return vertex_degrees.pop()

r_graph = random_graph(len(vertex_degrees), deg_sampler, directed=False)
print(graph_tool.clustering.global_clustering(r_graph))
