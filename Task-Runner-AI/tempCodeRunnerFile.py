from functions.get_file_content import get_file_content

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg"))
print(get_file_content("calculator", "/bin"))
print(get_file_content("calculator", "../"))