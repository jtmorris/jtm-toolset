# jtm-toolset
A repository for me to accumulate useful "helper" code for various languages, frameworks, and libraries.

## Usage
Just download the desired file into your project and include it via the language's/framework's/library's normal mechanisms.

## Tests
Wherever applicable, test driven development is done. If modifying code, RUN THE TESTS! If adding code, WRITE TESTS!
# Python
Most Python files have doctests. Some have associated unit or functionality tests. For doctests, just run the file from a terminal with Python. E.g. `$ python3 jtm_python_helpers.py`. Any failed doctests will scream bloody murder. For verbose test results, use the `-v` flag. E.g. `$ python3 -v jtm_python_helpers.py`.

For unit and functionality tests, Python's unittest library is used. To run, go to the tests directory and execute the file from a terminal with Python. E.g. `$ python3 test_jtm_opencv_helpers.py`. Results will be spit out.
