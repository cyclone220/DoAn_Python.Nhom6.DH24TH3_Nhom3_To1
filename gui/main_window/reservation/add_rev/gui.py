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


def add_rooms():
    AddRev()


class AddRev(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data = {"SoPhong": StringVar(), "MaKH": StringVar(), "CheckIn": StringVar()}
        
        self.configure(bg="#FFFFFF")
        
        # Lưu toàn bộ danh sách phòng và khách
        self.all_rooms = []
        self.all_guests = []


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
        self.canvas.place(x=0, y=0)
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(137.5, 153.0, image=self.entry_image_1)

        self.canvas.create_text(
            52.0,
            128.0,
            anchor="nw",
            text="Loại phòng ",
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
            text="Khách hàng",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(141.5, 271.0, image=self.entry_image_4)


        self.entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
        self.entry_bg_5 = self.canvas.create_image(378.5, 153.0, image=self.entry_image_5)

        self.canvas.create_text(
            293.0,
            128.0,
            anchor="nw",
            text="Số phòng",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
        self.entry_bg_6 = self.canvas.create_image(382.5, 165.0, image=self.entry_image_6)

        self.entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
        entry_bg_7 = self.canvas.create_image(378.5, 259.0, image=self.entry_image_7)
        self.canvas.create_text(
            293.0,
            234.0,
            anchor="nw",
            text="Ngày nhận phòng",
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
        # --- Combobox chọn loại phòng ---
        self.cmb_type = ctk.CTkComboBox(
            self,
            values=["Đơn", "Đôi", "Vip"],
            width=152,
            height=20,
            corner_radius=0,
            border_width=0,
            fg_color="#efefef",
            button_color="#efefef",
            text_color="#333333",
            dropdown_fg_color="white",
            dropdown_text_color="#333333",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
            command=self.load_available_rooms
        )
        self.cmb_type.place(x=52.0, y=153.0)
        self.cmb_type.set("Chọn loại phòng")


        # --- Combobox chọn phòng ---

        self.cmb_room = ctk.CTkComboBox(
            self,
            state="readonly",
            width=152,
            height=20,
            corner_radius=0,
            border_width=0,
            fg_color="#efefef",
            button_color="#efefef",
            text_color="#333333",
            dropdown_fg_color="white",
            dropdown_text_color="#333333",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
            
        )
        self.cmb_room.place(x=293.0, y=153.0)
        self.cmb_room.set("Chọn phòng")


        # --- Combobox chọn khách hàng ---

        self.cmb_guest = ctk.CTkComboBox(
            self,
            state="readonly",
            width=152,
            height=20,
            corner_radius=0,
            border_width=0,
            fg_color="#efefef",
            button_color="#efefef",
            text_color="#333333",
            dropdown_fg_color="white",
            dropdown_text_color="#333333",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
        )
        self.cmb_guest.place(x=52.0, y=259.0)
        self.cmb_guest.set("Chọn khách hàng")

        self.load_guests()

        # --- Ngày Check-in ---
        self.entry_checkin = DateEntry(
            self,
            textvariable=self.data["CheckIn"],
            width=18,
            background="#004080",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd" 
            
        )
        self.entry_checkin.place(x=293.0, y=259.0)

        # # --- Ngày Check-out ---
        # self.entry_checkout = DateEntry(
        #     self,
        #     textvariable=self.data["CheckOut"],
        #     width=18,
        #     background="#5E95FF",
        #     foreground="white",
        #     borderwidth=2,
        #     date_pattern="yyyy-mm-dd"
        # )
        # self.entry_checkout.place(x=180, y=215)
        # Sau khi UI được tạo xong
        self.load_all_data()


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

    # ------------------------------------------------
    # Refresh dữ liệu
    # ------------------------------------------------
    def load_all_data(self):
        # Lấy toàn bộ phòng
        self.all_rooms = db_controller.get_rooms() or []
        # Lấy toàn bộ khách
        self.all_guests = db_controller.get_guests() or []

        # Cập nhật combobox khách hàng
        self.load_guests()
        if self.cmb_type.get():
            # dùng load_available_rooms để lọc từ self.all_rooms
            self.load_available_rooms()
        else:
            # nếu muốn hiển thị tất cả phòng trống theo default (tùy bạn)
            # self.load_available_rooms()  # hoặc leave cmb_room empty
            pass
        
    def reset_combobox(combo, placeholder=""):
        # Xóa giá trị hiện tại và danh sách trong combobox
        combo.set(placeholder)
        combo.configure(values=[])

    # ------------------------------------------------
    # Nạp danh sách khách hàng vào combobox
    # ------------------------------------------------
    def load_guests(self):
        if not self.all_guests:
            return
        self.guest_map = {f"{g[0]} - {g[1]}": g[0] for g in self.all_guests}
    
        # Lấy danh sách hiển thị cho combobox
        display = list(self.guest_map.keys())
        self.cmb_guest.configure(values=display)
        
        # Giá trị mặc định
        if display:
            self.cmb_guest.set(display[0])


    # ------------------------------------------------
    # Nạp danh sách phòng còn trống theo loại
    # ------------------------------------------------
    def load_available_rooms(self, event=None):
        loaiphong = {
                "đơn": "don",
                "đôi": "doi",
                "vip": "vip"
            }
        loai = loaiphong.get(self.cmb_type.get().lower())
        available_rooms = [
            r for r in self.all_rooms
            if r[2] == loai and r[4] == 1  # 1 = còn trống
        ]

        if not available_rooms:
            self.cmb_room.configure(values=["(Không có phòng trống)"])
            self.room_map = {}
            return

        formatted = [f"{r[1]}" for r in available_rooms]
        self.cmb_room.configure(values=formatted)
        self.room_map = {f"{r[1]}": r[0] for r in available_rooms}
        self.cmb_room.set(formatted[0])

    # Save the data to the database
    def save(self):
        # Kiểm tra dữ liệu trống
        if not self.cmb_room.get() or not self.cmb_guest.get() \
        or not self.entry_checkin.get():
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Lấy MaPhong từ phòng đã chọn
        selected_room = self.cmb_room.get()
        MaPhong = self.room_map.get(selected_room)
        if MaPhong is None:
            messagebox.showerror("Lỗi", "Phòng chọn không hợp lệ!")
            return
        if MaPhong is None:
            messagebox.showerror("Lỗi", "Phòng chọn không hợp lệ!")
            return

        # Lấy MaKH từ guest_map
        selected_guest = self.cmb_guest.get()  # "ID - Tên"
        MaKH = self.guest_map.get(selected_guest)
        if MaKH is None:
            messagebox.showerror("Lỗi", "Khách hàng chọn không hợp lệ!")
            return

        # Lấy ngày checkin 
        CheckIn = self.entry_checkin.get()

        try:
            # Gọi hàm add_reservation trong controller
            result = db_controller.add_reservation(MaPhong, MaKH, CheckIn)

            if result:
                messagebox.showinfo(None, "Đặt phòng thành công")
                # self.parent.navigate("view")
                self.parent.refresh_entries()
            else:
                messagebox.showerror("Lỗi", "Đặt phòng thất bại. Vui lòng kiểm tra lại thông tin.")

        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Database error: {str(e)}")