import shutil
import sys
import os
import subprocess
# import resource

local_dir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) != 5:
    print("Usage: evaluator.exe [problem name] [file name] [time limit] [memory limit]")
    exit()

problem_name = sys.argv[1]
file_name = sys.argv[2]
max_time = int(sys.argv[3])/1000
max_ram = sys.argv[4]

MAX_VIRTUAL_MEMORY = max_ram * 1024 * 1024


print("WARN: RAM LIMIT NOT WORKING YET")
print("COMPILATION OF CPP COMING SOON")
print("PARTIAL POINTS COMING SOON")


def evaluate(test_no):
    shutil.copy(str.format("{0}/{1}/tests/{2}-{1}.in", local_dir, problem_name, test_no),
                str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
    try:
        subprocess.check_call(str.format("{0}\\{1}\\exe\\{2}.exe", local_dir, problem_name, file_name),
                              timeout=max_time, cwd=str.format("{0}\\{1}\\exe", local_dir, problem_name))
    except subprocess.TimeoutExpired:
        os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
        return [0, "Time limit exceeded"]
    except subprocess.CalledProcessError as err:
        os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
        return [0, str.format("Error: {0}", err.returncode)]
    os.remove(str.format("{0}/{1}/exe/{1}.in", local_dir, problem_name))
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
    return [1, "Diff: OK!"]


with open(str.format('{0}/{1}/tests/tests.txt', local_dir, problem_name)) as f:
    tests = f.read().splitlines()

total = 0

for i in range(len(tests)):
    p = tests[i].split(' ')[1]
    res = evaluate(tests[i].split(' ')[0])
    print(str.format("Test: {0} ~ {1} ~ {2}p", tests[i].split(' ')[0], res[1], res[0] * int(p)))
    total += res[0] * int(p)

print(str.format("Total: {0}p", total))
