from tkinter import *
from tkinter import ttk

def main(args=None):
    root = Tk()
    ttk.Button(root, text="Hello World").grid()
    root.mainloop()

if __name__ == '__main__':
    main()
