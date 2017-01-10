import curses
import sys

import utils
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from curses import wrapper

from cursor import Cursor
from grid import Grid
from soldier import create_soldier, move_soldiers

import signal
import sys

def signal_handler(signal, frame):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Initialize screen and keyboard
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.clear()
curses.curs_set(0)
y_limit = curses.LINES - 1
x_limit = curses.COLS - 1
directions = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]

# open debug file
debug_file = open("debug.out", "w")

def main(stdscr):
    cursor = Cursor(stdscr)
    url = "http://104.131.185.245/token/get"
    token = utils.request(url)['token']
    grid = Grid(stdscr, x_limit, y_limit)
    
    sel_bool = False
    sel_soldiers = []
    
    while True:
        key = stdscr.getch()

        # quit game
        if key == ord('q'):
            exit(stdscr)
    
        # create soldier
        elif key == ord('c'):
            create_soldier(token)
        
        # move cursor
        elif key in directions:
            cursor.move_cursor(key)
        
        # select tiles
        elif key == ord('s'):
            cursor.select()
            key = 0
            # grab tiles
            while key != ord('s') and key != ord('q'):
                stdscr.clear()
                cursor.display()
                grid.display(ord('s'))
                key = stdscr.getch()
                if key in directions:
                    cursor.move_cursor(key)
            # finish selecting
            if key is ord('s'):
                cursor.deselect()
                x_r = sorted((cursor.select_coords[0], cursor.x))
                y_r = sorted((cursor.select_coords[1], cursor.y))
                for x in range(x_r[0], x_r[1]):
                    for y in range(y_r[0], y_r[1]):
                        if (x,y) in grid.grid:
                            sel_soldiers.append(grid.grid[(x,y)])
                sel_bool = True
            if key is ord('q'):
                exit(stdscr)
        
        # move soldiers (soldiers must be selected first)
        elif key == ord('m'):
            key = 69
            if sel_soldiers:
                dest = utils.normalize_coords(cursor.position())
                move_soldiers(dest, sel_soldiers)
                sel_bool = False
        elif key == ord('d'):
            raise Exception(grid.request())
        
        # refresh display
        stdscr.clear()
        grid.debug(str(key))
        #debug_file.write(str(grid.request()))
        debug_file.write("a")
        cursor.display()
        grid.display(key, sel_bool)

# exit the game
def exit(stdscr):
    stdscr.clear()
    stdscr.addstr(y_limit//2, x_limit//2 - 15, "Are you sure you want to quit? (y or n)")
    key = stdscr.getch()
    if key == ord('y'):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        sys.exit(0)

# run the game
curses.wrapper(main)


