import csv

list = []

with open("data.csv", "r") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        list.append(row)

search = "192.168.1.81"

for i in list:
    if search in i:
        name = i[1]
        print(f"{search} = {name}")
        break
    else:
        continue
input()
