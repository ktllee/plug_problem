#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
last modified 2023/06/28

@author: katie

function to brute force two (or n) not touch puzzles

dependencies:
    copy.deepcopy
"""

from copy import deepcopy     # to avoid mutability issues on recursion

### helpers

# helper to translate list to list of lists
def expand(board, width = 4):
    return [board[i:i+width] for i in range(0, len(board), width)]

# helper to translate list of lists to list
def collapse(board):
    return [x for sublist in board for x in sublist]

# helper to appropriately add non-star spots around a new star
def star(board, width, height, r_stars, c_stars, r, c):
    ''' takes: a board, with r and c for row and column of new star
        returns: the board, with the star and appropriate non-star spaces
    '''
    # add star
    board[r][c] = 1
    
    # set no-star spaces around, based on whether on edge
    if r != 0:
        board[r - 1][c] = 0             # N
        if c != 0:
            board[r - 1][c - 1] = 0     # NW
            board[r][c - 1] = 0         # W
        if c != (width - 1):
            board[r - 1][c + 1] = 0     # NE
            board[r][c + 1] = 0         # E
    if r != (height - 1):
        board[r + 1][c] = 0             # S
        if c != 0:
            board[r + 1][c - 1] = 0     # SW
        if c != (width - 1):
            board[r + 1][c + 1] = 0     # SE
            
    # set no-star spaces if row or column filled
    if sum(filter(None, board[r])) == r_stars:    # row
        board[r] = [0 if x==None else x for x in board[r]]
    if sum(filter(None, collapse(board)[c::width])) == c_stars:   # column
        for i in range(height):
            if board[i][c] == None: board[i][c] = 0 
    
    return board

### the function
def not_touch(width = 10, height = 10, r_stars = 2, c_stars = 2,
              monitor = False, board = None):
    ''' takes:
            width - int, width of board
            height - int, height of board
            r_stars - int, number of stars per row
            c_stars - int, number of stars per column
            monitor - see live progress
            board - DO NOT USE, variable for recursion
            
        returns:
            list of strings corresponding to solutions for the board size;
            1 = star and 0 = empty, rows then columns.
            
        runs recursively, working left to right then top to bottom;
        sets necessary stars and empty spots after each addition.
        
        note monitor isn't really helpful;
        ! prints when a solution has been found, no matter what;
        monitor = True just gives "-" and "." to see endpoints if curious.
    '''
    
    # should probably set up input checks, but meh.
    
    # set up base board if necessary
    if board==None:
        board = [[None] * width for x in range(height)]
    # list of complete boards
    final = []
    
    # if all spots have been filled - base case
    if not any(None in sublist for sublist in board):
        
        # find marginal sums
        rows = [sum(x) for x in board]
        cols = [sum(x) for x in zip(*board)]
        
        # add to final list if all are correct
        if all(x==r_stars for x in rows) and all(x==c_stars for x in cols):
            final.append(collapse(board))
            print('!', end = '')             # found one!
            
        else:
            if monitor: print('.', end = '') # reached the end of a path.  
    
    # avoid recursion if any row is full of non-stars already
    elif [0]*width in board:
        if monitor: print('-', end = '')     # reached impossibility, cut-
    
    # if there are still spots to fill - recurse
    else:
        
        # find next empty spot
        empty = collapse(board).index(None)
        r = empty // width
        c = empty % width
        
        # option 1 - add star to empty spot
        board_1 = deepcopy(board)
        board_1 = star(board_1, width, height, r_stars, c_stars, r, c)
        final.extend(not_touch(width, height, r_stars, c_stars, monitor, board_1))
        
        # option 2 - place non-star on empty spot
        board_2 = deepcopy(board)
        board_2[r][c] = 0
        final.extend(not_touch(width, height, r_stars, c_stars, monitor, board_2))
    
    # !!! # possible improvement: keep partial final on KeyboardInterrupt
    
    return final



