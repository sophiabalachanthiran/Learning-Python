# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 3 - Empirical Performance of Matrix Multiplication
# Sophia Balachanthiran

# Acknowledgements:
# I worked with
# Ridwan Ali
# Federico Urraca

# I used the following sites
# https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python


import assignment2
import random
import time
import numpy as np


def zero_matrix(n):
    return [[0 for _ in range(n)] for _ in range(n)]


def random_matrix(n, mn=1, mx=10):
    return [[random.randint(mn, mx) for _ in range(n)] for _ in range(n)]


def numpy_mult(m1, m2):
    m3 = np.matmul(m1, m2)
    return m3


def listcomp_mult(m1, m2):
    m3 = [[sum(a * b for a, b in zip(m1_row, m2_col)) for m2_col in zip(*m2)]
          for m1_row in m1]
    return np.array(m3)


def simple_mult(m1, m2):
    n = len(m1)
    m3 = zero_matrix(n)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                m3[i][j] += m1[i][k] * m2[k][j]
    return np.array(m3)


def divconq_mult(m1, m2):
    m3 = divconq(np.array(m1), np.array(m2))
    return m3


def divconq(m1, m2):
    if len(m1) == 1:
        return m1 * m2
    a, b, c, d = split_matrix(m1)
    e, f, g, h = split_matrix(m2)
    # ae + bg, af + bh, ce + dg and cf + dh
    p1 = divconq(a, e)
    p2 = divconq(b, g)
    p3 = divconq(a, f)
    p4 = divconq(b, h)
    p5 = divconq(c, e)
    p6 = divconq(d, g)
    p7 = divconq(c, f)
    p8 = divconq(d, h)
    c11 = p1 + p2
    c12 = p3 + p4
    c21 = p5 + p6
    c22 = p7 + p8
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    return c


def split_matrix(m):
    row, col = m.shape
    row2, col2 = int(row / 2), int(col / 2)
    return m[:row2, :col2], m[:row2, col2:], m[row2:, :col2], m[row2:, col2:]


def strassen(m1, m2):
    if len(m1) == 1:
        return m1 * m2
    a, b, c, d = split_matrix(m1)
    e, f, g, h = split_matrix(m2)
    p1 = strassen(a, f - h)
    p2 = strassen(a + b, h)
    p3 = strassen(c + d, e)
    p4 = strassen(d, g - e)
    p5 = strassen(a + d, e + h)
    p6 = strassen(b - d, g + h)
    p7 = strassen(a - c, e + f)
    c11 = p5 + p4 - p2 + p6
    c12 = p1 + p2
    c21 = p3 + p4
    c22 = p1 + p5 - p3 - p7
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    return c


def strassen_mult(m1, m2):
    m3 = strassen(np.array(m1), np.array(m2))
    return m3


def run_algs(algs, sizes, trials):
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            m1 = random_matrix(size)
            m2 = random_matrix(size)
            for alg in algs:
                start_time = time.time()
                m3 = alg(m1, m2)
                if size == sizes[0]:
                    print(alg.__name__)
                    print(m3)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    return dict_algs


def mini_test():
    n = 8
    m1 = random_matrix(n, 1, 10)
    m2 = random_matrix(n, 1, 10)
    m3a = listcomp_mult(m1, m2)
    m3b = simple_mult(m1, m2)
    m3c = numpy_mult(m1, m2)
    m3d = divconq_mult(m1, m2)
    m3e = strassen_mult(m1, m2)
    print(m3a)
    print(m3b)
    print(m3c)
    print(m3d)
    print(m3e)


def main():
    # mini_test()
    print("Sophia Balachanthiran")
    assn = "Assignment3"
    sizes = [4, 8, 16, 32, 64]
    algs = [numpy_mult, listcomp_mult, simple_mult, divconq_mult, strassen_mult]
    trials = 1
    title = "Runtime of Matrix Multiplication Algorithms"
    dict_algs = run_algs(algs, sizes, trials)
    assignment2.print_times(dict_algs)
    assignment2.plot_times(dict_algs, sizes, trials, algs, assn + ".png")


if __name__ == "__main__":
    main()