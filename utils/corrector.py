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


def replace_inputs(alg):
    algfinal = "import sys\niter_args = iter(sys.argv[1:])\n"
    for l in alg:  # noqa: E741
        if l.startswith("#"):
            continue

        aux = l
        while "input" in aux:
            aux = aux.replace(aux[aux.find("input"):aux.find(
                ")", aux.find("input")) + 1], "next(iter_args)", 1)
        algfinal += aux
    algfinal += '\n'

    return algfinal


def corrector(questao, gabarito):
    # Fase 1 - ler questão e trata para entrada de argumentos do gabarito
    alg = questao.read().decode('utf-8').split('\n')
    algfinal = replace_inputs(alg)

    with open("temp.py", "w") as file:
        file.write(algfinal)

    # Fase 2 - Entrada e Saída do Gabaritos
    gab_in = []
    gab_out = []

    with zipfile.ZipFile(gabarito) as myzip:
        path_name = myzip.namelist()[0].split('/')[0]

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
        except subprocess.TimeoutExpired:
            copy = specific_error.copy()
            copy['message'] = 'Erro: Excedeu o tempo de limite de execução'
            logs.append(copy)
        except Exception as e:
            copy = specific_error.copy()
            copy['message'] = f'Erro: {e}'
            logs.append(copy)

    logs.append({'score': acertos*10, 'max_score': len(gab_out)*10})

    return logs
