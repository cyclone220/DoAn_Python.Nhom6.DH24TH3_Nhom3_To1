from pathlib import Path

from tkinter import Toplevel, Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
# from controller import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def loginWindow():
    Login()
    
class Login(Toplevel):
    def __init__(self, *args, **kwargs):

        Toplevel.__init__(self, *args, **kwargs)
        self.title("Đăng nhập - Quản lý khách sạn")
    
        
        self.geometry("1012x506")
        
        self.canvas = Canvas(
            self,
            bg="#66A1D1",
            height=506,
            width=1012
        )
        
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            469, 0, 1012, 506, fill="#FFFFFF", outline=""
        )
        
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(736, 331, image=self.entry_image_1)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(736, 229, image=self.entry_image_2)
        
        
        self.canvas.create_text(
            573,
            306,
            anchor="nw",
            text="Mật khẩu",
            fill="#66A1D1",
            font=("Montserrat Bold", 14 * -1),
        )

        self.canvas.create_text(
            573,
            204,
            anchor="nw",
            text="Tên đăng nhập",
            fill="#66A1D1",
            font=("Montserrat Bold", 14 * -1),
        )

        self.canvas.create_text(
            77,
            333,
            anchor="nw",
            text="ĐỒ ÁN ĐƯỢC \nTHỰC HIỆN BỞI",
            fill="#FFFFFF",
            font=("Montserrat Bold", 23 * -1),
        )
        self.canvas.create_text(
            77,
            403,
            anchor="nw",
            text="Đỗ Minh Anh - DTH235831",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 17 * -1),
        )
        
        self.canvas.create_text(
            77,
            425,
            anchor="nw",
            text="Nguyễn Thị Huyền Trân - DTH235791",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 17 * -1),
        )
        
        self.canvas.create_text(
            603,
            77,
            anchor="nw",
            text="    CHƯƠNG TRÌNH \nQUẢN LÝ KHÁCH SẠN",
            fill="#66A1D1",
            font=("Montserrat Bold", 25 * -1),
        )
        
        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16 * -1),
            foreground="#777777",
        )
        self.username.place(x=573, y=229, width=326, height=22)

        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16 * -1),
            foreground="#777777",
            show="•",
        )
        self.password.place(x=573, y=330, width=326, height=22)
        
        self.resizable(False, False)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
            self.destroy()      # đóng cửa sổ login
            self.master.destroy()  # kết thúc root.mainloop()