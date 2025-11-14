import mysql.connector
import os
import matplotlib.pyplot as pt

# Configurations
from config import config
from dotenv import load_dotenv

load_dotenv()  # Imports environemnt variables from the '.env' file

# ===================SQL Connectivity=================

# SQL Connection
connection = mysql.connector.connect(
    host=config.get("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=config.get("DB_NAME"),
    port="3306",
    autocommit=config.get("DB_AUTOCOMMIT"),
)

cursor = connection.cursor(buffered=True)

# SQL functions


def checkUser(username, password=None):
    cmd = f"Select count(username) from login where username='{username}' and BINARY password='{password}'"
    cursor.execute(cmd)
    cmd = None
    a = cursor.fetchone()[0] >= 1
    return a


def human_format(num):
    if num < 1000:
        return num

    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    return "%.1f%s" % (num, ["", "K", "M", "G", "T", "P"][magnitude])


def find_g_id(name):
    cmd = f"select g_id from guests where name = '{name}'"
    cursor.execute(cmd)
    out = cursor.fetchone()[0]
    return out


def checkin(g_id):
    cmd = f"select * from reservations where g_id = '{g_id}';"
    cursor.execute(cmd)
    reservation = cursor.fetchall()
    if reservation != []:
        subcmd = f"update reservations set check_in = curdate() where g_id = '{g_id}' "
        cursor.execute(subcmd)
        return "successful"
    else:
        return "No reservations for the given Guest"



def checkout(MaHoaDon):
    cmd = f"update datphong set NgayCheckout=current_timestamp where MaHoaDon='{MaHoaDon}' limit 1;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# ============Python Functions==========


def acceptable(*args, acceptables):
    """
    If the characters in StringVars passed as arguments are in acceptables return True, else returns False
    """
    for arg in args:
        for char in arg:
            if char.lower() not in acceptables:
                return False
    return True



# Get all guests
def get_guests():
    cmd = "select MaKH, HoTen, Dchi, sdt, NgayNhap from guests;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()


# Add a guest
def add_guest(name, address, phone):
    cmd = f"insert into guests(HoTen,Dchi,Sdt) values('{name}','{address}',{phone});"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# add a room
def add_room(SoPhong, LoaiPhong, ConTrong):
    cmd = f"insert into rooms(SoPhong,LoaiPhong,ConTrong) values('{SoPhong}','{LoaiPhong}','{ConTrong}');"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# Get All rooms
def get_rooms():
    cmd = "select MaPhong, SoPhong, LoaiPhong, Gia, ConTrong, NgayNhap from rooms;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()

# Get unoccupated rooms
def get_unoccupated_rooms_by_type(Loai):
    cmd = f"select MaPhong, SoPhong, LoaiPhong, Gia, ConTrong, NgayNhap from rooms where ConTrong = 1 and LoaiPhong = '{Loai}';"
    cursor.execute(cmd)
    rows = cursor.fetchall()
    return rows if rows else []

# Get all reservations
def get_reservations():
    cmd = "select MaHoaDon,MaPhong,MaKH,NgayCheckin,NgayCheckout from datphong;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()


# Add a reservation
def add_reservation(MaPhong,MaKH,CheckIn):
    cmd = f"insert into datphong(MaPhong,MaKH,NgayCheckin) values('{MaPhong}',{MaKH},'{CheckIn}');"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    cursor.execute("SELECT MaHoaDon FROM datphong ORDER BY MaHoaDon DESC LIMIT 1;")
    mahoadon = cursor.fetchone()[0]

    # Gọi procedure cập nhật tổng tiền
    cursor.callproc("sp_cap_nhat_tong_tien", [mahoadon])
    connection.commit()
    return True

# Get all room count
def get_total_rooms():
    cmd = "select count(MaPhong) from rooms;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchone()[0]

def get_Vip_booked():
    cmd = f"select count(MaPhong) from rooms where ConTrong = 0 and LoaiPhong = 'vip'"
    cursor.execute(cmd)

    return cursor.fetchone()[0]

def get_doi_booked():
    cmd = f"select count(MaPhong) from rooms where ConTrong = 0 and LoaiPhong = 'doi'"
    cursor.execute(cmd)

    return cursor.fetchone()[0]

def get_don_booked():
    cmd = f"select count(MaPhong) from rooms where ConTrong = 0 and LoaiPhong = 'don'"
    cursor.execute(cmd)

    return cursor.fetchone()[0]

def get_reservation_by_id(ma_hoadon):
    cmd = f"""
    SELECT MaHoaDon, MaPhong, MaKH, NgayCheckin, NgayCheckout, TienPhong, TongTienDV, TongThanhToan
    FROM datphong
    WHERE MaHoaDon = '{ma_hoadon}'
    """
    cursor.execute(cmd)
    return cursor.fetchone()  

def get_services_by_invoice(ma_hoadon):
    cmd = f"""
    SELECT dv.TenDV, hd.SoLuong, hd.ThanhTien
    FROM hoadon hd
    JOIN dichvu dv ON hd.MaDV = dv.MaDV
    WHERE hd.MaHoaDon = '{ma_hoadon}'
    """
    cursor.execute(cmd)
    return cursor.fetchall()  

# Check if a room is vacant
def booked():
    cmd = f"select count(MaPhong) from rooms where ConTrong = 0"
    cursor.execute(cmd)

    return cursor.fetchone()[0]


def vacant():
    return get_total_rooms() - booked()


def bookings():
    cmd = f"select count(rs.id) from reservations rs , rooms ros where rs.r_id = ros.id and ros.room_type = 'D';"
    cursor.execute(cmd)
    deluxe = cursor.fetchone()[0]

    cmd1 = f"select count(rs.id) from reservations rs , rooms ros where rs.r_id = ros.id and ros.room_type = 'N';"
    cursor.execute(cmd1)
    Normal = cursor.fetchone()[0]

    return [deluxe, Normal]

def get_HoaDon():
    cmd = "select MaHoaDon from datphong;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()

def get_DichVu():
    cursor.execute("SELECT MaDV, TenDV FROM dichvu;")
    services = cursor.fetchall()
    return services

def add_DichVu(ma_hoadon, ma_dv, so_luong):
    cmd = f"INSERT INTO hoadon (MaHoaDon, MaDV, SoLuong) VALUES ('{ma_hoadon}','{ma_dv}','{so_luong}')"
    cursor.execute(cmd)
    connection.commit()
    if cursor.rowcount == 0:
        return False
    return True
# Get total hotel value
def get_total_hotel_value():
    cmd = "select sum(price) from rooms;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    value = cursor.fetchone()[0]

    return human_format(value)


def delete_reservation(MaHoaDon):
    cmd = f"delete from datphong where MaHoaDon='{MaHoaDon}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def delete_room(id):
    cmd = f"delete from rooms where MaPhong='{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def delete_guest(id):
    cmd = f"delete from guests where MaKH='{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def update_rooms(id, room_no, room_type,occupation):
    cmd = f"update rooms set LoaiPhong = '{room_type}', SoPhong = {room_no}, ConTrong={occupation} where MaPhong = {id};"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def update_guests(name, address, id, phone):

    cmd = f"update guests set Dchi = '{address}',Sdt = '{phone}' , HoTen = '{name}' where MaKh = {id};"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def update_reservations(
    g_id, check_in, room_id, reservation_date, check_out, meal, type, id
):
    cmd = f"update reservations set check_in = '{check_in}',check_out = '{check_out}',g_id = {g_id}, \
        r_date = '{reservation_date}',meal = {meal},r_type='{type}', r_id = {room_id} where id= {id};"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True



def update_reservation(id, room_id, g_id, check_in):
    cmd = f"update datphong set NgayCheckin= '{check_in}', MaKH = {g_id}, MaPhong = '{room_id}' where MaHoaDon= '{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True
