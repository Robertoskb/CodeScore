P, S, E = (int(input()) for _ in range(3))

pos = 0

while pos < P:
    print(pos, end=' ')
    if pos + S < P:
        print(pos + S)
        pos += S-E

    else:
        print('saiu')
        break
