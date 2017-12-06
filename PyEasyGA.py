import math
import csv
import numpy
import pyeasyga

import requests
import json


f_data = 'D:\\Studies\\7_semester\\Intellect\\20.txt'
list_data = []  #исходные данные
list_data_2 = []

# Чтение данных из заданного файла в указанный список
def read_file(f_data, list):
    f = open(f_data, 'r')
    line = f.readline()
    while (line):
        row = line.split(' ')
        list.append(row)
        line = f.readline()
    f.close()


def convert(list):
    i=0
    j=0
    for element_i in list:
        for element_j in element_i:
            list[i][j]=float(list[i][j])
            j+=1
        j=0
        i+=1

from pyeasyga import pyeasyga


# define a fitness function
def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > 13000 or volume > 12:
        price = 0
    return price, weight, volume



def main():
    read_file(f_data, list_data) # Читаю данные из файла
    convert(list_data) #приводим всё к числовому типу для удобства дальнейших вычислений

    W = list_data[0][0]  # грузоподъемность
    V = list_data[0][1]  # вместимость

    #вес, объем, ценность
    m = 0
    k = 0
    print(W)
    print(V)
    print(list_data)

    list_data_2 = list_data[1:len(list_data)]
    print(list_data_2)

    ga = pyeasyga.GeneticAlgorithm(list_data_2)  # initialise the GA with data
    ga.population_size = 200  # increase population size to 200
    ga.fitness_function = fitness  # set the GA's fitness function
    ga.run()  # run the GA

    print(ga.best_individual())  # print the GA's best solution

    reg = 'https://cit-home1.herokuapp.com/api/ga_homework'
    txt = json.dumps({'1': {"value": 4588, "weight": 12266, "volume": 12,
                            "items": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0,
                                      1, 0, 1]}})
    head = {'content-type': 'application/json'}

    p = requests.post(reg, data=txt, headers=head)
    print(p)
    print(p.json())


if __name__ == "__main__":
    main()
