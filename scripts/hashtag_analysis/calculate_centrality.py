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
    
def calculate_closeness_centrality(graph, hashtag):
    start = time.time()
    print("Calculating closeness centrality...")
    closeness_centrality_scores = []
    step = graph.GetNodes()/10
    counter = 0
    for node in graph.Nodes():
        score = snap.GetClosenessCentr(graph, node.GetId())
        if score == 0:
            continue
        closeness_centrality_scores.append((node.GetId(), score))
        counter+=1
        if counter % step == 0:
            print("Progress: %d nodes" %counter)
    print("Saving results to file...")
    with open(hashtag+"_closeness_centrality.csv", "w") as fout:
        fout.write("Node,Closeness Centrality\n")
        for el in closeness_centrality_scores:
            fout.write(",".join([str(el[0]), str(el[1])])+"\n")
    end = time.time()
    print("Completed in: %s" % timedelta(seconds=(int(end-start))))

def calculate_eigenvector_centrality(graph, hashtag):
    start = time.time()
    print("Calculating eigenvector centrality...")
    NIdEigenH = snap.TIntFltH()
    snap.GetEigenVectorCentr(graph, NIdEigenH)
    print("Saving results to file...")
    with open(hashtag+"_eigenvector_centrality.csv", "w") as fout:
        fout.write("Node,Eigenvector Centrality\n")
        for item in NIdEigenH:
            fout.write(",".join([str(item), str(NIdEigenH[item])])+"\n")
    end = time.time()
    print("Completed in: %s" % timedelta(seconds=(int(end-start))))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Must specify hashtag and centrality type (1==betwenness, 2==closeness, 3==eigenvector)")
        sys.exit(1)
    hashtag = sys.argv[1]
    what = int(sys.argv[2])

    # Import the hashtag subgraph to work on
    FIn = snap.TFIn("../../data/mmr_subgraph_"+hashtag+".bin")
    hashtag_subgraph = TUNGraph.Load(FIn)

    # Get max connected component
    hashtag_subgraph = snap.GetMxScc(hashtag_subgraph)

    # Start computation
    if what == 1:
        calculate_betweenness_centrality(hashtag_subgraph, hashtag)
    elif what == 2:
        calculate_closeness_centrality(hashtag_subgraph, hashtag)
    elif what == 3:
        calculate_eigenvector_centrality(hashtag_subgraph, hashtag)
