import argparse
import os
import shutil
import subprocess

# import resource

local_dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Evaluate problem")
parser.add_argument('--problem', '-p', dest='problem', help='problem name')
parser.add_argument('--filename', '-f', dest='filename', help='a file to evaluate')
parser.add_argument('--compiler', '-c', dest='complier', default='',
                    help='compiler (gcc, g++) if not detected automatically')
parser.add_argument('--generator', '-g', dest='generator', default='',
                    help='a .exe file which generates input')
parser.add_argument('--verifier', '-v', dest='verifier', default='',
                    help='a .exe file which verifies output(if generator and more possible)')
parser.add_argument('--tests', dest='tests', type=int, default='10',
                    help='how many tests to run(if generator)')
parser.add_argument('--time', '-t', dest='time', help='time limit (ms)')
parser.add_argument('--memory', '-m', dest="memory", help="memory limit (kb)")

args = parser.parse_args()
problem_name = args.problem
file_name = args.filename
max_time = int(args.time)/1000
max_ram = args.memory

MAX_VIRTUAL_MEMORY = max_ram * 1024 * 1024


print("RAM LIMIT NOT WORKING YET")
print("PARTIAL POINTS COMING SOON")


def evaluate_test(test_no):
    shutil.copy(str.format("{0}/{1}/tests/{2}-{1}.in", local_dir, problem_name, test_no),
                str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
    try:
        subprocess.check_call(str.format("{0}\\{1}\\exe\\{2}", local_dir, problem_name, file_name),
                              timeout=max_time, cwd=str.format("{0}\\{1}\\exe", local_dir, problem_name))
    except subprocess.TimeoutExpired:
        os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
        return [0, "Time limit exceeded"]
    except subprocess.CalledProcessError as err:
        os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
        return [0, str.format("Error: {0}", err.returncode)]
    if args.verifier == '':
        os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
        # noinspection PyBroadException
        try:
            with open(str.format("{0}/{1}/exe/{1}.out", local_dir, problem_name)) as of:
                output = of.read().splitlines()
        except IOError:
            os.remove(str.format("{0}/{1}/exe/{1}.out", local_dir, problem_name))
            return [0, "Diff: No output"]
        except Exception:
            os.remove(str.format("{0}/{1}/exe/{1}.out", local_dir, problem_name))
            return [0, "Internal error"]
        os.remove(str.format("{0}/{1}/exe/{1}.out", local_dir, problem_name))
        with open(str.format("{0}/{1}/tests/{2}-{1}.ok", local_dir, problem_name, test_no)) as of:
            ok = of.read().splitlines()
        if len(output) == 0:
            return [0, "No output"]
        while ok[len(ok)-1] == '':
            ok = ok[:len(ok)-1]
        while output[len(output)-1] == '\n' or output[len(output)-1] == ' ':
            output = output[:len(output)-1]
        if len(output) != len(ok):
            return [0, str.format("Diff: line {0}", max(len(output), len(ok)) + 1)]
        for line in range(max(len(output), len(ok))):
            if output[line] != ok[line]:
                return [0, str.format("Diff: line {0}", line + 1)]
    else:
        output, err = subprocess.Popen(str.format("{0}\\{1}\\tests\\{2}", local_dir, problem_name, args.verifier),
                                       cwd=str.format("{0}\\{1}\\exe", local_dir, problem_name),
                                       stdout=subprocess.PIPE).communicate()
        os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
        if err is not None:
            return [0, str.format("Verifier: {0}", err)]

        if output == 0:
            return [1, "Verifier: OK!"]
        else:
            return [0, str.format("Verifier: {0}", output.decode("utf-8"))]

    return [1, "Diff: OK!"]


if __name__ == "__main__":
    if file_name.endswith('.cpp'):
        subprocess.call(str.format('g++ -Wall -O2 -std=c++14 -static {0} -lm -o ..\\exe\\{1}', file_name,
                                   file_name[:-4]),
                        cwd=str.format("{0}\\{1}\\source", local_dir, problem_name))
        file_name = str(file_name[:-4] + '.exe')
    elif file_name.endswith('.c'):
        subprocess.call(str.format('gcc -Wall -O2 -std=c11 -static {0} -lm -o ..\\exe\\{1}', file_name,
                                   file_name[:-4]),
                        cwd=str.format("{0}\\{1}\\source", local_dir, problem_name))
        file_name = str(file_name[:-4] + '.exe')
    elif file_name.endswith('.exe'):
        pass
    else:
        print("Could not detect best compiler. Specify one with --compiler (gcc, g++)")
    if args.generator != '':
        import os
        import glob

        # Get a list of all the file paths that ends with .txt from in specified directory
        fileList = glob.glob(str.format("{0}\\{1}\\tests\\*.in", local_dir, problem_name))
        for filePath in fileList:
            # noinspection PyBroadException
            try:
                os.remove(filePath)
            except Exception:
                print("Error while deleting file : ", filePath)

        fileList = glob.glob(str.format("{0}\\{1}\\tests\\*.ok", local_dir, problem_name))
        for filePath in fileList:
            # noinspection PyBroadException
            try:
                os.remove(filePath)
            except Exception:
                print("Error while deleting file : ", filePath)

        tests_gen = []
        for i in range(args.tests):
            subprocess.call(str.format("{0}\\{1}\\tests\\{2}", local_dir, problem_name, args.generator),
                            cwd=str.format("{0}\\{1}\\tests", local_dir, problem_name))
            shutil.copy(str.format("{0}/{1}/tests/{1}.in", local_dir, problem_name),
                        str.format("{0}/{1}/tests/{2}-{1}.in", local_dir, problem_name, i))
            shutil.copy(str.format("{0}/{1}/tests/{1}.ok", local_dir, problem_name),
                        str.format("{0}/{1}/tests/{2}-{1}.ok", local_dir, problem_name, i))
            tests_gen.append(str.format('{0} {1}\n', i, 100/args.tests))
        with open(str.format('{0}/{1}/tests/tests.txt', local_dir, problem_name), 'w') as f:
            f.writelines(tests_gen)

    with open(str.format('{0}/{1}/tests/tests.txt', local_dir, problem_name)) as f:
        tests = f.read().splitlines()
    total = 0
    for i in range(len(tests)):
        p = tests[i].split(' ')[1]
        res = evaluate_test(tests[i].split(' ')[0])
        print(str.format("Test: {0} ~ {1} ~ {2}p", tests[i].split(' ')[0], res[1], res[0] * float(p)))
        total += res[0] * float(p)
    print(str.format("Total: {0}p", total))

