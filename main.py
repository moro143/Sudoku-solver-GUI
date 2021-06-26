import tkinter as tk
import numpy as np

BOARD = [[0,0,5,4,7,1,3,0,9],
        [0,1,0,0,0,0,0,6,0],
        [0,4,0,0,0,8,1,0,0],
        [0,0,8,0,0,0,0,0,0],
        [0,7,4,0,6,0,8,3,0],
        [0,0,9,5,8,7,0,1,0],
        [3,0,0,0,9,0,0,0,0],
        [7,0,6,0,0,2,9,0,0],
        [4,0,0,8,0,0,2,0,0]]

def is_done(board):
    for i in board:
        for j in i:
            if j==0:
                return False
    return True

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value!=val]

def values_row(board, y):
    values = []
    for v in board[y]:
        if v!=0:
            values.append(v)
    return values

def values_col(board, x):
    values = []
    for v in board:
        if v[x]!=0:
            values.append(v[x])
    return values

def values_box(board, x, y):
    values = []
    for i in range(3):
        for j in range(3):
            if board[3*x+i][3*y+j]!=0:
                values.append(board[3*x+i][3*y+j])
    return values

def step(board):
    flag = False
    table = []
    for i in range(9):
        row = []
        for j in range(9):
            if board[i][j]==0:
                row.append(list(np.arange(1,10)))
            else:
                row.append([])
        table.append(row)

    tmptable = []
    for rowidx in range(len(table)):
        values = values_row(board, rowidx)
        tmprow = []
        for p in table[rowidx]:
            tmp = p
            for v in values:
                tmp = remove_values_from_list(tmp, v)
            tmprow.append(tmp)
        tmptable.append(tmprow)
    table = tmptable

    tmptable = table
    for colidx in range(len(table[0])):
        values = values_col(board, colidx)
        for pidx in range(len(table)):
            tmp = table[pidx][colidx]
            for v in values:
                tmp = remove_values_from_list(tmp, v)
            tmptable[pidx][colidx] = tmp

    tmptable = table
    for x in range(3):
        for y in range(3):
            values = values_box(board, y, x)
            for i in range(3):
                for j in range(3):
                    px = 3*x+i
                    py = 3*y+j
                    tmp = table[py][px]
                    for v in values:
                        tmp = remove_values_from_list(tmp, v)
                    tmptable[py][px] = tmp
    for i in range(len(table)):
        for j in range(len(table[i])):
            if len(table[i][j])==1:
                flag = True
                board[i][j] = table[i][j][0]
                return board, flag, table

    return board, flag, table


def solve(board):
    run = True
    while run:
        board, run, prob = step(board)

    if is_done(board):
        return board

    minlenidx = []
    minlen = 10
    for y in range(len(prob)):
        for x in range(len(prob[y])):
            if minlen>len(prob[y][x])>1:
                minlenidx = [x,y]
                minlen = len(prob[y][x])

    if minlen == 10:
        return board
    
    choices = prob[minlenidx[1]][minlenidx[0]].copy()
    np.random.shuffle(choices)
    for choice in choices:
        tmp = [x[:] for x in board]
        tmp[minlenidx[1]][minlenidx[0]] = choice
        b = solve(tmp)
        if is_done(b):
            return b
    return board

def get_board():
    result = []
    for i in board:
        row = []
        for e in i:
            if e.get()!='':
                row.append(int(e.get()))
            else:
                row.append(0)
        result.append(row)
    return result

def solve_gui():
    sol = solve(get_board())
    for i in range(len(board)):
        for e in range(len(board[i])):
            board[i][e].delete(0)
            board[i][e].insert(0,sol[i][e])


def reset():
    for i in board:
        for e in i:

            e.delete(0)

def is_short(P):
    if len(P) == 0 or len(P) == 1 and P.isdigit() and P!="0":
        return True
    return False

window = tk.Tk()
window.title('Sudoku Solver')
fr_sudoku = tk.Frame(window)
fr_buttons = tk.Frame(window)
short = (window.register(is_short), '%P')
board = []
for i in range(9):
    row = []
    for j in range(9):
        e = tk.Entry(fr_sudoku, validate="key", validatecommand=short, width=2)
        e.grid(row=i, column=j)
        e.insert(0, BOARD[i][j])
        row.append(e)
    board.append(row)

fr_buttons = tk.Frame(window)
btn_solve = tk.Button(fr_buttons, text='Solve', command=solve_gui)
btn_solve.grid(row=0, column=0)
btn_reset = tk.Button(fr_buttons, text='Reset', command=reset)
btn_reset.grid(row=1, column=0)

fr_buttons.grid(row=0, column=1)
fr_sudoku.grid(row=0, column=0)

window.mainloop()