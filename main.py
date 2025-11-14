import tkinter as tk
from gui.login.gui import loginWindow
from gui.main_window.main import mainWindow


root = tk.Tk()  
root.withdraw() # Thu nhỏ cửa sổ root


if __name__ == "__main__":
    loginWindow()

    root.mainloop()
    