# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 2 - Empirical Analysis of Search Algorithms
# Sophia Balachanthiran

# Acknowledgements:
# I worked with
# Ridwan Ali
# Federico Urraca

# I used the following sites
# https://www.geeksforgeeks.org/bubble-sort/


import random
import pandas as pd
import time
import matplotlib.pyplot as plt
import math


def random_list(size):
    my_list = [i for i in range(size)]
    random.shuffle(my_list)
    return my_list


def native_sort(arr):
    arr.sort()


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1


def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        j = gap
        while j < n:
            i = j - gap
            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]
                i = i - gap
            j += 1
        gap = gap // 2


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[largest] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_helper(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort_helper(arr, low, pi - 1)
        quicksort_helper(arr, pi + 1, high)


def quick_sort(arr):
    quicksort_helper(arr, 0, len(arr) - 1)


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def count_sort(arr):
    n = len(arr)
    max_element = max(arr)
    min_element = min(arr)
    range_of_elements = max_element - min_element + 1
    count_arr = [0 for _ in range(range_of_elements)]
    output_arr = [0 for _ in range(n)]
    for i in range(n):
        count_arr[arr[i] - min_element] += 1
    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i - 1]
    for i in range(n - 1, -1, -1):
        output_arr[count_arr[arr[i] - min_element] - 1] = arr[i]
        count_arr[arr[i] - min_element] -= 1
    for i in range(n):
        arr[i] = output_arr[i]


def countingsort_for_radixsort(arr, exp1):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]


def radix_sort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        countingsort_for_radixsort(arr, exp)
        exp *= 10


def bucket_sort(arr):
    n = len(arr)
    num_buckets = 10
    temp = []
    for i in range(num_buckets):
        temp.append([])
    for j in arr:
        index_b = int(j * num_buckets / n)
        temp[index_b].append(j)
    for i in range(num_buckets):
        insertion_sort(temp[i])
    k = 0
    for i in range(num_buckets):
        for j in range(len(temp[i])):
            arr[k] = temp[i][j]
            k += 1


def timsort_calcMinRun(n):
    MIN_MERGE = 32
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def timsort_insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1


def timsort_merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])
    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1
    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1


def tim_sort(arr):
    n = len(arr)
    min_run = timsort_calcMinRun(n)
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        timsort_insertion_sort(arr, start, end)
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                timsort_merge(arr, left, mid, right)
        size = 2 * size


def pigeonhole_sort(arr):
    my_min = min(arr)
    my_max = max(arr)
    size = my_max - my_min + 1
    holes = [0] * size
    for x in arr:
        holes[x - my_min] += 1
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + my_min
            i += 1


def bingo_sort(arr):
    n = len(arr)
    bingo = min(arr)
    largest = max(arr)
    next_bingo = largest
    next_pos = 0
    while bingo < next_bingo:
        start_pos = next_pos
        for i in range(start_pos, n):
            if arr[i] == bingo:
                arr[i], arr[next_pos] = arr[next_pos], arr[i]
                next_pos += 1
            elif arr[i] < next_bingo:
                next_bingo = arr[i]
        bingo = next_bingo
        next_bingo = largest


def combsort_getNextGap(gap):
    gap = (gap * 10) // 13
    if gap < 1:
        return 1
    return gap


def comb_sort(arr):
    n = len(arr)
    gap = n
    swapped = True
    while gap != 1 or swapped == 1:
        gap = combsort_getNextGap(gap)
        swapped = False
        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True


def cycle_sort(arr):
    n = len(arr)
    for cycleStart in range(0, n - 1):
        item = arr[cycleStart]
        pos = cycleStart
        for i in range(cycleStart + 1, n):
            if arr[i] < item:
                pos += 1
        if pos == cycleStart:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        while pos != cycleStart:
            pos = cycleStart
            for i in range(cycleStart + 1, n):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            arr_orig = random_list(size)
            for alg in algs:
                arr = arr_orig.copy()
                start_time = time.time()
                alg(arr)
                end_time = time.time()
                net_time = end_time - start_time
                verify_results(alg, arr)
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def verify_results(alg, arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]:
            print(alg.__name__, "is not sorted at position", i, len(arr), arr)


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


def print_times(dict_algs):
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)


def main():
    print("Sophia Balachanthiran")
    assn = "assignment_2"
    sizes = [10, 100, 1000, 10000]
    algs = [native_sort, bubble_sort, selection_sort, insertion_sort,
            cocktail_sort, shell_sort, heap_sort, quick_sort, merge_sort,
            count_sort, radix_sort, bucket_sort, tim_sort, pigeonhole_sort,
            bingo_sort, comb_sort, cycle_sort]
    trials = 1
    dict_algs = run_algs(algs, sizes, trials)
    print_times(dict_algs)
    plot_times(dict_algs, sizes, trials, algs, assn + ".png")


if __name__ == "__main__":
    main()