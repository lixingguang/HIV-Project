#! /usr/bin/env python3
import argparse
from dendropy.simulate import treesim

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--birth', required=True, type=float, help="Birth Rate")
    parser.add_argument('-d', '--death', required=True, type=float, help="Death Rate")
    parser.add_argument('-n', '--num_leaves', required=True, type=int, help="Number of Leaves")
    args = parser.parse_args()
    assert args.birth >= 0, "Birth rate must be at least 0"
    assert args.death >= 0, "Death rate must be at least 0"
    assert args.num_leaves > 1, "Must have at least 2 leaves"
    print(treesim.birth_death_tree(birth_rate=args.birth, death_rate=args.death, ntax=args.num_leaves).as_string(schema='newick'))
