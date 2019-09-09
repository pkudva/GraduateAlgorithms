#Author: Priya Kudva
#CIS 621 Assignment 5
#Last Updated 6/2/18

import sys
import math


icost = []
irel = []
cost = []
rel = []
dict = {}
array = []
machines = {}
i_machines = []
counter = []


def main():
    arr = []
    file = sys.stdin
    j = 0
    for line in file:
        arr.append(line.rstrip('\n'))
        j += 1
    n = int(arr[1])
    budget = int(arr[0])
    file.close()
    dp = []
    for j in range(2, len(arr)):
        dp.append(arr[j].split())


    icost.append(1)
    irel.append(1)
    for c in dp:
        icost.append(int(c[0]))
        irel.append(float(c[1]))
        cost.append(int(c[0]))
        rel.append(float(c[1]))

    print("Budget: {}".format(budget))
    print("Number machines: {}".format(n))
    print("")
    print("Iterated Version: ")
    #iterative
    b = budget
    a, mach = i_rel(n, b)
    print("Maximum reliability: {}".format(a[n-1][b]))
    for i in range(n-1, -1, -1):
        print("{} copies of machine {} of cost {}".format(mach[i][b], i+1, icost[i+1]))
        b = b - (icost[i+1] * mach[i][b])

    print("")
    print("Memoized Version: ")

    #recursive
    counter.append(0)
    memo_rel(n - 1, budget)
    print_dict(dict, n-1, budget)
    print_machines(n, budget)

    print("")
    print("Memoization Statistics:")
    print("Total locations: {}".format(n*budget))
    print("Number used: {}".format(counter[0]))
    print("Percentage used: {}".format(float((counter[0]/(n*budget))*100)))


def i_rel(n, budget):
    for i in range(n):
        array.append([])
        i_machines.append([])
        for b in range(budget+1):
            array[i].append([0])
            i_machines[i].append([0])
            if b < 0:
                array[i][b] = 0
                i_machines[i][b] = 0
            elif b == 0 and i > 0:
                array[i][b] = 0
                i_machines[i][b] = 0
            elif b >= 0 and i == 0:
                x = math.floor(b/icost[i+1])
                array[i][b] = (1 - math.pow(1-irel[1], x))
                icost[0] = x
                i_machines[i][b] = x
            else:
                if b not in array:
                    max = 0
                    tempmachinemax = 0
                    r = int(math.floor(b / icost[i+1]) + 1)
                    for m in range(1, r):
                        max_i = array[i - 1][b - m * icost[i+1]] * (1 - math.pow(1 - irel[i+1], m))
                        if max <= max_i:
                            max = max_i
                            tempmachinemax = m
                    array[i][b] = max
                    i_machines[i][b] = tempmachinemax
    return array, i_machines


def memo_rel(i, budget):
    key = (i, budget)
    if budget < 0:
        machines[key] = 0
        return 0
    elif budget == 0 and i > -1:
        machines[key] = 0
        return 0
    elif budget >= 0 and i == -1:
        machines[key] = 1
        return 1
    else:
        # make a dictionary and check to see if the (i,budget) is already in dict
        if key not in dict:
            max_rel = 0
            tempmachinesmax = 0
            r = int(math.floor(budget / cost[i])+1)
            for m in range(1, r):
                max_i = memo_rel(i - 1, budget - (m * cost[i])) * (1 - math.pow(1 - rel[i], m))
                if max_rel <= max_i:
                    max_rel = max_i
                    tempmachinesmax = m
            dict[key] = max_rel
            machines[key] = tempmachinesmax
            counter[0] += 1
        return dict[key]


def print_dict(dictionary, i, b):
    key = (i, b)
    print("Maximum Reliability: {}".format(dictionary[key]))



def print_machines(n, b):
    for i in range(n-1, -1, -1):
        key = (i, b)
        print("{} copies of machine {} of cost {}".format(machines[key], i+1, cost[i]))
        b = b - cost[i] * machines[key]


if __name__ == "__main__":
    main()
