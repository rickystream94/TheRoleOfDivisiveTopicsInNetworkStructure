from __future__ import print_function
import snap
from snap import TUNGraph
import time
from datetime import timedelta
import sys

def calculate_shortest_path_lengths_distribution(graph, hashtag):
    start = time.time()
    print("Calculating shortest path lengths distribution...")
    snap.PlotShortPathDistr(graph, hashtag+"_shortestPathLengthsDist", "Shortest Path Lengths Distribution")
    end = time.time()
    print("Completed in: %s" %timedelta(seconds=(int(end-start))))

def calculate_aspl_diameter(graph, hashtag):
    start = time.time()
    print("Calculating diameter and average shortest path length...")
    result = snap.GetBfsEffDiamAll(graph, graph.GetNodes(), False)
    end = time.time()
    print("Completed in: %s" %timedelta(seconds=(int(end-start))))
    filename = hashtag+"_aspl_diameter.txt"
    with open(filename,"w") as fout:
        fout.write("Effective Diameter 1: %f\nEffective Diameter 2: %f\nDiameter: %d\nAverage Shortest Path Length: %f\n" %(result[0], result[1],result[2],result[3]))
    print("Saved result to %s" %filename)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Must specify hashtag and what to calculate (1 == Avg Shortest Path Length + Diameter, 2 == Shortest Path Lengths Distribution")
        sys.exit(1)
    hashtag = sys.argv[1]
    what = int(sys.argv[2])

    # Import the hashtag subgraph to work on
    FIn = snap.TFIn("../../data/mmr_subgraph_"+hashtag+".bin")
    hashtag_subgraph = TUNGraph.Load(FIn)

    # Get max connected component
    hashtag_subgraph = snap.GetMxScc(hashtag_subgraph)

    # Start computation
    if(what == 1):
        # Avg Shortest Path Length + Diameter
        calculate_aspl_diameter(hashtag_subgraph, hashtag)
    elif(what == 2):
        calculate_shortest_path_lengths_distribution(hashtag_subgraph, hashtag)
