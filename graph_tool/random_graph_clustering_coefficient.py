from graph_tool.generation import random_graph
import graph_parser
import graph_tool


def filter_main_component(graph):
    main_component = graph_tool.topology.label_largest_component(graph.graph)
    graph.graph.set_vertex_filter(main_component)
    graph.graph.purge_vertices()
    
filepath = "../data/cooc_denews10k.csv"

graph = graph_parser.file_to_graph(filepath)
filter_main_component(graph)


vertex_degrees = [v.in_degree() + v.out_degree() for v in graph.graph.vertices()]

def deg_sampler():
    return vertex_degrees.pop()

r_graph = random_graph(len(vertex_degrees), deg_sampler, directed=False)
print(graph_tool.clustering.global_clustering(r_graph))

# cooc_wiki_sim: (0.04836508152618817, 0.0064730643181345245)
# cooc_wiki_en:  (0.04906310588836009, 0.004693714628953113)
# cooc_nl:       (0.06654082373918595, 0.0029182368420710997)
# cooc_denews10k:(0.0690792859801145, 0.006716156468309491)

