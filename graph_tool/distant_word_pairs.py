from graph_tool.topology import shortest_distance


def word(graph, vertex):
  return graph.vprop_word_string[vertex]

distances = shortest_distance(graph.graph, dense=True)

def find_most_distant_word_pairs(graph, distances, max_value):
  print("finding most distant pairs")
  pairs = []
  for vertex in graph.graph.vertices():
    dists_v = distances[vertex].a #distanzen für ein wort
    for index, value in enumerate(dists_v):
      if value == max_value:
        pair = (word(graph, vertex), word(graph, graph.graph.vertex(index)))
        print(pair)
        pairs.append(pair)
  return pairs
# graph.vprop_word_string[graph.graph.vertex(nr)] # wort
# distances[graph.graph.vertex(nr)] # liste zu dem vertex
