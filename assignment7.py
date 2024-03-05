# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 7 - Empirical Performance of Shortest Path Algorithms
# Sophia Balachanthiran

# Acknowledgements:
# I worked with
# Ridwan Ali
# Joel Joseph

# I used the following sites
# https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/


import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import time

INF = 999999


def random_graph(num_vertices, max_cost):
    cm = [[0] * num_vertices for i in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                cm[i][j] = INF
            else:
                cm[i][j] = random.randint(1, max_cost)
    return cm


def init_dist(matrix):
    dist = copy.deepcopy(matrix)
    n = len(dist)
    for i in range(n):
        dist[i][i] = 0
    return dist


def to_table(matrix):
    n = len(matrix)
    table = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < INF:
                table[i].append((j, matrix[i][j]))
    return table


def get_edges(matrix):
    edges = []
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            cost = matrix[i][j]
            if cost < INF:
                edges.append((i, j, cost))
    return edges


def floyd_apsp(matrix):
    n = len(matrix)
    dist = init_dist(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


def bellman_ford_apsp(matrix):
    edges = get_edges(matrix)
    n = len(matrix)
    dist = init_dist(matrix)
    for src in range(n):
        dist[src][src] = 0
        for i in range(n - 1):
            for u, v, w in edges:
                if dist[src][u] + w < dist[src][v]:
                    dist[src][v] = dist[src][u] + w
        for u, v, w in edges:
            if dist[src][u] + w < dist[src][v]:
                print('Graph contains negative weight cycle')
                return
    return dist


def find_min(keys, used):
    mn = INF
    mn_idx = -1
    for u in range(len(keys)):
        if keys[u] < mn and not used[u]:
            mn = keys[u]
            mn_idx = u
    return mn_idx


def dijkstra_apsp(matrix):
    n = len(matrix)
    dist = init_dist(matrix)
    for src in range(n):
        dist[src][src] = 0
        used = [False] * n
        for i in range(n):
            x = find_min(dist[src], used)
            used[x] = True
            for y in range(n):
                if not used[y] and dist[src][y] > dist[src][x] + matrix[x][y]:
                    dist[src][y] = dist[src][x] + matrix[x][y]
    return dist


def print_matrix(matrix):
    print(np.array(matrix))
    print('')


def print_table(table):
    n = len(table)
    for i in range(n):
        print(i, table[i])


def mini_test():
    n = 10
    matrix = random_graph(n, 99)
    print_matrix(matrix)
    table = to_table(matrix)
    print_table(table)

    dist = floyd_apsp(matrix)
    print('Floyd')
    print_matrix(dist)

    dist = bellman_ford_apsp(matrix)
    print('Bellman Ford')
    print_matrix(dist)

    dist = dijkstra_apsp(matrix)
    print('Dijkstra')
    print_matrix(dist)


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            matrix = random_graph(size, 99)
            if size == sizes[0]:
                print('MATRIX')
                print_matrix(matrix)
            for alg in algs:
                start_time = time.time()
                dist = alg(matrix)
                if size == sizes[0]:
                    print(alg.__name__)
                    print_matrix(dist)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def plot_times(dict_algs, sizes, trials, algs, title, file_name):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algs:
        alg_num += 1
        d = dict_algs[alg.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=alg.__name__)
    plt.legend()
    plt.title(title)
    plt.xlabel('Size')
    plt.ylabel('Time for ' + str(trials) + ' trials (ms)')
    plt.savefig(file_name)
    plt.show()


def print_times(dict_algs, file):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)

    with open('outputs/' + file + '.txt', 'a') as f:
        print(df, file=f)


def main():
    print("Sophia Balachanthiran")
    assn = 'Assignment7'
    sizes = [10 * i for i in range(1, 11)]
    algs = [floyd_apsp, bellman_ford_apsp, dijkstra_apsp]
    trials = 1
    title = 'Runtime of APSP Algorithms'
    dict_algs = run_algs(algs, sizes, trials)
    print_times(dict_algs, assn)
    plot_times(dict_algs, sizes, trials, algs, title, 'graphs/' + assn + '.png')


if __name__ == "__main__":
    main()
