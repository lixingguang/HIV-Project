#!/usr/bin/env python3
'''
Split the leaves of a given tree into the minimum number of clusters such that,
in each cluster, no pair of leaves is more than the given distance threshold
apart.
'''
from queue import Queue

# cut out the current node's subtree (by setting all nodes' DELETED to True) and return list of leaves
def cut(node):
    cluster = []
    descendants = Queue(); descendants.put(node)
    while not descendants.empty():
        descendant = descendants.get()
        if descendant.DELETED:
            continue
        descendant.DELETED = True
        if descendant.parent_node:
            parent_children = descendant.parent_node.child_nodes()
            if descendant == parent_children[0]:
                descendant.parent_node.left_dist = 0
            else:
                descendant.parent_node.right_dist = 0
        desc_children = descendant.child_nodes()
        if len(desc_children) == 0:
            cluster.append(descendant.taxon.label)
        else:
            for c in desc_children:
                descendants.put(c)
    return cluster

def min_clusters_threshold(tree,threshold):
    # check for validity and create all "dist" variables (distance to furthest leaf descendant)
    leaves = set()
    for node in tree.postorder_node_iter():
        node.DELETED = False
        child_nodes = node.child_nodes()
        assert len(child_nodes) in {0,2}, "ERROR: Multifurcating tree. Resolve polytomies first"
        if len(child_nodes) == 0:
            node.left_dist = 0; node.right_dist = 0; leaves.add(node.taxon.label)
        else:
            node.left_dist = max(child_nodes[0].left_dist,child_nodes[0].right_dist) + child_nodes[0].edge_length
            node.right_dist = max(child_nodes[1].left_dist,child_nodes[1].right_dist) + child_nodes[1].edge_length

    # perform algorithm
    clusters = []
    for node in tree.postorder_node_iter():
        # if I've already been handled, ignore me
        if node.DELETED:
            continue

        # check my true undeleted max distance to leaf
        dist = node.edge_length
        if dist is None:
            dist = 0
        child_nodes = node.child_nodes()
        if len(child_nodes) != 0:
            if not child_nodes[0].DELETED and not child_nodes[1].DELETED:
                dist += max(node.left_dist,node.right_dist)
            elif not child_nodes[0].DELETED:
                dist += node.left_dist; node.right_dist = 0
            elif not child_nodes[1].DELETED:
                dist += node.right_dist; node.left_dist = 0
        cluster = []

        # if my kids are screwing things up, cut out the longer one
        if node.left_dist + node.right_dist > threshold:
            if node.left_dist > node.right_dist:
                cluster = cut(child_nodes[0])
            else:
                cluster = cut(child_nodes[1])

        # if I'm screwing things up, cut me out
        elif dist > threshold:
            cluster = cut(node)

        # add cluster
        if len(cluster) != 0:
            clusters.append(cluster)
            for leaf in cluster:
                leaves.remove(leaf)

    # add all remaining leaves to a single cluster
    if len(leaves) != 0:
        clusters.append(list(leaves))
    return clusters

def parse_args():
    from sys import stdin
    import argparse
    import dendropy
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', required=False, type=argparse.FileType('r'), default=stdin, help="Input Tree File (default: stdin)")
    parser.add_argument('-t', '--threshold', required=True, type=float, help="Length Threshold")
    args = parser.parse_args()
    return [dendropy.Tree.get(data=line.strip(),schema='newick') for line in args.file.read().strip().splitlines()], args.threshold

if __name__ == "__main__":
    trees,threshold = parse_args()
    for tree in trees:
        clusters = min_clusters_threshold(tree,threshold)
        for cluster in clusters:
            print(cluster)
        print()