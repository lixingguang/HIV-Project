#! /usr/bin/env python3
'''
Niema Moshiri 2016

Subsample an input transmission network and determine the number of missing
links, where a "missing link" is defined as node that was not sampled itself,
but that was infected by a sampled node and infected a sampled node.

The script takes as input the transmission network, the contact network from
which it was simulated, the desired fraction of nodes to subsample, and the
desired number of subsampling iterations to perform. The networks can be in
plain-text or Gzipped, but they must be in the FAVITES formats.
'''

# return the set of nodes in the given contact network (FAVITES edge list)
def cn_nodes(cn):
    nodes = set()
    for line in cn:
        parts = line.split('\t')
        if parts[0] == 'NODE':
            nodes.add(parts[1])
    return nodes

# return "infected" and "infected_by" dicts from given transmission network (FAVITES format)
def infected_infectedby(tn):
    infected = {}    # infected[u]    = set of nodes infected by u
    infected_by = {} # infected_by[v] = node that infected v
    for line in tn:
        u,v,t = [i.strip() for i in line.split('\t')]
        if u not in infected:
            infected[u] = set()
        infected[u].add(v)
        infected_by[v] = u
    return infected,infected_by

# subsample "s" nodes from the input transmission network (tn) and count missing links once
def subsample_and_missing_links(cn, tn, s_over_n):
    from random import sample
    nodes = cn_nodes(cn)
    infected,infected_by = infected_infectedby(tn)
    infected_nodes = set()
    for u in infected:
        infected_nodes.add(u)
        infected_nodes.update(infected[u])
    s = int(s_over_n*len(infected_nodes))
    sampled_nodes = set(sample(infected_nodes, s))
    missing_nodes = infected_nodes - sampled_nodes
    missing_links = set()
    for v in sampled_nodes:
        if v in infected_by:
            u = infected_by[v]
            if u in infected_by and u in missing_nodes:
                missing_links.add(u)
    return len(missing_links)

# subsample "s_over_n" (fraction) nodes from the input transmission network (tn) and count missing links "it" times
def subsample_and_missing_links_it(cn, tn, s_over_n, it):
    out = []
    for i in range(it):
        print("Iteration " + str(i+1) + " of " + str(it) + "...")
        out.append(subsample_and_missing_links(cn,tn,s_over_n))
    return out

if __name__ == "__main__":
    import sys,gzip
    if len(sys.argv) != 5:
        if len(sys.argv) != 2 or sys.argv[1].strip() not in {'-h','--help'}:
            print("ERROR: Incorrect number of arguments")
        print("USAGE: python subsample_tn_count_missing_links.py <contact_network> <transmission_network> <s_over_n> <num_it>")
        exit(-1)
    gz = {'.gz','.GZ','.Gz'}
    if sys.argv[1].strip()[-3:] in gz:
        cn = [i.strip() for i in gzip.open(sys.argv[1].strip(), 'rt').read().strip().splitlines()]
    else:
        cn = [i.strip() for i in open(sys.argv[1].strip()).read().strip().splitlines()]
    if sys.argv[2].strip()[-3:] in gz:
        tn = [i.strip() for i in gzip.open(sys.argv[2].strip(), 'rt').read().strip().splitlines()]
    else:
        tn = [i.strip() for i in open(sys.argv[2].strip()).read().strip().splitlines()]
    s_over_n = float(sys.argv[3])
    it = int(sys.argv[4])
    print(','.join([str(i) for i in subsample_and_missing_links_it(cn,tn,s_over_n,it)]))