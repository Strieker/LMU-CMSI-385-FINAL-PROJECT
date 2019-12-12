# LMU-CMSI-385-FINAL-PROJECT
Programmatic simulation of non-deterministic finite state automota

## Instructions on How To Run The Program Itself
Within the command line, run ```python3 "insert_file_path_name" insert_string_in question```. I found it easiest to save the file you are passing into the program within the project folder after cloning this repository.

## Instructions on How To Run Tests for the Program
There are 13 test harnesses found within the ```test.py file```. All harnesses are called within ```__main__()```, after making an instance of a test class. Notice that each call to a single test harness is commented out, because these calls cannot all at once due to issues with stdin. To ensure that the tests function properly, simply uncomment one function call at a time, and run ```python3 test.py``` after you have gotten into the directory of the cloned repo. 
