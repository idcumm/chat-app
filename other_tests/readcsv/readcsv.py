import csv

# csvfile = []

# with open("data.csv", "r") as file:
#     csvreader = csv.reader(file)
#     for row in csvreader:
#         csvfile.append(row)

# search = "192.168.1.29"

# for i in csvfile:
#     if search in i:
#         name = i[1]
#         print(f"{search} = {name}")
#         break
#     else:
#         continue
# input()


def assign_name(x):
    csvfile = []
    global name
    name = None

    with open("data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csvfile.append(row)

    search = x

    for i in csvfile:
        if search in i:
            name = i[1]
            print(f"{search} = {name}")
            break
        else:
            continue


joined = "192.168.1.29"
assign_name(joined)
print(name)
input()
