from __future__ import print_function
import snap
from snap import TUNGraph
import time
from datetime import timedelta
import sys


def calculate_betweenness_centrality(graph, hashtag):
    start = time.time()
    print("Calculating betweenness centrality...")
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(graph, Nodes, Edges, 1.0)
    print("Saving results to file...")
    with open(hashtag+"_betweenness_centrality_nodes.csv", "w") as fout:
        fout.write("Node,Betweenness Centrality\n")
        for node in Nodes:
            if Nodes[node] == 0:
                continue
            fout.write(",".join([str(node), str(Nodes[node])])+"\n")
    with open(hashtag+"_betweenness_centrality_edges.csv", "w") as fout:
        fout.write("Source,Target,Betweenness Centrality\n")
        for edge in Edges:
            if Edges[edge] == 0:
                continue
            fout.write(",".join([str(edge.GetVal1()), str(edge.GetVal2()), str(Edges[edge])])+"\n")
    end = time.time()
    print("Completed in: %s" % timedelta(seconds=(int(end-start))))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Must specify hashtag")
        sys.exit(1)
    hashtag = sys.argv[1]

    # Import the hashtag subgraph to work on
    FIn = snap.TFIn("../../data/mmr_subgraph_"+hashtag+".bin")
    hashtag_subgraph = TUNGraph.Load(FIn)

    # Get max connected component
    hashtag_subgraph = snap.GetMxScc(hashtag_subgraph)

    # Start computation
    calculate_betweenness_centrality(hashtag_subgraph, hashtag)
