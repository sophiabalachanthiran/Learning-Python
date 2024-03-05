# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 1 - Empirical Analysis of Search Algorithms
# Sophia Balachanthiran

# Acknowledgements:
# I worked with
# Ridwan Ali
# Federico Urraca

# I used the following sites
# https://www.geeksforgeeks.org/linear-search/


import random
import pandas as pd
import time
import matplotlib.pyplot as plt
import math


def random_list(size):
    rl = []
    num = 0
    for i in range(size):
        r = random.randint(1, 10)
        num += r
        rl.append(num)
    return rl


def native_search(arr, key):
    return arr.index(key)


def linear_search_iterative(arr, key):
    n = len(arr)
    for i in range(0, n):
        if arr[i] == key:
            return i
    return i


def binary_search_iterative(arr, key):
    lo = 0
    hi = len(arr) - 1
    while hi - lo > 1:
        mid = (hi + lo) // 2
        if arr[mid] < key:
            lo = mid + 1
        else:
            hi = mid

    if arr[lo] == key:
        return lo
    elif arr[hi] == key:
        return hi
    else:
        return -1


def binary_search_recursive(arr, key):
    return binary_search_recursive_helper(arr, 0, len(arr), key)


def binary_search_recursive_helper(arr, l, r, key):
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            return binary_search_recursive_helper(arr, l, mid - 1, key)
        else:
            return binary_search_recursive_helper(arr, mid + 1, r, key)
    else:
        return -1


def print_times(dict_algs):
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)


def binary_search_randomized(arr, key):
    return binary_search_randomized_helper(arr, 0, len(arr) - 1, key)


def binary_search_randomized_helper(arr, l, r, key):
    if r >= l:
        mid = random.randint(l, r)
        if arr[mid] == key:
            return mid
        if arr[mid] > key:
            return binary_search_randomized_helper(arr, l, mid - 1, key)
        else:
            return binary_search_randomized_helper(arr, mid + 1, r, key)
    return -1


def exponential_search(arr, x):
    if arr[0] == x:
        return 0
    i = 1
    n = len(arr)
    while i < n and arr[i] <= x:
        i = i * 2
    return binary_search_recursive_helper(arr, i // 2, min(i, n - 1), x)


def jump_search(arr, key):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while arr[(min(step, n) - 1)] < key:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    while arr[prev] < key:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[prev] == key:
        return prev
    return -1


def interpolation_search(arr, key):
    return interpolation_search_helper(arr, 0, len(arr)-1, key)


def interpolation_search_helper(arr, lo, hi, key):
    if arr[lo] == arr[hi]:
        if key == arr[lo]:
            return lo
        else:
            return -1
    if lo <= hi and arr[lo] <= key <= arr[hi]:
        pos = int(lo + ((hi - lo) / float(arr[hi] - arr[lo])) * float((key - arr[lo])))
        if arr[pos] == key:
            return pos
        elif arr[pos] < key:
            return interpolation_search_helper(arr, pos + 1, hi, key)
        else:
            return interpolation_search_helper(arr, lo, pos - 1, key)
    return -1


def fibonacci_search(arr, x):
    n = len(arr)
    fib2 = 0
    fib1 = 1
    fibM = fib2 + fib1
    while fibM < n:
        fib2 = fib1
        fib1 = fibM
        fibM = fib2 + fib1
    offset = -1
    while fibM > 1:
        i = min(offset + fib2, n - 1)
        if arr[i] < x:
            fibM = fib1
            fib1 = fib2
            fib2 = fibM - fib1
            offset = i
        elif arr[i] > x:
            fibM = fib2
            fib1 = fib1 - fib2
            fib2 = fibM - fib1
        else:
            return i
    if fib1 and arr[n - 1] == x:
        return n - 1

    return -1


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            arr = random_list(size)
            idx = random.randint(0, size - 1)
            key = arr[idx]
            for alg in algs:
                start_time = time.time()
                idx_found = alg(arr, key)
                end_time = time.time()
                net_time = end_time - start_time
                verify_results(alg, arr, idx, idx_found)
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs

def verify_results(alg, arr, idx, idx_found):
    if idx_found != idx:
        print(alg.__name__, "wrong index found", arr, idx, idx_found)


def plot_times(dict_algs, sizes, trials, algs, file_name):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algs:
        alg_num += 1
        d = dict_algs[alg.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=alg.__name__)
    plt.legend()
    plt.title("Runtime of algorithms")
    plt.xlabel("Number of elements")
    plt.ylabel("Time for " + str(trials) + " trials (ms)")
    plt.savefig(file_name)
    plt.show()


def main():
    sizes = [10, 100, 1000, 10000]
    searches = [native_search, linear_search_iterative, binary_search_iterative, binary_search_recursive,
                binary_search_randomized, exponential_search, jump_search, interpolation_search, fibonacci_search]
    trials = 1000
    dict_searches = run_algs(searches, sizes, trials)
    print_times(dict_searches)
    plot_times(dict_searches, sizes, trials, searches, "Assignment1.png")


if __name__ == "__main__":
    main()