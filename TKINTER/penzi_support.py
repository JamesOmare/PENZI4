import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import  penzi

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = penzi.Toplevel1(_top1)
    root.mainloop()

Custom = tk.Frame  # To be updated by user with name of custom widget.

if __name__ == '__main__':
    penzi.start_up()




