#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import heapq

from numpy import empty

Item = namedtuple('Item', ['i', 'v', 'w', 'd'])
# i -> index
# v -> value
# w -> weight
# d -> value density


class Node:
    def __init__(self, ic, wl, sel, cv, oe) -> None:
        self.ic = ic
        self.wl = wl
        self.sel = sel
        self.cv = cv
        self.oe = oe

    def __lt__(self, other):
        # return self.ic < other.ic  # breadth first search
        # return self.cv + self.oe < other.cv + other.oe  # min heap
        return self.cv + self.oe >= other.cv + other.oe  # max heap

    def __repr__(self) -> str:
        return f'Node(ic={self.ic}, wl={self.wl}, sel={self.sel}, cv={self.cv}, oe={self.oe})'


# Node = namedtuple('Node', ['ic', 'wl', 'sel', 'cv', 'oe'])
# ic -> items covered
# wl -> weight left
# sel -> selected indices
# cv -> current value
# oe -> optimistic estimate


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


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    N, W = [int(x) for x in lines[0].split()]
    tkn = [0 for i in range(N)]

    items = []

    for i in range(1, N+1):
        v, w = [int(x) for x in lines[i].split()]
        items.append(Item(i=i-1, v=v, w=w, d=v/w))

    items.sort(key=lambda x: x.d, reverse=True)
    # print(items)

    q = []
    heapq.heappush(q, Node(ic=0, wl=W, sel=[], cv=0, oe=calc_oe(items, W)))
    # print(Node(ic=0, wl=W, sel=[], cv=0, oe=calc_oe(items, W)))

    cnt = 0
    optimal = 1
    curr_best = 0
    sel_best = []

    while q:
        # print(q)
        node = heapq.heappop(q)
        # print(node)

        # if cnt % 10000 == 0:
        #     print(cnt, node, curr_best)
        if cnt == 1000000:
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
                heapq.heappush(q, drop)

            pick = Node(ic=c_i+1,
                        wl=node.wl - items[c_i].w,
                        sel=node.sel[:] + [items[c_i].i],
                        cv=node.cv + items[c_i].v,
                        oe=calc_oe(items[c_i+1:], node.wl - items[c_i].w))
            if pick.wl >= 0 and pick.cv + pick.oe > curr_best:
                heapq.heappush(q, pick)

    for x in sel_best:
        tkn[x] = 1

    print(cnt)

    # prepare the solution in the specified output format
    output_data = str(curr_best) + ' ' + str(optimal) + '\n'
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
