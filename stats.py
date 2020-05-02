import json
import numpy as np
import argparse
from os.path import join

parser = argparse.ArgumentParser()
parser.add_argument('outputs_filename')
args = parser.parse_args()

PREV_OUTPUTS_FILENAME = join(args.outputs_filename, 'all_prev_outputs.txt')

with open(PREV_OUTPUTS_FILENAME, 'r') as f:
        data = json.load(f)
bests = [data[k]['best'] for k in data.keys()]
counts = [(b, bests.count(b)) for b in np.unique(bests)]
counts.sort(key=lambda pair: pair[1], reverse=True)
print(counts)

