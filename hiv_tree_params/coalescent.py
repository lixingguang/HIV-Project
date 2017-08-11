#! /usr/bin/env python3
import argparse
from dendropy import TaxonNamespace
from dendropy.simulate import treesim

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--population', required=True, type=int, help="Population Size")
    parser.add_argument('-n', '--num_leaves', required=True, type=int, help="Number of Leaves")
    args = parser.parse_args()
    assert args.num_leaves > 1, "Must have at least 2 leaves"
    print(treesim.pure_kingman_tree(TaxonNamespace([str(i) for i in range(args.num_leaves)]), pop_size=args.population).as_string(schema='newick'))
