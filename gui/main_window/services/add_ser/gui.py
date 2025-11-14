from pathlib import Path

from tkinter import (
    Frame,
    Canvas,
    Entry,
    StringVar,
    Text,
    Button,
    PhotoImage,
    messagebox,
    ttk
)
import customtkinter as ctk
from tkcalendar import DateEntry
import mysql.connector
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def add_ser():
    AddSer()


class AddSer(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data = {"MaHD": StringVar(), "MaDV": int, "SoLuong": int}
        
        self.configure(bg="#FFFFFF")


        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=432,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(137.5, 153.0, image=self.entry_image_1)

        self.canvas.create_text(
            52.0,
            128.0,
            anchor="nw",
            text="Mã hoá đơn:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(141.5, 165.0, image=self.entry_image_2)


        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(137.5, 259.0, image=self.entry_image_3)

        self.canvas.create_text(
            52.0,
            234.0,
            anchor="nw",
            text="Dịch vụ:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(141.5, 271.0, image=self.entry_image_4)

        self.entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
        self.entry_bg_7 = self.canvas.create_image(378.5, 259.0, image=self.entry_image_7)
        self.canvas.create_text(
            293.0,
            234.0,
            anchor="nw",
            text="Số lượng:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        
        self.canvas.create_rectangle(
            515.0, 59.0, 517.0, 370.0, fill="#EFEFEF", outline=""
        )
        self.canvas.create_text(
            549.0,
            59.0,
            anchor="nw",
            text="Tác vụ",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_rectangle(
            515.0, 59.0, 517.0, 370.0, fill="#EFEFEF", outline=""
        )

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("view"),
            relief="flat",
        )
        button_2.place(x=547.0, y=116.0, width=209.0, height=74.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit"),
            relief="flat",
        )
        button_3.place(x=547.0, y=210.0, width=209.0, height=74.0)
        # --- Combobox chọn Mã hoá đơn ---
        self.cmb_ID = ctk.CTkComboBox(
            self,
            width=152,
            height=20,
            corner_radius=0,
            border_width=0,
            fg_color="#efefef",
            button_color="#efefef",
            text_color="#777777",
            dropdown_fg_color="white",
            dropdown_text_color="#777777",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
        )
        self.cmb_ID.place(x=52.0, y=153.0)
        self.cmb_ID.set("Chọn Mã hoá đơn")
        self.load_hoadon()

        
        # --- Combobox chọn dịch vụ ---

        self.cmb_service = ctk.CTkComboBox(
            self,
            state="readonly",
            width=152,
            height=20,
            corner_radius=0,
            border_width=0,
            fg_color="#efefef",
            button_color="#efefef",
            text_color="#777777",
            dropdown_fg_color="white",
            dropdown_text_color="#777777",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
        )
        self.cmb_service.place(x=52.0, y=259.0)
        self.cmb_service.set("Chọn dịch vụ")

        self.load_dichvu()
        self.entry_SL = Entry(
            self,
            textvariable=self.data["SoLuong"],
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat SemiBold", 14),
            foreground="#777777",
            width=10
        )
        self.entry_SL.place(x=293.0, y=259.0)

        # Sau khi UI được tạo xong
        self.canvas.create_text(
            181.0,
            58.0,
            anchor="nw",
            text="Thêm dịch vụ",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save,
            relief="flat",
        )
        self.button_1.place(x=164.0, y=322.0, width=190.0, height=48.0)

    def reset_combobox(combo, placeholder=""):
        # Xóa giá trị hiện tại và danh sách trong combobox
        combo.set(placeholder)
        combo.configure(values=[])

    def load_hoadon(self):
        # Lấy tất cả MaHoaDon từ database
        hoadon_list = db_controller.get_HoaDon() 
        if not hoadon_list:
            return

        # Tạo danh sách hiển thị
        self.hoadon_map = {str(h[0]): h[0] for h in hoadon_list}  # key = string hiển thị, value = MaHoaDon

        display = list(self.hoadon_map.keys())
        self.cmb_ID.configure(values=display)

        # Giá trị mặc định
        if display:
            self.cmb_ID.set(display[0])


    def load_dichvu(self):
        # Lấy danh sách dịch vụ từ database
        services = db_controller.get_DichVu()  # trả về [(1, 'Giặt ủi'), (2, 'Ăn sáng'), ...]
        if not services:
            return

        # Tạo map để hiển thị: key = tên dịch vụ, value = MaDV
        self.dichvu_map = {name: ma for ma, name in services}

        # Danh sách hiển thị cho combobox
        display = list(self.dichvu_map.keys())
        self.cmb_service.configure(values=display)

        # Giá trị mặc định
        if display:
            self.cmb_service.set(display[0])

    # Save the data to the database
    def save(self):
        # Lấy MaHoaDon từ combobox
        ma_hoadon = self.cmb_ID.get()
        if not ma_hoadon:
            messagebox.showerror("Lỗi", "Vui lòng chọn mã hóa đơn.")
            return

        # Lấy tên dịch vụ từ combobox và tra MaDV
        selected_name = self.cmb_service.get()
        if not selected_name:
            messagebox.showerror("Lỗi", "Vui lòng chọn dịch vụ.")
            return

        ma_dv = self.dichvu_map.get(selected_name)
        if not ma_dv:
            messagebox.showerror("Lỗi", "Dịch vụ không hợp lệ.")
            return

        # Lấy số lượng
        try:
            so_luong = int(self.entry_SL.get())
            if so_luong <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số nguyên lớn hơn 0.")
            return

        # Thêm vào bảng hoadon
        try:
            db_controller.add_DichVu(ma_hoadon,ma_dv,so_luong)
            messagebox.showinfo("Thành công", "Thêm dịch vụ vào hóa đơn thành công.")
            # Nếu muốn refresh lại giao diện sau khi thêm
            self.load_hoadon_details()  # ví dụ hàm load chi tiết hóa đơn
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể thêm dịch vụ: {str(e)}")
