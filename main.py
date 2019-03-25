from collections import OrderedDict
import numpy as np


class Node:
    left = None
    right = None
    value = None

    def __init__(self, key):
        self.value = key


def load_file():
    lines2 = []
    with open('dictionary.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = [x.strip() for x in line.split(' ')]
            lines2.append(line)
    return lines2


def lexikographic_sort(lines):
    dictionary = {}
    for line in lines:
        dictionary[line[1]] = line[0]
    dictionary_2 = OrderedDict(sorted(dictionary.items(), key=lambda v: v, reverse=False))
    return dictionary_2


def get_prob_arrays(dictionary, p_total):
    p_prob = []
    q_prob = []
    arr_keys = []
    arr_dumm = []
    arr_tmp = []
    sumator = 0
    last_key = list(dictionary.keys())[-1]
    for key, value in dictionary.items():
        value = int(value)
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
    return p_prob, q_prob, arr_keys, arr_dumm


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


def get_optimal_matrix(p_array, q_array):
    n = len(p_array)

    e = np.zeros((n, n), dtype=np.float)
    w = np.zeros((n, n), dtype=np.float)
    root = np.zeros((n, n), dtype=np.float)

    for i in range(0, n):
        e[i][i] = q_array[i]
        w[i][i] = q_array[i]

    for l in range(1, n):
        for i in range(0, n - l):
            j = i + l
            e[i][j] = np.inf
            w[i][j] = w[i][j - 1] + p_array[j - 1] + q_array[j]
            for r in range(i, j):
                t = e[i][r] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r
    print('Optimal Cost of Binary Search Tree is: ', e[1][len(e) - 1])
    return e, w, root


def number_of_compares(root, key, num_of_compar):
    if isinstance(root.value, list) or root.value == key:
        return num_of_compar + 1

    if root.value < key:
        return number_of_compares(root.left, key, num_of_compar + 1)
    if root.value > key:
        return number_of_compares(root.right, key, num_of_compar + 1)


def create_tree(r, r_value, root, arr_k, arr_d):
    r_value = int(r_value)
    for i in range(0, len(r) - 1):
        if r[i][i + 1] == r_value and len(r) > 2:
            root = Node(arr_k[r_value][0])
            arr_cut = r[0:i + 1, 0:i + 1]
            arr_cut_rest = r[i:len(r), i:len(r)]
            if len(arr_cut) <= 1:
                root.left = Node(arr_d[r_value][0])
            else:
                root.left = create_tree(arr_cut, r[0][i], root, arr_k, arr_d)
            if len(arr_cut_rest) <= 1:
                root.right = Node(arr_d[r_value][0])
            else:
                root.right = create_tree(arr_cut_rest, r[i + 1][len(r) - 1], root, arr_k, arr_d)
        elif len(r) <= 2:
            root = Node(arr_k[r_value][0])
            root.left = Node(arr_d[r_value - 1][0])
            root.right = Node(arr_d[r_value][0])
    return root


def main():
    lines = load_file()
    dictionary = lexikographic_sort(lines)
    p_total = get_total_probability(dictionary)
    p_prob, q_prob, arr_keys, arr_dum = get_prob_arrays(dictionary, p_total)
    e, w, r = get_optimal_matrix(p_prob, q_prob)
    r_value = r[0][len(r) - 1]
    root = 1
    root = create_tree(r, r_value, root, arr_keys, arr_dum)
    finding = input("Write a word that you want find: ")
    if isinstance(finding, str):
        print('Number of compares: ', number_of_compares(root, str(finding), 0))
    else:
        print('"', finding, '" is not word. Failed')
    print('END')


if __name__ == '__main__':
    main()
