from make_glob_list import make_glob # for listing out files in a folder to pass to WT Forms. REQUIRES PYTHON3
import re
# Produce list of books to pass to WTFORMS as LIST of value/label TUPLES
def wtform_tuple_creator(func):
    def func_wrapper(folder_path,filetype):
        list_of_paths=func(folder_path,filetype)
        list_of_path_tuples = []
        for file_path in list_of_paths:
            filename = re.search('[^\/]*\.'+filetype,file_path).group(0)
            list_of_path_tuples.append((
            file_path,
            filename
            ))
        return(list_of_path_tuples)
    return(func_wrapper)

#No syntactic sugar with the fancy @ symbols and whatnot
make_glob_list_to_wtforms_tuple = wtform_tuple_creator(make_glob)

for tuple in make_glob_list_to_wtforms_tuple('./wordlists','txt'):
    print(tuple)

# print(make_glob_list_to_wtforms_tuple('./wordlists','txt'))
