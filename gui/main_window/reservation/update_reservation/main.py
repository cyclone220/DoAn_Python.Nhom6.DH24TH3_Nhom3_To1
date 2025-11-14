from pathlib import Path

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Text,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
import customtkinter as ctk
from tkcalendar import DateEntry
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def update_reservations():
    UpdateReservations()


class UpdateReservations(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_r_id = self.parent.selected_rid

        self.configure(bg="#FFFFFF")

        self.data = {
            "MaHD": StringVar(),
            "SoPhong":StringVar(),
            "HoTen": StringVar(),
            "NgayCheckin": StringVar()
        }


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
        self.canvas.create_rectangle(
            40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_text(
            116.0,
            33.0,
            anchor="nw",
            text="Cập nhật thông tin đặt phòng",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )
        
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("add"),
            relief="flat",
        )
        self.button_1.place(x=40.0, y=33.0, width=53.0, height=53.0)
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(206.0, 170.0, image=self.image_image_1)

        self.canvas.create_text(
            71.56398010253906,
            145.0,
            anchor="nw",
            text="Mã hoá đơn:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )
        self.id_text = self.canvas.create_text(
            71.56398010253906, 170.0,
            anchor="nw",
            text="",
            fill="#777777",
            font=("Montserrat Bold", 18 * -1),
        )


        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(206.0, 276.0, image=self.image_image_2)

        self.canvas.create_text(
            71.56398010253906,
            251.0,
            anchor="nw",
            text="Khách hàng:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            212.8127899169922, 288.0, image=self.entry_image_1
        )

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(583.0, 170.0, image=self.image_image_3)

        self.canvas.create_text(
            455.0473937988281,
            145.0,
            anchor="nw",
            text="Số phòng:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(589.5, 182.0, image=self.entry_image_2)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(583.0, 278.0, image=self.image_image_4)

        self.canvas.create_text(
            455.0473937988281,
            253.0,
            anchor="nw",
            text="Ngày nhận phòng",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(
            589.5094757080078, 290.0, image=self.entry_image_3
        )

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
            text_color="#777777",
            dropdown_fg_color="white",
            dropdown_text_color="#777777",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
            
        )
        self.cmb_room.place(x=455.0, y=170.0)
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
            text_color="#777777",
            dropdown_fg_color="white",
            dropdown_text_color="#777777",
            dropdown_hover_color="#E3EBFF",
            font=("Montserrat SemiBold", 14),
        )
        self.cmb_guest.place(x=71.56398010253906, y=276.0)
        self.cmb_guest.set("Chọn khách hàng")

        # --- Ngày Check-in ---
        self.entry_checkin = DateEntry(
            self,
            # textvariable=self.data["CheckIn"],
            width=18,
            background="#004080",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd" 
            
        )
        self.entry_checkin.place(x=455.0473937988281, y=278.0)
        
        self.initialize()

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_update,
            relief="flat",
        )
        self.button_2.place(x=326.0, y=339.0, width=144.0, height=48.0)

    def load_guest_map(self):

        # Lấy danh sách khách hàng
        self.all_guests = db_controller.get_guests()  # trả về [(MaKH, HoTen, ...), ...]

        if not self.all_guests:
            self.guest_map = {}
            self.cmb_guest.configure(values=[])
            self.cmb_guest.set("Chọn khách hàng")
            return

        # Tạo map: key hiển thị, value là MaKH
        self.guest_map = {f"{g[0]} - {g[1]}": g[0] for g in self.all_guests}

        # Danh sách hiển thị cho combobox
        display = list(self.guest_map.keys())
        self.cmb_guest.configure(values=display)

        # Giá trị mặc định (nếu có)
        if display:
            self.cmb_guest.set(display[0])
            
    def load_room_map(self):

        # Lấy danh sách phòng
        self.all_rooms = db_controller.get_rooms()  # trả về [(MaPhong, LoaiPhong, ConTrong, ...), ...]

        if not self.all_rooms:
            self.room_map = {}
            self.cmb_room.configure(values=[])
            self.cmb_room.set("Chọn phòng")
            return

        # Tạo map: key hiển thị, value là MaPhong
        self.room_map = {f"{r[0]} - {r[1]}": r[0] for r in self.all_rooms}

        # Danh sách hiển thị cho combobox
        display = list(self.room_map.keys())
        self.cmb_room.configure(values=display)

        # Giá trị mặc định (nếu có)
        if display:
            self.cmb_room.set(display[0])


    def initialize(self):
        self.selected_r_id = self.parent.selected_rid
        self.reservation_data = self.parent.reservation_data

        # Load combobox maps
        self.load_guest_map()
        self.load_room_map()

        # Lọc dữ liệu reservation
        self.selected_reservation_data = list(
            filter(lambda x: str(x[0]) == self.selected_r_id, self.reservation_data)
        )

        if self.selected_reservation_data:
            self.selected_reservation_data = self.selected_reservation_data[0]

            # Cập nhật mã reservation lên canvas
            self.canvas.itemconfigure(self.id_text, text=self.selected_reservation_data[0])

            # Điền giá trị phòng
            ma_phong = self.selected_reservation_data[1]
            for display_text, room_id in self.room_map.items():
                if room_id == ma_phong:
                    self.cmb_room.set(display_text)
                    break

            # Điền giá trị khách hàng
            ma_kh = self.selected_reservation_data[2]
            for display_text, kh_id in self.guest_map.items():
                if kh_id == ma_kh:
                    self.cmb_guest.set(display_text)
                    break

            # Điền giá trị ngày check-in
            self.entry_checkin.set_date(self.selected_reservation_data[3])



    def handle_update(self):
        if not self.selected_r_id:
            messagebox.showwarning(None, "Không có hoá đơn được chọn để cập nhật")
            return

        # Lấy MaPhong từ room_map dựa trên combobox
        room_text = self.cmb_room.get()
        ma_phong = self.room_map.get(room_text)
        if not ma_phong:
            messagebox.showerror(None, "Vui lòng chọn phòng hợp lệ")
            return

        # Lấy MaKH từ guest_map dựa trên combobox
        guest_text = self.cmb_guest.get()
        ma_kh = self.guest_map.get(guest_text)
        if not ma_kh:
            messagebox.showerror(None, "Vui lòng chọn khách hàng hợp lệ")
            return

        # Lấy ngày check-in
        check_in_date = self.entry_checkin.get_date()

        # Thực hiện update
        success = db_controller.update_reservation(
            self.selected_r_id,
            ma_phong,
            ma_kh,
            check_in_date
        )

        if success:
            messagebox.showinfo("Thành công", "Cập nhật đặt phòng thành công")
            self.parent.navigate("view")
            self.parent.refresh_entries()
            self.reset()
        else:
            messagebox.showerror("Lỗi", "Cập nhật thất bại. Vui lòng kiểm tra dữ liệu")

    def reset(self):
        # clear all entries
        for label in self.data:
            self.data[label].set("")

        self.canvas.itemconfigure(
            self.id_text, text="Select source first..."
        )
