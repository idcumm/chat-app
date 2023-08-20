towrite = ["guill em", "de vesa"]
for i in towrite:
    if " " in i:
        print("No logeable")
        break
    else:
        print("logeable")
