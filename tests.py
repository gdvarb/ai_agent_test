#todo make tests for get_files_info.py
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

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

print("Results for main.py")
get_file_content("calculator", 'main.py')
print("Results for pkg/calculator.py")
get_file_content("calculator", 'pkg/calculator.py')
print("Results for /bin/cat")
get_file_content("calculator", '/bin/cat')
print("Results for pkg/does_not_exist.py")
get_file_content("calculator", 'pkg/does_not_exist.py')
