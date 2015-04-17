from graph_tool.topology import shortest_distance
import wordsgraph

def word(graph, vertex):
  return graph.vprop_word_string[vertex]

def distances(wordsgraph): 
  return shortest_distance(wordsgraph.graph, dense=True)

def find_distant_word_pairs(graph, distances, distance):
  print("finding most distant pairs")
  pairs = []
  for vertex in graph.graph.vertices():
    dists_v = distances[vertex].a #distanzen für ein wort
    for index, value in enumerate(dists_v):
      if value == distance:
        pair = (word(graph, vertex), word(graph, graph.graph.vertex(index)))
        print(pair)
        pairs.append(pair)
  return pairs
# graph.vprop_word_string[graph.graph.vertex(nr)] # wort
# distances[graph.graph.vertex(nr)] # liste zu dem vertex
