#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from queue import LifoQueue
import numpy as np

Item = namedtuple('Item', ['i', 'v', 'w', 'd'])

Node = namedtuple('Node', ['ic', 'wl', 'sel', 'cv', 'oe'])


def calc_oe(items, cap):
    tot_w, tot_v = 0, 0
    for item in items:
        if item.w + tot_w <= cap:
            tot_w += item.w
            tot_v += item.v
        else:
            tot_v += (cap - tot_w) * (item.v / item.w)
            tot_w = cap
    return tot_v


def run_dfs(lines):

    N, W = [int(x) for x in lines[0].split()]
    tkn = [0 for i in range(N)]

    items = []

    for i in range(1, N+1):
        v, w = [int(x) for x in lines[i].split()]
        items.append(Item(i=i-1, v=v, w=w, d=v/w))

    items.sort(key=lambda x: x.d, reverse=True)
    # print(items)

    q = LifoQueue(0)
    q.put(Node(ic=0, wl=W, sel=[], cv=0, oe=calc_oe(items, W)))
    # print(Node(ic=0, wl=W, sel=[], cv=0, oe=calc_oe(items, W)))

    cnt = 0
    optimal = 1
    curr_best = 0
    sel_best = []

    while not q.empty():
        node = q.get()
        # print(node)

        # if cnt % 10000 == 0:
        #     print(cnt, node, curr_best)
        if cnt == 50000:
            optimal = 0
            break
        cnt += 1

        c_i = node.ic
        if c_i == N:
            if node.cv > curr_best:
                curr_best = node.cv
                sel_best = node.sel[:]
        else:
            drop = Node(ic=c_i+1,
                        wl=node.wl,
                        sel=node.sel[:],
                        cv=node.cv,
                        oe=calc_oe(items[c_i+1:], node.wl))
            if drop.wl >= 0 and drop.cv + drop.oe > curr_best:
                q.put(drop)

            pick = Node(ic=c_i+1,
                        wl=node.wl - items[c_i].w,
                        sel=node.sel[:] + [items[c_i].i],
                        cv=node.cv + items[c_i].v,
                        oe=calc_oe(items[c_i+1:], node.wl - items[c_i].w))
            if pick.wl >= 0 and pick.cv + pick.oe > curr_best:
                q.put(pick)

    for x in sel_best:
        tkn[x] = 1

    return curr_best, 0, tkn


def run_dp(lines):

    N, W = [int(x) for x in lines[0].split()]

    # stores array of values for each item
    vals = np.empty(N, dtype=np.int32)
    # stores array of weights for each item
    wts = np.empty(N, dtype=np.int32)
    # denotes wether item will be chosen in final selection or not
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

    return dp[N-1, W], 1, tkn


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    N, W = [int(x) for x in lines[0].split()]

    if (N * W) > 25_000_000:
        sol, opt, tkn = run_dfs(lines)
    else:
        sol, opt, tkn = run_dp(lines)

    # prepare the solution in the specified output format
    output_data = str(sol) + ' ' + str(opt) + '\n'
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
