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
    finalalg = "import sys\niter_args = iter(sys.argv[1:])\n"
    for l in alg:  # noqa: E741
        if l.startswith("#"):
            continue

        aux = l
        while "input" in aux:
            aux = aux.replace(aux[aux.find("input"):aux.find(
                ")", aux.find("input")) + 1], "next(iter_args)", 1)
        finalalg += aux
    finalalg += '\n'

    return finalalg


def get_ans_in_out(answer):
    ans_in = []
    ans_out = []

    with zipfile.ZipFile(answer) as myzip:
        path_name = myzip.namelist()[0].split('/')[0]

        for i in range(1, (len(myzip.namelist())//2)+1):
            with myzip.open(path_name+'/'+str(i)+".in") as f:
                ans_in.append([x.decode('utf-8').strip()
                              for x in f.readlines()])
            with myzip.open(path_name+'/'+str(i)+".out") as f:
                ans_out.append([x.decode('utf-8').strip()
                               for x in f.readlines()])
    return ans_in, ans_out


def corrector(python_file, answer):
    # Fase 1 - ler questão e trata para entrada de argumentos do gabarito
    alg = python_file.read().decode('utf-8').split('\n')
    finalalg = replace_inputs(alg)

    with open("temp.py", "w") as file:
        file.write(finalalg)

    # Fase 2 - Entrada e Saída do Gabaritos

    ans_in, ans_out = get_ans_in_out(answer)

    # Fase 3 - para cada entrada verifica o resultado com a saída
    logs = []
    score = 0
    for i in range(len(ans_in)):
        sin = "\"".join(ans_in[i])
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
                output = stdoutdata[:-1].split("\n")
                output = [k.lower() for k in output]
                ans_out[i] = [k.lower() for k in ans_out[i]]
                if all(map(operator.eq, output, ans_out[i])):
                    logs.append(correct)
                    score += 1
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

    logs.append({'score': score*10, 'max_score': len(ans_out)*10})

    return logs
