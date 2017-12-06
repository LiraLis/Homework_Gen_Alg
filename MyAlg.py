import random
import requests
import json
from itertools import accumulate
from random import randint

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

#Создание первой популяции
def generation(list):
    population = []
    while (len(population)!=200):
        array = [random.randrange(0, 2) for i in range(30)]
        if fitness_function(array, list) != 0:
            population.append(array)
    return population


#Фитнес-функция
def fitness_function(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > list_data[0][0] or volume > list_data[0][1]:
        price = 0
    return price

#Создание пар-родителей с помощью рулетки
def select(popul, list_d):
    parents = []
    sort_population = sorted([[ind, fitness_function(val, list_d), val] for ind, val in enumerate(popul)], key=lambda x: x[1], reverse=True)
    for pairs in range(int(len(popul) / 2)):
        pair = []
        for p in range(2):
            interv = list(accumulate([sort_population[ind][1] for ind in range(len(sort_population))]))
            osob = randint(1, sum(sort_population[ind][1] for ind in range(len(sort_population))))
            for i in range(len(interv)):
                if osob <= interv[i] and osob > interv[i] - sort_population[i][1]:
                    pair.append(sort_population[i][2])
                    del sort_population[i]
                    break
        parents.append(pair)
    return parents


#Скрещивание пары по трем точкам
def crossover(parents, list_d):
    children = []
    child1 = []
    child2 = []
    cnt = 30
    while (len(children)!=2):
        dot1 = random.randint(0, cnt // 2)
        dot2 = random.randint(dot1, cnt - 1)
        dot3 = random.randint(dot2, cnt - 1)
        for i in range(0, dot1):
            child1.append(parents[0][i])
            child2.append(parents[1][i])
        for i in range(dot1, dot2):
            child1.append(parents[1][i])
            child2.append(parents[0][i])
        for i in range(dot2, dot3):
            child1.append(parents[0][i])
            child2.append(parents[1][i])
        for i in range(dot3, cnt):
            child1.append(parents[1][i])
            child2.append(parents[0][i])
        if (fitness_function(child1, list_d)!= 0 and fitness_function(child1, list_d)!= 0):
            children.append(child1)
            children.append(child2)
        else:
            child1 = []
            child2 = []
    return children

# Скрещивание всех отобранных пар особей
def crossover_popul(parents, list_d):
    children = []
    for p in range(len(parents)):
        children.extend(crossover(parents[p], list_d))
    return children

# Мутация (случайное изменение 3х битов у 5% особейслучайное изменение 3х битов у 5% особей)
def mutation(children):
    count = int(len(children) * 0.05)
    for i in range(0, count):
        osob = random.randint(0, len(children) - 1)
        for i in range(0, 3):
            bit = random.randint(0, 29)
            children[osob][bit] = children[osob][bit] ^ 1
    return children

#Формирование новой популяции (заменане не более 30% худших особей на потомков)
def new_population(parents, children, list_d):
    old = sorted([[ind, fitness_function(val, list_d), val] for ind, val in enumerate(parents)], key=lambda x: x[1], reverse=False)
    new = sorted([[ind, fitness_function(val, list_d), val] for ind, val in enumerate(children)], key=lambda x: x[1], reverse=True)
    for i in range(0, int((len(old)*0.2))):
        if (old[i][1]) < new[i][1]:
            old[i] = new.pop(i)
        else:
            break
    return [old[_][2] for _ in range(len(old))]


def result(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > list_data[0][0] or volume > list_data[0][1]:
        price = 0
    return price, weight, volume

def main():
    read_file(f_data, list_data) # Читаю данные из файла
    convert(list_data) #приводим всё к числовому типу для удобства дальнейших вычислений
    list_data_2 = list_data[1:len(list_data)]
    population = generation(list_data_2)

    for i in range(0, 100):
        parents = select(population, list_data_2)
        children = mutation(crossover_popul(parents, list_data_2))
        population = new_population(population, children, list_data_2)
    res = sorted([val for val in population], key=lambda x: x[1], reverse=True)

    print(result(res[0], list_data_2))
    print(res[0])

    reg = 'https://cit-home1.herokuapp.com/api/ga_homework'
    txt = json.dumps({'1': {"value": 4588, "weight": 12266, "volume": 12,
                            "items": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1]},
                      '2': {"value": 4684, "weight": 12675, "volume": 12,
                            "items": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0]}})
    head = {'content-type': 'application/json'}

    p = requests.post(reg, data=txt, headers=head)
    print(p)
    print(p.json())


if __name__ == "__main__":
    main()

