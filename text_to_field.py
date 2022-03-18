import json
import os


this_path = os.path.dirname(os.path.abspath(__file__)) + "/"
abc = "abcdefghi"


def getnums(string):
    res = ""
    for s in string:
        if str(s).isnumeric():
            res += s
    return res


def write_to_field_hpp():
    old = open(this_path+"field.hpp", "r").read()
    toreplace = old.split("const std::vector<int> sudoku")[1].split("}")[0]
    new = old.replace(
        toreplace, "{" + str(field2).replace("'", "").replace("[", "").replace("]", ""))

    with open(this_path+"field.hpp", "w") as f:
        f.write(new)


field = {}
field2 = []

for i in range(9):

    inputed = input(f"Enter row {i}: ")

    breaks = False

    asnum = list(map(int, getnums(inputed)))

    while True:
        if len(asnum) == 9:
            break

        if len(asnum) == 81:
            breaks = True
            field2 = asnum

            for j, l in enumerate(abc):
                field[l] = asnum[j*9:(j+1)*9]

            break

        print(f"Wrong length ({len(asnum)})")
        inputed = input(f"Enter row {i}: ")
        asnum = list(map(int, getnums(inputed)))

    if breaks:
        break

    field2 += asnum
    field[abc[i]] = asnum


json.dump(field, open(this_path+"field.json", "w"), indent=4)
json.dump(field2, open(this_path+"field2.json", "w"), indent=4)
write_to_field_hpp()

print("Saved")
