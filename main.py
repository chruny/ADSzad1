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


def get_probability_array(dictionary, p_total):
    # TODO
    p = []
    q = []
    k = []
    d = []
    tmp_elements = []
    tmp_values = []
    last_key = list(dictionary.keys())[-1]
    for key, value in dictionary.items():
        value = float(value)
        if value > 50000 and len(tmp_elements) > 0:
            d.append(tmp_elements)
            tmp_elements = []
            q.append(get_q_probability(tmp_values, p_total))
            tmp_values = []

            k.append(key)
            p.append(get_p_probability(value, p_total))
        elif value > 50000 and len(tmp_elements) <= 0:
            k.append(key)
            p.append(get_p_probability(value, p_total))
        elif value < 50000:
            tmp_elements.append(key)
            tmp_values.append(value)
        elif key == last_key:
            tmp_elements.append(key)
            tmp_values.append(value)
            d.append(tmp_elements)
            q.append(get_q_probability(tmp_values, p_total))
    print(sum(p) + sum(q))
    print(len(k) + sum(d))
    return d, q, k, p


def get_total_probability(dictionary):
    sumator = 0
    for key, value in dictionary.items():
        sumator = sumator + float(value)
    return sumator


def get_p_probability(frequency, p_total):
    return frequency / p_total


def get_q_probability(array, p_total):
    sumator = 0
    for element in array:
        sumator = sumator + element
    return sumator / p_total


def get_matrix(dictionary, p_array, q_array):
    print()


def main():
    lines = load_file()
    dictionary = lexikographic_sort(lines)
    p_total = get_total_probability(dictionary)
    get_probability_array(dictionary, p_total)


if __name__ == '__main__':
    main()
