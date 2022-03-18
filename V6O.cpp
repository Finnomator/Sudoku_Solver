#include "field.hpp"

using namespace std;
using chrono::duration;
using chrono::duration_cast;
using chrono::high_resolution_clock;
using chrono::milliseconds;

const string ENDC = "\033[0m";
const string UNDERLINE = "\033[4m";

void printfield(const vector<int> &field)
{
    cout << "    ";
    for (int i = 0; i < 9; i++)
    {
        cout << i << " ";
        if ((i + 1) % 3 == 0 && i + 1 != 9)
        {
            cout << "| ";
        }
    }
    cout << "\n";
    cout << "          |       |\n";

    for (int i = 0; i < 9; i++)
    {
        if ((i + 1) % 3 == 0 && i + 1 != 9)
        {
            cout << UNDERLINE;
        }

        cout << i << "   ";

        for (int j = 0; j < 9; j++)
        {
            cout << field[i * 9 + j] << " ";
            if ((j + 1) % 3 == 0 && j + 1 != 9)
            {
                cout << "| ";
            }
        }

        if ((i + 1) % 3 == 0 && i + 1 != 9)
        {
            cout << ENDC;
        }

        cout << "\n";
    }
}

void getusednums_line(const vector<int> &field, const int pos, set<int> &possiblenums)
{
    int line = floor(pos / 9);
    for (int i = 0; i < 9; i++)
    {
        possiblenums.erase(field[line * 9 + i]);
    }
}

void getusednums_col(const vector<int> &field, const int pos, set<int> &possiblenums)
{
    int col = pos % 9;
    for (int i = 0; i < 9; i++)
    {
        possiblenums.erase(field[col + i * 9]);
    }
}

int getcluster(const int &pos)
{
    for (int line = 0; line < 9; line++)
    {
        for (int col = 0; col < 9; col++)
        {
            if (line * 9 + col == pos)
            {
                return floor(line / 3) * 3 + floor(col / 3);
            }
        }
    }
    return -1;
}

int clustertooffset(const int pos_cluster)
{
    switch (pos_cluster)
    {
    case 0:
        return 0;
    case 1:
        return 3;
    case 2:
        return 6;
    case 3:
        return 27;
    case 4:
        return 30;
    case 5:
        return 33;
    case 6:
        return 54;
    case 7:
        return 57;
    case 8:
        return 60;
    }

    return -1;
}

void getusednums_cluster(const vector<int> &field, const int pos, set<int> &possiblenums)
{
    int pos_cluster = getcluster(pos);
    int offset = clustertooffset(pos_cluster);

    for (int _ = 0; _ < 3; _++)
    {
        for (int x = 0; x < 3; x++)
        {
            possiblenums.erase(field[offset + x]);
        }
        offset += 9;
    }
}

set<int> getunusednums(const vector<int> &field, const int pos)
{
    set<int> possiblenums = {1, 2, 3, 4, 5, 6, 7, 8, 9};

    getusednums_line(field, pos, possiblenums);
    getusednums_col(field, pos, possiblenums);
    getusednums_cluster(field, pos, possiblenums);

    return possiblenums;
}

bool is_solved(const vector<int> &sudoku)
{
    for (int i = 0; i < 9; i++)
    {
        if (sudoku[i] == 0)
        {
            return false;
        }

        int line = floor(i / 9);

        vector<int> tempsud(9);
        for (int j = line * 9; j < (line + 1) * 9; j++)
        {
            tempsud[j - line * 9] = sudoku[j];
        }

        if (count(tempsud.begin(), tempsud.end(), i + 1) > 1)
        {
            return false;
        }

        vector<int> sudcol(9);

        for (int j = 0; j < 9; j++)
        {
            int col = i % 9;
            sudcol[j] = sudoku[col + j * 9];
        }

        for (int j = 0; j < 9; j++)
        {
            if (count(sudcol.begin(), sudcol.end(), j + 1) > 1)
            {
                return false;
            }
        }

        vector<int> sudclust(9);
        int offset = clustertooffset(i);

        for (int _ = 0; _ < 3; _++)
        {
            for (int x = 0; x < 3; x++)
            {
                sudclust[x] = sudoku[offset + x];
            }
            offset += 9;
        }

        for (int j = 0; j < 9; j++)
        {
            if (count(sudclust.begin(), sudclust.end(), j + 1) > 1)
            {
                return false;
            }
        }
    }
    return true;
}

vector<int> loese_sudoku(vector<int> sudoku, int field_pos = 0)
{
    if (field_pos == 81)
    {
        if (is_solved(sudoku))
        {
            return vector<int>(sudoku);
        }
        return vector<int>({});
    }

    if (sudoku[field_pos] != 0)
    {
        return loese_sudoku(sudoku, field_pos + 1);
    }

    set<int> moeglichkeiten = getunusednums(sudoku, field_pos);

    for (int m : moeglichkeiten)
    {
        sudoku[field_pos] = m;
        vector<int> res = loese_sudoku(sudoku, field_pos + 1);
        sudoku[field_pos] = 0;
        if (res.size() == 0)
        {
            continue;
        }

        return res;
    }

    return vector<int>({});
}

int main()
{
    cout << "Starting field:\n";
    printfield(sudoku);

    auto t1 = high_resolution_clock::now();
    vector<int> res = loese_sudoku(sudoku);

    auto t2 = high_resolution_clock::now();

    duration<double, milli> ms_double = t2 - t1;

    bool solved = res.size() != 0;
    cout << "\nSolved: " << solved << ", in " << ms_double.count() / 1000 << "s\n";
    if (solved)
    {
        printfield(res);
    }
    return 0;
}