import random
import re
import argparse
import concurrent.futures as cf

parser = argparse.ArgumentParser()
parser.add_argument('-r', type=float, default=0.0, help='ratio of missing items')
args = parser.parse_args()
RATIO = 1 - args.r

with open('./item_index2entity_id_ratio_1.00.txt') as fin:
    ALL_ITEMS = fin.readlines()

with open('item_index2entity_id_ratio_{:.2f}.txt'.format(RATIO), 'wt') as fout:
    fout.write("".join(sorted(ALL_ITEMS[:int(len(ALL_ITEMS)*(RATIO))])))
