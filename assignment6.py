# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 6 - Empirical Performance of Search Structures
# Sophia Balachanthiran


import copy
import random
import assignment2
import time


def display_hash(hash_table):
    for i in range(len(hash_table)):
        print(i, hash_table[i])
    print()


def hash_chaining_build(arr):
    size = int(len(arr) / 10)
    hash_table = [[] for _ in range(size)]
    for key in arr:
        hash_key = hash_function(key, size)
        hash_table[hash_key].append(key)
    return hash_table


def hash_probing_build(arr):
    size = len(arr) * 2
    hash_table = [None for _ in range(size)]
    k = 0
    for key in arr:
        hash_key = hash_function(key, size)

        if hash_table[hash_key] is None:
            hash_table[hash_key] = key
        else:
            i = 0
            while hash_table[hash_key] is not None:
                i += 1
                hash_key = hash_function_probing(hash_key, size, i)
            hash_table[hash_key] = key
        k += 1
    return hash_table


def hash_chaining_search(hash_table, arr):
    size = len(hash_table)
    found = [False] * len(arr)
    for j in range(len(arr)):
        key = arr[j]
        hash_key = hash_function(key, size)
        for item in hash_table[hash_key]:
            if item == key:
                found[j] = True
                break
    return found


def hash_probing_search(hash_table, arr):
    size = len(hash_table)
    found = [False] * len(arr)
    print()
    for j in range(len(arr)):
        key = arr[j]
        hash_key = hash_function(key, size)
        i = 0
        while hash_table[hash_key] is None or hash_table[hash_key] != key:
            i += 1
            hash_key = hash_function_probing(hash_key, size, i)
        found[j] = True
    return found


def hash_function_probing(hash_key, size, i):
    a, b, c = 0, 1, 0
    new_hash_key = (hash_key + 1) % size
    return new_hash_key


def hash_function(key, size):
    return key % size


def run_algs(algs, sizes, trials):
    dict_algs = {}
    test_map = {}
    for alg in algs:
        dict_algs[alg[2]] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg[2]][size] = 0
        for trial in range(1, trials + 1):
            arr = random_list(size)
            arr_copy = copy.copy(arr)
            random.shuffle(arr_copy)
            for alg in algs:
                start_time = time.time()
                build = alg[0]
                ds = build(arr)
                search = alg[1]
                found = search(ds, arr_copy)
                if size == sizes[0]:
                    print(alg[2])
                    print(ds)
                    print(found)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg[2]][size] += 1000 * net_time
    return dict_algs


def random_list(size):
    arr = [i**3 for i in range(size)]
    random.shuffle(arr)
    return arr


def mini_test():
    size = 1000
    arr = random_list(size)
    print(arr)
    ht_probing = hash_probing_build(arr)
    print("Hash probing disp hash: ")
    display_hash(ht_probing)
    random.shuffle(arr)
    print("Hash pROBING PRINT: ")
    print(ht_probing)
    found = hash_probing_search(ht_probing, arr)
    print("Hash Probing Search22: ")
    print(found)


def big_test():
    assn = "assignment6"
    sizes = [100, 1000, 10000]
    algs = [(hash_probing_build, hash_probing_search, "Hash Probing"),
            (hash_chaining_build, hash_chaining_search, "Hash Chaining")
            ]
    trials = 1
    title = "Runtime of Search Structures (Build and Search)"
    dict_algs = run_algs(algs, sizes, trials)
    assignment2.print_times(dict_algs)
    assignment2.plot_times(dict_algs, sizes, trials, algs, title, assn + ".png")


def main():
    print("Sophia Balachanthiran")
    big_test()


if __name__ == "__main__":
    main()
