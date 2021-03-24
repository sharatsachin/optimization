#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    N, W = [int(x) for x in lines[0].split()]

    vals = np.empty(N, dtype=np.int32)
    wts = np.empty(N, dtype=np.int32)
    tkn = np.zeros(N, dtype=np.int8)

    for i in range(1, N+1):
        vals[i-1], wts[i-1] = [int(x) for x in lines[i].split()]

    dp = np.zeros((N, W+1), dtype=np.int64)
    for i in range(N):
        for j in range(W+1):
            if j-wts[i] >= 0:
                dp[i, j] = max(dp[i-1, j],
                               dp[i-1, j-wts[i]] + vals[i])
            else:
                dp[i, j] = dp[i-1, j]

    # for row in dp: # DBG
    #     print(row)

    i, j = N-1, W
    while i >= 0 and j >= 0:
        # print(i, j, dp[i,j]) # DBG
        if dp[i, j] == dp[i-1, j]:
            i -= 1
        else:
            tkn[i] = 1
            j -= wts[i]
            i -= 1

    # prepare the solution in the specified output format
    output_data = str(dp[N-1, W]) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, tkn))
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
