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
)
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def add_guests():
    AddGuests()


class AddGuests(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data = {
            "name": StringVar(),
            "address": StringVar(),
            "phone": StringVar(),
        }

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
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(137.0, 153.0, image=self.image_image_1)

        self.canvas.create_text(
            52.0,
            128.0,
            anchor="nw",
            text="Họ tên:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(137.5, 165.0, image=self.entry_image_1)
        self.entry_1 = Entry(
            self,
            textvariable=self.data.get("name"),
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
        )
        self.entry_1.place(x=52.0, y=153.0, width=179.0, height=22.0)


        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(258.0, 259.0, image=self.image_image_2)

        self.canvas.create_text(
            52.0,
            234.0,
            anchor="nw",
            text="Địa chỉ:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(257.5, 271.0, image=self.entry_image_2)
        self.entry_2 = Entry(
            self,
            textvariable=self.data.get("address"),
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
        )
        self.entry_2.place(x=52.0, y=259.0, width=179.0, height=22.0)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(378.0, 153.0, image=self.image_image_3)

        self.canvas.create_text(
            293.0,
            128.0,
            anchor="nw",
            text="Số điện thoại:",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(378.5, 165.0, image=self.entry_image_3)
        self.entry_3 = Entry(
            self,
            textvariable=self.data.get("phone"),
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
        )
        self.entry_3.place(x=293.0, y=153.0, width=179.0, height=22.0)

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

        self.canvas.create_text(
            143.0,
            59.0,
            anchor="nw",
            text="Thêm khách hàng",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
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
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("view"),
            relief="flat",
        )
        self.button_2.place(x=547.0, y=116.0, width=209.0, height=74.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit"),
            relief="flat",
        )
        self.button_3.place(x=547.0, y=210.0, width=209.0, height=74.0)

    # Save the data to the database
    def save(self):
        # check if any fields are empty
        for val in self.data.values():
            if val.get() == "":
                messagebox.showinfo("Lỗi", "Vui lòng điền thông tin cần thiết.")
                return

        # Save the guest
        result = db_controller.add_guest(
            *[self.data[label].get() for label in ("name", "address", "phone")]
        )

        if result:
            messagebox.showinfo(None, "Thêm thông tin thành công!")
            self.parent.navigate("view")
            self.parent.windows.get("view").handle_refresh()
            # clear all fields
            for label in self.data.keys():
                self.data[label].set(0)
        else:
            messagebox.showerror(
                "Lỗi", "Không thể thêm thông tin."
            )
