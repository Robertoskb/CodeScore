import sys
valores = {1: 11, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:10, 12:10, 13:10}

lista = [valores[int(i)] for i in sys.argv[1].split()[1:]]

while 11 in lista and sum(lista) > 21:
  lista[lista.index(11)] = 1


print(sum(lista))
