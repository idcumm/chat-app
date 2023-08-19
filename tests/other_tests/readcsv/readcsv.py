import csv


def set_name(x):
    csvfile = []
    in_i = False

    with open("data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            csvfile.append(row)

    search = x[0]

    for i in csvfile:
        if search in i:
            in_i = True
            index = csvfile.index(i)
            csvfile[index] = x
            break

    if in_i == False:
        csvfile.append(x)

    with open("data.csv", "w", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csvfile)


list = ["192.168.1.29", "jesus"]
set_name(list)
