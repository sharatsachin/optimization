#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from collections import namedtuple
Item = namedtuple("Item", ['i', 'v', 'w'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    N = int(firstLine[0])
    W = int(firstLine[1])

    items = []

    for i in range(1, N+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    N = len(items)
    taken = [0 for i in range(N)]

    dp = [[0 for j in range(W+1)] for i in range(N)]
    for i in range(N):
        for j in range(W+1):
            if j-items[i].w >= 0:
                dp[i][j] = max(dp[i-1][j],
                               dp[i-1][j-items[i].w] + items[i].v)
            else:
                dp[i][j] = dp[i-1][j]

    # for row in dp: # DBG
    #     print(row)

    i, j = N-1, W
    while i >= 0 and j >= 0:
        # print(i, j, dp[i][j]) # DBG
        if dp[i][j] == dp[i-1][j]:
            i -= 1
        else:
            taken[i] = 1
            j -= items[i].w
            i -= 1

    # prepare the solution in the specified output format
    output_data = str(dp[N-1][W]) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
