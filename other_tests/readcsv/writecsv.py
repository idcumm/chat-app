import csv


def set_name(x):
    csvfile = []
    global name
    name = None

    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            csvfile.append(row)

    print(csvfile)
    csvfile.append(x)
    print(csvfile)

    with open("data.csv", "w", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csvfile)


address = "192.168.1.1"
name = "Pere Devesa"
readytowrite = [address, name]
set_name(readytowrite)
