# Evaluator

##### Installing:

Download evaluator.exe

##### Usage:

1. Create in the download folder, a directory named `problem_name`. Inside it create 3 directories: `exe`, `source` and `tests`. 

2. Copy the source code file (only c/c++ supported) to `source` or the compiled `.exe` to the `exe` folder.

3. Add tests / generator (/ verifiers)
    * Create or download test cases and copy them in the `tests` directory. The test file name must be in format: `(test_number)-(problem_name).in/ok`. If there is no tests.txt file, create one and write on each line: `(test_number) (points_awarded)`, for each test case, or
    * Create a generator which outputs to `problem_name.in` the inputs and to `problem_name.ok` the correct output and copy the compiled exe to `tests`
    * (Optional - if a test case has more solutions) Create a verifier which gets input from `problem_name.in` and `problem_name.out` and prints to the terminal `0` if the solution is correct or a message if the solution is wrong. Copy the compiled exe to `tests`.

4. Open command prompt, change to download directory using `cd /d download_location` and run `evaluator.exe -p problem_name -f solution_file_name.extension -t time_limit_in_milliseconds -m memory_limit_in_kb`.
