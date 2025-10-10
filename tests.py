#todo make tests for get_files_info.py
from functions.tools import *
#print("Results for current directory:")
#get_files_info("calculator", ".")
#
#print("Results for 'pkg' directory")
#get_files_info("calculator", "pkg")
#
#print("Results for '/bin' directory")
#get_files_info("calculator", "/bin")
#
#print("Results for '../' directory")
#get_files_info("calculator", "../")

#print("Results for main.py")
#get_file_content("calculator", 'main.py')
#print("Results for pkg/calculator.py")
#get_file_content("calculator", 'pkg/calculator.py')
#print("Results for /bin/cat")
#get_file_content("calculator", '/bin/cat')
#print("Results for pkg/does_not_exist.py")
#get_file_content("calculator", 'pkg/does_not_exist.py')


#print("Results for write calculator, lorem.txt")
#write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
#print("Results for write calculator/pkg/morelorem.txt")
#write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
#print("Results for write calculator/tmp/temp.txt")
#write_file("calculator", "/tmp/temp.txt", "this should not be allowed")


run_python_file("calculator", "main.py")
run_python_file("calculator", "main.py", ["3 + 5"])
run_python_file("calculator", "tests.py")
run_python_file("calculator", "../main.py")
run_python_file("calculator", "nonexistent.py")

