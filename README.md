# Evaluator

##### Installing:

Download evaluator.exe

##### Usage:

Create in the download folder, a directory named `problem_name`. Inside it create 2 directories: `exe` and `tests`. 

Compile the source code in your favorite IDE / compiler and copy the resulted `.exe` file in the `exe` folder.

Create or download test cases and copy them in the `tests` directory. The test file name must be in format: `(test_number)-(problem_name).in/ok`. If there is no tests.txt file, create one and write on each line: `(test_number) (points_awarded)`, for each test case.

Open command prompt, change to download directory using `cd /d download_location` and run `evaluator.exe (problem_name) (solution_file_name) (time_limit) (memory_limit)`(solution_file_name is the `.exe` file copied, without`.exe` in the end).

Wait for your solution to be evaluated.