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
    calculate_shortest_path_lengths_distribution(hashtag_subgraph, hashtag)
