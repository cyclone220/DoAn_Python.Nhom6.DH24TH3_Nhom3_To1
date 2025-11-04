/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS hms;


use hms;

DROP TABLE IF EXISTS `guests`;
CREATE TABLE `guests` (
  `MaKH` int(11) NOT NULL AUTO_INCREMENT,
  `Hoten` varchar(30) DEFAULT NULL,
  `Dchi` varchar(50) DEFAULT NULL,
  `Sdt` varchar(20) DEFAULT NULL,
  `NgayNhap` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`MaKH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `guests` WRITE;
/*!40000 ALTER TABLE `guests` DISABLE KEYS */;
INSERT INTO `guests` VALUES (001,'Nguyễn Văn A',"Tp.HCM",'0968776113','2025-10-14 08:51:19'),
(002,'Trần Thị B',"Đà Nẵng",'0961176113','2025-10-17 05:19:02'),
(003,'Lê C',"An Giang",'0461276113','2025-10-17 06:58:23');
/*!40000 ALTER TABLE `guests` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `rooms`;
DROP TABLE IF EXISTS `loai_phong`;

-- ========================
-- BẢNG LOẠI PHÒNG
-- ========================
CREATE TABLE `loai_phong` (
  `ma_loai` ENUM('don', 'doi', 'vip') PRIMARY KEY,
  `gia` INT(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dữ liệu mẫu cho loại phòng
INSERT INTO `loai_phong` (`ma_loai`, `gia`) VALUES
('don', 250000),
('doi', 500000),
('vip', 800000);

-- ========================
-- BẢNG PHÒNG
-- ========================
CREATE TABLE `rooms` (
  `MaPhong` INT(11) NOT NULL AUTO_INCREMENT,
  `SoPhong` INT(11) UNIQUE,
  `LoaiPhong` ENUM('don', 'doi', 'vip'),
  `Gia` INT(12) DEFAULT NULL,
  `ConTrong` BOOLEAN DEFAULT FALSE,
  `NgayNhap` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`MaPhong`),
  FOREIGN KEY (`LoaiPhong`) REFERENCES `loai_phong`(`ma_loai`)
    ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ========================
-- TRIGGER: Tự động cập nhật giá theo loại phòng
-- ========================

DELIMITER //
CREATE TRIGGER before_insert_rooms
BEFORE INSERT ON rooms
FOR EACH ROW
BEGIN
  DECLARE gia_phong INT;
  SELECT gia INTO gia_phong FROM loai_phong WHERE ma_loai = NEW.LoaiPhong;
  SET NEW.Gia = gia_phong;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER before_update_rooms
BEFORE UPDATE ON rooms
FOR EACH ROW
BEGIN
  DECLARE gia_phong INT;
  IF NEW.LoaiPhong <> OLD.LoaiPhong THEN
    SELECT gia INTO gia_phong FROM loai_phong WHERE ma_loai = NEW.LoaiPhong;
    SET NEW.Gia = gia_phong;
  END IF;
END //
DELIMITER ;

-- ========================
-- MOCK DATA CHO BẢNG ROOMS
-- ========================
INSERT INTO rooms (SoPhong, LoaiPhong, ConTrong, NgayNhap) VALUES
(101, 'don', TRUE,  '2025-10-15 07:05:03'),
(102, 'vip', FALSE, '2025-10-16 10:38:49'),
(103, 'doi', TRUE,  '2025-10-17 05:15:29'),
(104, 'don', FALSE, '2025-10-17 05:15:38'),
(105, 'doi', TRUE,  '2025-10-17 05:16:09'),
(106, 'don', FALSE, '2025-10-17 05:16:33'),
(107, 'doi', TRUE,  '2025-10-17 05:17:29'),
(108, 'vip', TRUE,  '2025-10-17 06:57:46');

-- ========================
-- BẢNG DỊCH VỤ
-- ========================
DROP TABLE IF EXISTS `dichvu`;
CREATE TABLE `dichvu` (
  `MaDV` INT(11) NOT NULL AUTO_INCREMENT,
  `TenDV` VARCHAR(50) NOT NULL,
  `DonGia` INT(12) NOT NULL,
  PRIMARY KEY (`MaDV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dữ liệu mẫu
INSERT INTO dichvu (TenDV, DonGia) VALUES
('Giặt ủi', 30000),
('Ăn sáng', 50000),
('Thuê xe', 200000),
('Spa', 250000);

-- ========================
-- BẢNG ĐẶT PHÒNG (cập nhật)
-- ========================
DROP TABLE IF EXISTS `datphong`;
CREATE TABLE `datphong` (
`MaHoaDon` VARCHAR(10) NOT NULL,   -- Primary key
`MaPhong` INT(11) NOT NULL,
`MaKH` INT(11) NOT NULL,
`NgayCheckin` DATETIME NOT NULL,
`NgayCheckout` DATETIME DEFAULT NULL,
`TienPhong` INT(12) DEFAULT 0,
`TongTienDV` INT(12) DEFAULT 0,
`TongThanhToan` INT(12) DEFAULT 0,
PRIMARY KEY (`MaHoaDon`),
FOREIGN KEY (`MaPhong`) REFERENCES `rooms`(`MaPhong`)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (`MaKH`) REFERENCES `guests`(`MaKH`)
ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Trigger BEFORE INSERT: tự tạo MaHoaDon dạng HD0001, HD0002,...
DELIMITER //
CREATE TRIGGER trg_datphong_before_insert
BEFORE INSERT ON datphong
FOR EACH ROW
BEGIN
DECLARE next_id INT;
SELECT IFNULL(MAX(CAST(SUBSTRING(MaHoaDon,3) AS UNSIGNED)),0) + 1 INTO next_id FROM datphong;
SET NEW.MaHoaDon = CONCAT('HD', LPAD(next_id, 4, '0'));
END //
DELIMITER ;

-- ========================
-- BẢNG HÓA ĐƠN DỊCH VỤ
-- ========================
DROP TABLE IF EXISTS `hoadon`;
CREATE TABLE `hoadon` (
`ID` INT(11) NOT NULL AUTO_INCREMENT,
`MaHoaDon` VARCHAR(10) NOT NULL,
`MaDV` INT(11) NOT NULL,
`SoLuong` INT(11) NOT NULL DEFAULT 1,
`ThanhTien` INT(12) DEFAULT 0,
PRIMARY KEY (`ID`),
FOREIGN KEY (`MaHoaDon`) REFERENCES `datphong`(`MaHoaDon`)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (`MaDV`) REFERENCES `dichvu`(`MaDV`)
ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Trigger tự động tính Thành tiền trước insert hoặc update
DELIMITER //
CREATE TRIGGER trg_hoadon_before_insert
BEFORE INSERT ON hoadon
FOR EACH ROW
BEGIN
DECLARE gia INT;
SELECT DonGia INTO gia FROM dichvu WHERE MaDV = NEW.MaDV;
SET NEW.ThanhTien = gia * NEW.SoLuong;
END //

CREATE TRIGGER trg_hoadon_before_update
BEFORE UPDATE ON hoadon
FOR EACH ROW
BEGIN
DECLARE gia INT;
SELECT DonGia INTO gia FROM dichvu WHERE MaDV = NEW.MaDV;
SET NEW.ThanhTien = gia * NEW.SoLuong;
END //
DELIMITER ;

-- Stored Procedure: tự động cập nhật tổng tiền
DROP PROCEDURE IF EXISTS sp_cap_nhat_tong_tien;
DELIMITER //
CREATE PROCEDURE sp_cap_nhat_tong_tien(IN p_MaHoaDon VARCHAR(10))
BEGIN
    DECLARE so_ngay INT DEFAULT 0;
    DECLARE gia_phong INT DEFAULT 0;
    DECLARE tien_phong INT DEFAULT 0;
    DECLARE tong_dv INT DEFAULT 0;
    DECLARE tong INT DEFAULT 0;

    -- Tính số ngày ở và giá phòng
    SELECT 
        DATEDIFF(IFNULL(NgayCheckout, NOW()), NgayCheckin),
        r.Gia
    INTO so_ngay, gia_phong
    FROM datphong dp
    JOIN rooms r ON dp.MaPhong = r.MaPhong
    WHERE dp.MaHoaDon = p_MaHoaDon;

    IF so_ngay <= 0 THEN
        SET so_ngay = 1;
    END IF;

    SET tien_phong = so_ngay * gia_phong;

    SELECT IFNULL(SUM(ThanhTien),0)
    INTO tong_dv
    FROM hoadon
    WHERE MaHoaDon = p_MaHoaDon;

    SET tong = tien_phong + tong_dv;

    UPDATE datphong
    SET 
        TienPhong = tien_phong,
        TongTienDV = tong_dv,
        TongThanhToan = tong
    WHERE MaHoaDon = p_MaHoaDon;
END //
DELIMITER ;

-- Trigger AFTER INSERT/UPDATE/DELETE trên hoadon gọi stored procedure
DELIMITER //
CREATE TRIGGER trg_hoadon_after_insert
AFTER INSERT ON hoadon
FOR EACH ROW
BEGIN
CALL sp_cap_nhat_tong_tien(NEW.MaHoaDon);
END //

CREATE TRIGGER trg_hoadon_after_update
AFTER UPDATE ON hoadon
FOR EACH ROW
BEGIN
CALL sp_cap_nhat_tong_tien(NEW.MaHoaDon);
END //

CREATE TRIGGER trg_hoadon_after_delete
AFTER DELETE ON hoadon
FOR EACH ROW
BEGIN
CALL sp_cap_nhat_tong_tien(OLD.MaHoaDon);
END //
DELIMITER ;


INSERT INTO datphong (MaPhong, MaKH, NgayCheckin, NgayCheckout)
VALUES
(1, 1, '2025-10-20 14:00:00', '2025-10-22 12:00:00'),
(3, 2, '2025-10-25 15:00:00', '2025-10-28 11:00:00');

INSERT INTO hoadon (MaHoaDon, MaDV, SoLuong)
VALUES
('HD0001', 1, 2),
('HD0001', 2, 2),
('HD0001', 3, 1),
('HD0002', 4, 1);
--
-- 

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

