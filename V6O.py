import json
import os
from datetime import datetime as dt

ran = list(range(1, 10))

this_path = os.path.dirname(os.path.abspath(__file__)) + "/"


class bc:
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'


def printfield(field: list):

    print(end="    ")
    for i in range(9):
        print(end=f"{i} ")
        if (i+1) % 3 == 0 and i+1 != 9:
            print(end="| ")

    print()
    print("          |       |")

    for i in range(9):

        if (i+1) % 3 == 0 and i+1 != 9:
            print(end=bc.UNDERLINE)

        print(end=f"{i}   ")

        for j in range(9):
            print(end=f"{field[i*9+j]} ")
            if (j+1) % 3 == 0 and j+1 != 9:
                print(end="| ")

        if (i+1) % 3 == 0 and i+1 != 9:
            print(end=bc.ENDC)

        print()


def getusednums_line(field: list, pos: int, possible: set):
    line = pos//9
    for i in range(9):
        possible.discard(field[line*9+i])


def getusednums_col(field: list, pos: int, possible: set):
    col = pos % 9
    for i in range(9):
        possible.discard(field[col+i*9])


def getcluster(pos):

    for line in range(9):

        for col in range(9):

            if line*9+col == pos:
                return (line//3)*3 + col//3


def clustertooffset(pos_cluster: int):

    if pos_cluster == 0:
        offset = 0
    elif pos_cluster == 1:
        offset = 3
    elif pos_cluster == 2:
        offset = 6
    elif pos_cluster == 3:
        offset = 27
    elif pos_cluster == 4:
        offset = 30
    elif pos_cluster == 5:
        offset = 33
    elif pos_cluster == 6:
        offset = 54
    elif pos_cluster == 7:
        offset = 57
    elif pos_cluster == 8:
        offset = 60

    return offset


def getusednums_cluster(field: list, pos: int, possible: set):
    pos_cluster = getcluster(pos)
    offset = clustertooffset(pos_cluster)

    for _ in range(3):
        for x in range(3):
            possible.discard(field[offset+x])
        offset += 9


def getunusednums(field: list, pos: int):

    posiblenums = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    getusednums_line(field, pos, posiblenums)
    getusednums_col(field, pos, posiblenums)
    getusednums_cluster(field, pos, posiblenums)

    return posiblenums


def loadfield():
    return json.load(open(this_path+"field2.json", "r"))


def is_solved(sudoku):

    if 0 in sudoku:
        return False

    for i in range(9):

        line = i // 9

        if sudoku[line*9:(line+1)*9].count(i+1) > 1:
            return False

        sudocol = []
        for j in range(9):
            col = i % 9
            sudocol.append(sudoku[col+j*9])

        for j in range(9):
            if sudocol.count(j+1) > 1:
                return False

        sudoclust = []

        offset = clustertooffset(i)

        for _ in range(3):
            for x in range(3):
                sudoclust.append(sudoku[offset+x])
            offset += 9

        for j in range(9):
            if sudoclust.count(j+1) > 1:
                return False

    return True


def loese_sudoku(sudoku: dict, field_pos=0):

    if field_pos == 81:
        if is_solved(sudoku):
            return sudoku.copy()
        return []

    if sudoku[field_pos] != 0:
        return loese_sudoku(sudoku, field_pos+1)

    moeglichkeiten = getunusednums(
        sudoku, field_pos)

    for m in moeglichkeiten:

        sudoku[field_pos] = m
        res = loese_sudoku(sudoku, field_pos+1)
        sudoku[field_pos] = 0

        if res == []:
            continue

        return res

    return []


def main():

    print("Starting field:\n")
    printfield(loadfield())
    print("\n")

    start = dt.now()
    solved = loese_sudoku(loadfield())
    end = dt.now()
    print(f"{solved!=[]}, took {end-start}")
    if solved != []:
        printfield(solved)


if __name__ == "__main__":
    main()
