from os import path

absolute_path = path.dirname(path.abspath(__file__))
file_path = absolute_path + "/database/data.csv"

print(absolute_path)

print(file_path)
