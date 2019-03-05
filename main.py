from collections import OrderedDict
import numpy as np
import pandas as pd


def load_file():
    lines2 = []
    with open('dictionary.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = [x.strip() for x in line.split(' ')]
            lines2.append(line)
        print(len(lines2))
    return lines2


def lexikographic_sort(lines):
    dictionary = {}
    for line in lines:
        dictionary[line[1]] = line[0]
    dictionary_2 = OrderedDict(sorted(dictionary.items(), key=lambda v: v, reverse=False))
    return dictionary_2


def get_probability_array_2(dictionary, p_total):
    p_prob = []
    q_prob = []
    arr_keys = []
    arr_dumm = []
    arr_tmp = []
    sumator = 0
    last_key = list(dictionary.keys())[-1]
    for key, value in dictionary.items():
        value = float(value)
        if value > 50000:
            arr_keys.append((key, value))
            arr_dumm.append((arr_tmp, sumator))
            sumator = 0
            arr_tmp = []
        else:
            sumator += value
            arr_tmp.append(key)
        if last_key == key:
            arr_dumm.append((arr_tmp, sumator))

    p_prob = get_probability(arr_keys, p_total)
    q_prob = get_probability(arr_dumm, p_total)
    print(len(p_prob), len(q_prob))
    return p_prob, q_prob


def get_probability(arr_prob, p_total):
    arr = []
    for line in arr_prob:
        arr.append(line[1] / p_total)
    return arr


def get_total_probability(dictionary):
    sumator = 0
    for key, value in dictionary.items():
        sumator = sumator + float(value)
    return sumator


def get_p_probability(frequency, p_total):
    return frequency / p_total


def get_q_probability(array, p_total):
    return sum(array) / p_total


def get_matrix(dictionary, p_array, q_array):
    n = len(p_array)

    p = pd.Series(p_array, index=range(1, n + 1))
    q = pd.Series(q_array, index=range(1, n + 2))

    e = pd.DataFrame(np.diag(q_array), index=range(1, n + 2))
    w = pd.DataFrame(np.diag(q_array), index=range(1, n + 2))

    root = pd.DataFrame(np.zeros((n, n)), index=range(1, n + 1), columns=range(1, n + 1))

    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            e.set_value(i, j, np.inf)
            w.set_value(i, j, w.get_value(i, j - 1 + p[j] + q[j]))
            for r in range(i, j + 1):
                t = e.get_value(i, r - 1) + e.get_value(r + 1, j) + w.get_value(i, j)
                if t < e.get_value(i, j):
                    e.set_value(i, j, t)
                    root.set_value(i, j, r)
    print(e)
    print(w)
    print(root)


def main():
    lines = load_file()
    dictionary = lexikographic_sort(lines)
    p_total = get_total_probability(dictionary)
    # d, q_prob, k, p_prob = get_probability_array(dictionary, p_total)
    p_prob, q_prob = get_probability_array_2(dictionary, p_total)
    get_matrix(dictionary, p_prob, q_prob)


if __name__ == '__main__':
    main()
