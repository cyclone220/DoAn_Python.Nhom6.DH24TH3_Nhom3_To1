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


CREATE VIEW view_guests AS
SELECT 
  MaKH,
  Hoten,
  Dchi,
  Sdt,
  DATE_FORMAT(NgayNhap, '%d/%m/%Y %H:%i:%s') AS NgayNhap
FROM guests;

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

