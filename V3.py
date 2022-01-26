import random
import json
import os 


this_path = os.path.dirname(os.path.abspath(__file__)) + "\\"

class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def convert_tonum(field):
    field_num1 = {}
    for i in ran:
        temp = []
        for j in range(9):
            temp.append(field[abc[j]][i-1])

        field_num1.update({i: temp})
    return field_num1


def convert_tocluster(field_num):
    field_cluster1 = {}
    for h in ran:
        cluster = []
        xp = 0
        yp = 0

        if h in (2, 5, 8):
            xp = 3
        elif h in (3, 6, 9):
            xp = 6

        if h in (4, 5, 6):
            yp = 3
        elif h in (7, 8, 9):
            yp = 6

        for i in range(3):
            for j in range(1, 4):
                cluster.append(field_num[j+xp][i+yp])
        field_cluster1.update({h: cluster})

    return field_cluster1


def printfield(field: dict):

    print(end="    ")

    for i in ran:
        if i in (4, 7):
            print("| ", end="")
        print(i, end=" ")

    print()
    print("          |       |")

    for l in field:

        c = 1

        if l in ("c", "f"):
            print(end=bc.UNDERLINE)

        if l in ("d", "g"):
            print(end=bc.ENDC)

        cc = 1
        for i in field[l]:

            if c == 1:
                print(l, end="   ")

            if cc == 9:
                print(i, end="")
            else:
                print(i, end=" ")

            if c in (3, 6):
                print("| ", end="")

            if c == 9:
                print()

            c += 1
            cc += 1


def getunusednums_line(field: dict, line: str):
    res = []
    for i in ran:
        if i in field[line]:
            res.append(i)
    return res


def getunusednums_row(field_num: dict, row: int):
    res = []
    for i in ran:
        if i in field_num[row]:
            res.append(i)
    return res


def getunusednums_cluster(field_cluster: dict, cluster: int):
    res = []
    for i in ran:
        if i in field_cluster[cluster]:
            res.append(i)
    return res


def getunusednums(field: dict, field_num: dict, field_cluster: dict, cluster: int, line: str, row: int):
    posiblenums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    if field[line][row-1] != 0:
        return []

    unusednums_line = getunusednums_line(field, line)
    unusednums_row = getunusednums_row(field_num, row)
    unusednums_cluster = getunusednums_cluster(field_cluster, cluster)

    for i in unusednums_line:
        if i in posiblenums:
            posiblenums.remove(i)
    for i in unusednums_cluster:
        if i in posiblenums:
            posiblenums.remove(i)
    for i in unusednums_row:
        if i in posiblenums:
            posiblenums.remove(i)

    return posiblenums


def fillsures(field: dict, possibilities: dict):
    for l in abc:
        for i in ran:
            if len(possibilities[l][i]) == 1:
                field[l][i-1] = possibilities[l][i][0]
                return field, True
    return field, False


def random_fill(field: dict, possibilities: dict):
    min_len = 10
    index_l = ""
    index_i = 0

    for l in possibilities:
        for i in possibilities[l]:
            if len(possibilities[l][i]) < min_len and len(possibilities[l][i]) != 0:
                min_len = len(possibilities[l][i])
                index_l, index_i = l, i

    rand_ind = random.randint(0, len(possibilities[index_l][index_i])-1)

    field1 = field.copy()
    field1[index_l][index_i-1] = possibilities[index_l][index_i][rand_ind]

    possibilities1 = possibilities.copy()
    possibilities1[index_l][index_i] = possibilities[index_l][index_i][rand_ind]

    return field1, possibilities1


def check(field):
    for l in field:
        for i in field[l]:
            if i == 0:
                return False
    return True


def loadfield():
    return json.load(open(this_path+"field.json", "r"))


def main(field, field_num, field_cluster, possibilities):
    for l in abc:
        for i in ran:

            if l in ("a", "b", "c"):
                if i <= 3:
                    c = 1
                elif i > 3 and i < 7:
                    c = 2
                else:
                    c = 3
            elif l in ("d", "e", "f"):
                if i <= 3:
                    c = 4
                elif i > 3 and i < 7:
                    c = 5
                else:
                    c = 6
            else:
                if i <= 3:
                    c = 7
                elif i > 3 and i < 7:
                    c = 8
                else:
                    c = 9

            possibilities[l][i] = getunusednums(
                field, field_num, field_cluster, c, l, i)

    field, filled_one = fillsures(field, possibilities)

    if not filled_one:
        field, possibilities = random_fill(field, possibilities)

    field_num = convert_tonum(field)
    field_cluster = convert_tocluster(field_num)

    return field, field_num, field_cluster, possibilities


if __name__ == "__main__":

    abc = "abcdefghi"
    ran = list(range(1, 10))

    field = loadfield()

    field_num = convert_tonum(field)
    field_cluster = convert_tocluster(field_num)

    og_possibilities = {}

    for l in abc:
        og_possibilities.update({l: {}})
        for i in ran:
            og_possibilities[l].update({i: []})

    possibilities = og_possibilities.copy()

    solved = check(field)

    while not solved:
        try:
            field, field_num, field_cluster, possibilities = main(
                field, field_num, field_cluster, possibilities)
            solved = check(field)
        except KeyError:

            field = loadfield()
            field_num = convert_tonum(field)
            field_cluster = convert_tocluster(field_num)
            possibilities = og_possibilities.copy()

    print("Starting field:\n")
    printfield(loadfield())

    print("\n")

    print("Solved field:\n")
    printfield(field)
