from pathlib import Path
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
    Tk
)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def mainWindow():
    MainWindow()
    
class MainWindow(Toplevel):
    global user
    
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Quản lý khách sạn")

        self.geometry("1012x506")
        self.configure(bg="#5E95FF")

        self.current_window = None
        self.current_window_label = StringVar()
        
        self.canvas = Canvas(
            self,
            bg="#5E95FF",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            215, 0, 1012, 506, fill="#FFFFFF", outline=""
        )

        self.sidebar_indicator = Frame(self, background="#FFFFFF")
        self.sidebar_indicator.place(x=0, y=133, height=47, width=7)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.dashboard_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            # command=lambda: self.handle_btn_press(self.dashboard_btn, "dash"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.dashboard_btn.place(x=7.0, y=133.0, width=208.0, height=47.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.rooms_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            # command=lambda: self.handle_btn_press(self.rooms_btn, "roo"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.rooms_btn.place(x=7.0, y=183.0, width=208.0, height=47.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.guests_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            # command=lambda: self.handle_btn_press(self.guests_btn, "gue"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        
        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.logout_btn = Button(
            self.canvas,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            # command=self.logout,
            relief="flat",
        )
        self.logout_btn.place(x=0.0, y=441.0, width=215.0, height=47.0)

        self.button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        self.reservations_btn = Button(
            self.canvas,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            # command=lambda: self.handle_btn_press(self.reservations_btn, "res"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.reservations_btn.place(x=7.0, y=233.0, width=208.0, height=47.0)
        self.guests_btn.place(x=7.0, y=283.0, width=208.0, height=47.0)
        
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
            self.destroy()      # đóng cửa sổ login
            self.master.destroy()  # kết thúc root.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  
    mainWindow()
    root.mainloop()