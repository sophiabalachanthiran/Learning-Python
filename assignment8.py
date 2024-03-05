# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 8 - Accuracy and Efficiency of Bin-Packing Algorithms
# Sophia Balachanthiran

# Acknowledgements:
# I worked with
# Ridwan Ali
# Joel Joseph

# I used the following sites
#https://www.geeksforgeeks.org/bin-packing-problem-minimize-number-of-used-bins/.


import copy
import pandas as pd
import time
import matplotlib.pyplot as plt
from os import listdir

INF = 999999
BIN_SIZE = 100


def bpp_next_fit(weights):
    res = 0
    rem = BIN_SIZE
    for weight in weights:
        if rem >= weight:
            rem = rem - weight
        else:
            res += 1
            rem = BIN_SIZE - weight
    return res


def bpp_first_fit(weights):
    res = 0
    n = len(weights)
    bin_rem = [0] * n
    for weight in weights:
        j = 0
        while j < res:
            if bin_rem[j] >= weight:
                bin_rem[j] = bin_rem[j] - weight
                break
            j += 1
        if j == res:
            bin_rem[res] = BIN_SIZE - weight
            res = res + 1
    return res


def bpp_best_fit(weights):
    res = 0
    n = len(weights)
    bin_rem = [0] * n
    for weight in weights:
        min_rem = BIN_SIZE + 1
        bi = 0
        for j in range(res):
            if bin_rem[j] >= weight and bin_rem[j] - weight < min_rem:
                bi = j
                min_rem = bin_rem[j] - weight
        if min_rem == BIN_SIZE + 1:
            bin_rem[res] = BIN_SIZE - weight
            res += 1
        else:
            bin_rem[bi] -= weight
    return res


def bpp_worst_fit(weights):
    res = 0
    n = len(weights)
    bin_rem = [0] * n
    for weight in weights:
        mx, wi = -1, 0
        for j in range(res):
            if bin_rem[j] >= weight and bin_rem[j] - weight > mx:
                wi = j
                mx = bin_rem[j] - weight
        if mx == -1:
            bin_rem[res] = BIN_SIZE - weight
            res += 1
        else:
            bin_rem[wi] -= weight
    return res


def bpp_first_fit_decreasing(weights):
    weights_sorted = copy.copy(weights)
    weights_sorted.sort(reverse=True)
    return bpp_first_fit(weights_sorted)


def bpp_best_fit_decreasing(weights):
    weights_sorted = copy.copy(weights)
    weights_sorted.sort(reverse=True)
    return bpp_best_fit(weights_sorted)


def bpp_worst_fit_decreasing(weights):
    weights_sorted = copy.copy(weights)
    weights_sorted.sort(reverse=True)
    return bpp_worst_fit(weights_sorted)


def bpp_next_fit_decreasing(weights):
    weights_sorted = copy.copy(weights)
    weights_sorted.sort(reverse=True)
    return bpp_next_fit(weights_sorted)


def run_algs(algs, data, sizes):
    dict_algs_times = {}
    dict_algs_bins = {}
    trials = 1
    for alg in algs:
        dict_algs_times[alg.__name__] = {}
        dict_algs_bins[alg.__name__] = {}
    size_num = -1
    for size in sizes:
        size_num += 1
        for alg in algs:
            dict_algs_times[alg.__name__][size] = 0
            dict_algs_bins[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            weights = data[size_num]
            for alg in algs:
                start_time = time.time()
                bins = alg(weights)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs_times[alg.__name__][size] += 1000 * net_time
                dict_algs_bins[alg.__name__][size] = bins
    return dict_algs_times, dict_algs_bins


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
    plt.xlabel("Size")
    plt.ylabel("Time for " + str(trials) + " trials (ms)")
    plt.savefig(file_name)
    plt.show()


def print_times(dict_algs):
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)


def big_test():
    assn = "Assignment8"
    sizes = [10 * 1 for _ in range(1, 11)]
    algs = []
    trials = 1
    title = "Run times of algorithms"
    dict_algs = run_algs(algs, sizes, trials)
    print_times(dict_algs)
    plot_times(dict_algs, sizes, trials, algs, title, assn + ".png")


def read_data(path):
    data = []
    for filename in sorted(listdir(path)):
        if filename.startswith("BinPackingData"):
            with open(path + "/" + filename, "r") as file:
                weights = file.readlines()
                weights = [int(weight.strip()) for weight in weights]
                data.append(weights)
    return data


def main():
    # big_test()
    print("Sophia Balachanthiran")
    path = "BPP_data"
    data = read_data(path)
    sizes = [len(datum) for datum in data]
    algs = [bpp_next_fit, bpp_first_fit, bpp_best_fit, bpp_worst_fit,
            bpp_next_fit_decreasing, bpp_first_fit_decreasing, bpp_best_fit_decreasing, bpp_worst_fit_decreasing]
    dict_algs_times, dict_algs_bins = run_algs(algs, data, sizes)
    print_times(dict_algs_times)
    title = "Runtime for Bin Packing Approximation Algorithms"
    plot_times(dict_algs_times, sizes, 1, algs, title, "assn_8_times.png")

    print_times(dict_algs_bins)
    title = "Number of bins for Bin Packing Approximation Algorithms"
    plot_times(dict_algs_bins, sizes, 1, algs, title, "assn_8_bins.png")


if __name__ == "__main__":
    main()
