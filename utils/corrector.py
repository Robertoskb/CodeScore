import operator
import subprocess
import zipfile

error = {'message': 'Erro durante a execução',
         'class': 'bx bx-error icon', 'color': '#F2BE24'}
specific_error = {'message': '',
                  'class': 'bx bx-error icon', 'color': '#F2BE24'}
incorrect = {'message': 'A saída está errada',
             'class': 'bx bx-x-circle icon', 'color': '#D94C1A'}
correct = {'message': 'A saída está correta',
           'class': 'bx bx-check-circle', 'color': '#04D939'}


def corrigir(questao, gabarito):
    # Fase 1 - ler questão e trata para entrada de argumentos do gabarito
    alg = questao.read().decode('utf-8').split('\n')
    arg = 1
    algfinal = "import sys\n"
    for l in alg:  # noqa: E741
        if l.startswith("#"):
            continue
        # verifica se existe mais de um input na mesma linha, se sim,
        # troca todos incrementando o arg
        if l.count("input") == 1:
            # preciso verificar se o input esta dentro de um for,
            # para eu poder sustituir por por sys.argv[i+arg]
            if (l.startswith(" ") or l.startswith("\t")) and (alg[alg.index(l)-1].startswith("for")):  # noqa: E501
                var_do_for = alg[alg.index(l)-1].split()[1]
                aux = alg[alg.index(l)-1]
                aux = aux[aux.index("(")+1:aux.index(")")].split(",")
                algfinal += l.replace(l[l.find("input"): l.find(")", l.find(
                    "input")) + 1],
                    "sys.argv["+var_do_for+"+" + str(arg) + "]")
                if len(aux) > 1:
                    try:
                        arg += int(aux[1])
                    except:  # noqa: E722
                        pass
                else:
                    try:
                        arg += int(aux[-1])
                    except:  # noqa: E722
                        pass
            elif l.count("for") > 1:
                var_do_for = l[l.rindex("for"):].split()[1]
                algfinal += l.replace(l[l.find("input"):l.find(")", l.find(
                    "input")) + 1], "sys.argv[" + var_do_for+"+"+str(arg) + "]")  # noqa: E501
            else:
                algfinal += l.replace(l[l.find("input"):l.find(")",
                                      l.find("input")) + 1],
                                      "sys.argv[" + str(arg) + "]")
                arg += 1
        elif l.count("input") > 1:
            aux = l
            while aux.count("input") > 0:
                aux = aux.replace(aux[aux.find("input"):aux.find(")", aux.find(
                    "input")) + 1], "sys.argv[" + str(arg) + "]", 1)
                arg += 1
            algfinal += aux
        else:
            algfinal += l

        algfinal += '\n'

    with open("temp.py", "w") as file:
        file.write(algfinal)

    # Fase 2 - Entrada e Saída do Gabaritos
    gab_in = []
    gab_out = []

    with zipfile.ZipFile(gabarito) as myzip:
        path_name = gabarito.split('\\')[-1][:-4]
        for i in range(1, (len(myzip.namelist())//2)+1):
            with myzip.open(path_name+'/'+str(i)+".in") as f:
                gab_in.append([x.decode('utf-8').strip()
                              for x in f.readlines()])
            with myzip.open(path_name+'/'+str(i)+".out") as f:
                gab_out.append([x.decode('utf-8').strip()
                               for x in f.readlines()])

    # print(gab_in)
    # print(gab_out)

    # Fase 3 - para cada entrada verifica o resultado com a saída
    logs = []
    acertos = 0
    for i in range(len(gab_in)):
        sin = "\"".join(gab_in[i])
        args = sin.split("\"")
        args.insert(0, "python")
        args.insert(1, 'temp.py')

        try:
            process = subprocess.run(args,
                                     stdin=subprocess.PIPE,
                                     timeout=2,
                                     capture_output=True,
                                     text=True)
            stdoutdata, stderrdata = process.stdout, process.stderr
            if stderrdata:
                logs.append(error)
            else:
                saida = stdoutdata[:-1].split("\n")
                saida = [k.lower() for k in saida]
                gab_out[i] = [k.lower() for k in gab_out[i]]
                if all(map(operator.eq, saida, gab_out[i])):
                    logs.append(correct)
                    acertos += 1
                else:
                    logs.append(incorrect)
        except subprocess.TimeoutExpired as e:
            copy = specific_error.copy()
            copy['message'] = f'Erro: {e}'
            logs.append(copy)
        except Exception as e:
            copy = specific_error.copy()
            copy['message'] = f'Erro: {e}'
            logs.append(copy)

    logs.append({'score': acertos, 'max_score': len(gab_out)})

    return logs
