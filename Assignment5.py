# Analysis of Algorithms (CSCI 323)
# Winter 2023
# Assignment 5 - Estimating and Evaluating Recurrences
# Sophia Balachanthiran

# Acknowledgements:
# I worked with
# Ridwan Ali
# Joel Joseph

# I used the following sites
# https://www.geeksforgeeks.org/how-to-analyse-complexity-of-recurrence-relation/

import inspect
import math


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


dict_funcs = {}


def ff(f, n):
    func_name = f.__name__
    if func_name not in dict_funcs:
        dict_funcs[func_name] = {}
    dict_func = dict_funcs[func_name]
    if n not in dict_func:
        dict_func[n] = f(f, n)
    return dict_func[n]


def f0_fibonacci(f, n):
    return 0 if n == 0 else (1 if n == 1 else ff(f, n-1) + ff(f, n-2))


def f1_merge_sort(f, n):
    return 0 if n == 1 else 2 * ff(f, int(n/2)) + n


def f2_linear_search(f, n):
    return 1 if n == 1 else ff(f, (n-1)) + 1


def f3_binary_search(f, n):
    return 1 if n == 1 else ff(f, int(n/2)) + 1


def f4_towers_of_hanoi(f, n):
    return 1 if n == 1 else 2 * ff(f, int(n-1)) + 1


def f5_stooge_sort(f, n):
    return 1 if n == 1 else 3 * ff(f, int(2 * n/3)) + 1


def f6_dc_int_mult(f, n):
    return 1 if n == 1 else 4 * ff(f, int(n/2)) + n


def f7_karatsuba_int_mult(f, n):
    return 1 if n == 1 else 3 * ff(f, int(n/2)) + n


def f8_dc_exponentiation(f, n):
    return 1 if n == 1 else 2 * ff(f, int(n/2)) + 1


def f9_quick_select(f, n):
    return 1 if n == 1 else ff(f, int(n/2)) + n-1

def call_and_print(func, n):
    print(func.__name__, "for n =", n, "is", ff(func, n))


def func_body(f):
    body = inspect.getsource(f)
    idx = body.index("return")
    return '"' + body[7 + idx:].strip() + '"'



def evaluate_recurrences():
    funcs = [f0_fibonacci, f1_merge_sort, f2_linear_search, f3_binary_search,
             f4_towers_of_hanoi, f5_stooge_sort, f6_dc_int_mult, f7_karatsuba_int_mult,
             f8_dc_exponentiation, f9_quick_select]
    sizes = [2 ** i for i in range(10)]
    for func in funcs:
        print(func.__name__, func_body(func))
        for size in sizes:
            call_and_print(func, size)
        print()
    for func in dict_funcs:
        print(func, dict_funcs[func])


def master_theorem(a, b, c):
    temp = math.log(a, b)
    result = "T(n) = Θ(n^"
    if c < temp:
        result += "(log_" + str(b) + " " + str(a) + ")"
    elif c == temp:
        result += str(c) + " " + "log n"
    else:
        result += str(c)
    result += ")"
    return result


def evaluate_master_theorem():
    examples = [("Binary Search", 1, 2, 0),
                ("Merge Sort", 2, 2, 1),
                ("Stooge Sort", 3, 1.5, 0),
                ("D and C Long Integer Multiplication", 4, 2, 1),
                ("Karatsuba Long Integer Multiplication", 3, 2, 1),
                ("D and C Matrix Multiplication", 8, 2, 2),
                ("Strassen Matrix Multiplication", 7, 2, 2),
                ("Closest Point Naive", 2, 2, 2),
                ("D and C Exponentiation", 1, 2, 0),
                ("Quick Select", 1, 2, 1)
                ] 
    for example in examples:
        a, b, c = example[1], example[2], example[3]
        print("Master Theorem for", example[0], "is", master_theorem(a, b, c))


def main():
    evaluate_recurrences()
    evaluate_master_theorem()


if __name__ == "__main__":
    main()
