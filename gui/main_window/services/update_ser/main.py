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


def update_ser():
    UpdateSer()


class UpdateSer(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_r_id = self.parent.selected_rid

        self.configure(bg="#FFFFFF")

        self.data = {
            "id": StringVar(),
            "meal": StringVar(),
            "type": StringVar(),
            "g_id": StringVar(),
            "check_in": StringVar(),
            "room_id": StringVar(),
            "reservation_date": StringVar(),
            "check_out": StringVar(),
        }

        self.initialize()

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

    def initialize(self):
        self.selected_r_id = self.parent.selected_rid
        self.reservation_data = self.parent.reservation_data

        # Filter out all reservations for selected id reservation
        self.selected_reservation_data = list(
            filter(lambda x: str(x[0]) == self.selected_r_id, self.reservation_data)
        )

        if self.selected_reservation_data:
            self.selected_reservation_data = self.selected_reservation_data[0]

            self.canvas.itemconfigure(
                self.id_text, text=self.selected_reservation_data[0]
            )
            self.data["g_id"].set(self.selected_reservation_data[1])
            self.data["room_id"].set(self.selected_reservation_data[2])
            self.data["check_in"].set(self.selected_reservation_data[3])
            self.data["check_out"].set(self.selected_reservation_data[4])
            self.data["meal"].set(self.selected_reservation_data[5])
            self.data["reservation_date"].set(self.selected_reservation_data[3])

    def handle_update(self):

        data = [
            x
            for x in [
                self.data[label].get()
                for label in ("g_id", "check_in", "room_id", "check_out", "meal")
            ]
        ]

        # Update data and show alert
        if db_controller.update_reservation(self.selected_r_id, *data):
            messagebox.showinfo("Success", "Reservation Updated Successfully")
            self.parent.navigate("view")

            self.reset()

        else:
            messagebox.showerror(
                "Error", "Error Updating Reservation. Please check all ids exist"
            )

        self.parent.refresh_entries()
    def reset(self):
        # clear all entries
        for label in self.data:
            self.data[label].set("")

        self.canvas.itemconfigure(
            self.id_text, text="Select source first..."
        )
