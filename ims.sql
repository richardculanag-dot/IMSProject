-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 05, 2025 at 10:22 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ims`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `AccountID` int(11) NOT NULL,
  `FName` varchar(100) NOT NULL,
  `LName` varchar(100) NOT NULL,
  `UserName` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`AccountID`, `FName`, `LName`, `UserName`, `Password`, `Role`) VALUES
(1, 'Jan Lorens', 'Comision', 'jancomision', '12345678', 'Staff'),
(2, 'Ezequel', 'Gilay', 'ezequelgilay', '12345678', 'Staff'),
(3, 'Jim', 'Joves', 'jimjoves', '12345678', 'Staff'),
(4, 'Gab', 'Gongon', 'gabgongon', '12345678', 'Staff'),
(5, 'Richard', 'Culanag', 'richardculanag', '12345678', 'Admin'),
(7, 'Jules', 'Ylanan', 'julsylanan', '12345678', 'Staff');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `CategoryID` int(11) NOT NULL,
  `CategoryName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`CategoryID`, `CategoryName`) VALUES
(1, 'Peripherals'),
(2, 'Internals'),
(3, 'Networking'),
(4, 'Accessories');

-- --------------------------------------------------------

--
-- Table structure for table `logs`
--

CREATE TABLE `logs` (
  `LogID` int(11) NOT NULL,
  `AccountID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `Action` varchar(500) NOT NULL,
  `Date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `ProductID` int(11) NOT NULL,
  `ProductName` varchar(100) NOT NULL,
  `TypeID` int(11) NOT NULL,
  `SupplierID` int(11) NOT NULL,
  `Price` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL,
  `Total` int(11) NOT NULL,
  `ReorderLevel` int(11) NOT NULL,
  `DateSupplied` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`ProductID`, `ProductName`, `TypeID`, `SupplierID`, `Price`, `Quantity`, `Total`, `ReorderLevel`, `DateSupplied`) VALUES
(1, 'Acer 24-inch Monitor', 1, 1, 7500, 15, 112500, 5, '2025-09-25 10:00:00'),
(2, 'Logitech K120 Keyboard', 2, 2, 800, 40, 32000, 10, '2025-09-26 09:30:00'),
(3, 'Razer DeathAdder Mouse', 3, 3, 2500, 25, 62500, 8, '2025-09-26 13:00:00'),
(4, 'Redragon Zeus Headset', 4, 1, 3200, 18, 57600, 5, '2025-09-27 11:45:00'),
(5, 'Canon Pixma Printer', 7, 5, 6200, 10, 62000, 3, '2025-09-28 08:15:00'),
(6, 'Intel Core i5 CPU', 9, 2, 9500, 12, 114000, 4, '2025-09-29 14:20:00'),
(7, 'Corsair 16GB RAM', 10, 3, 4800, 30, 144000, 10, '2025-09-29 09:00:00'),
(8, 'ASUS B550 Motherboard', 12, 5, 8800, 9, 79200, 3, '2025-09-30 15:30:00'),
(9, 'Seagate 1TB HDD', 13, 1, 2400, 20, 48000, 5, '2025-10-01 10:10:00'),
(10, 'TP-Link WiFi Router', 15, 4, 1800, 25, 45000, 7, '2025-10-02 16:50:00'),
(11, 'D-Link Network Switch', 16, 4, 2300, 14, 32200, 4, '2025-10-02 17:10:00'),
(12, 'Logitech Webcam C270', 8, 3, 2200, 22, 48400, 6, '2025-10-03 09:40:00'),
(13, 'HyperX Mouse Pad', 23, 5, 500, 50, 25000, 15, '2025-10-03 12:00:00'),
(14, 'Sandisk 1TB External Drive', 24, 1, 3200, 16, 51200, 5, '2025-10-04 13:15:00'),
(15, 'HDMI Cable 2m', 21, 2, 250, 60, 15000, 20, '2025-10-04 14:25:00'),
(16, 'Intel Core i3 CPU', 9, 6, 10000, 35, 350000, 5, '2025-10-06 01:56:18'),
(17, 'Intel Core i7 CPU', 9, 2, 11000, 35, 385000, 5, '2025-10-06 01:56:24');

-- --------------------------------------------------------

--
-- Table structure for table `stockin`
--

CREATE TABLE `stockin` (
  `StockInID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `AccountID` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stockin`
--

INSERT INTO `stockin` (`StockInID`, `ProductID`, `AccountID`, `Quantity`) VALUES
(7, 17, 4, 5),
(8, 16, 4, 5),
(9, 17, 3, 10),
(10, 16, 4, 10),
(11, 17, 4, 5),
(12, 16, 4, 5),
(13, 17, 4, 10);

-- --------------------------------------------------------

--
-- Table structure for table `stockout`
--

CREATE TABLE `stockout` (
  `StockOutID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  `AccountID` int(11) NOT NULL,
  `Quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stockout`
--

INSERT INTO `stockout` (`StockOutID`, `ProductID`, `AccountID`, `Quantity`) VALUES
(5, 16, 3, 5),
(6, 16, 4, 10),
(7, 16, 4, 5),
(8, 17, 4, 10);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `SupplierID` int(11) NOT NULL,
  `SupplierName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`SupplierID`, `SupplierName`) VALUES
(1, 'TechSource'),
(2, 'PC Hub'),
(3, 'Gadget World'),
(4, 'NetLink Solutions'),
(5, 'CompTech Distributors'),
(6, 'GetHub Distributors'),
(7, 'SheshTech'),
(8, 'Qualitech');

-- --------------------------------------------------------

--
-- Table structure for table `type`
--

CREATE TABLE `type` (
  `TypeID` int(11) NOT NULL,
  `TypeName` varchar(100) NOT NULL,
  `CategoryID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type`
--

INSERT INTO `type` (`TypeID`, `TypeName`, `CategoryID`) VALUES
(1, 'Monitor', 1),
(2, 'Keyboard', 1),
(3, 'Mouse', 1),
(4, 'Headset', 1),
(5, 'Speaker', 1),
(6, 'Microphone', 1),
(7, 'Printer', 1),
(8, 'Webcam', 1),
(9, 'CPU', 2),
(10, 'RAM', 2),
(11, 'GPU', 2),
(12, 'Motherboard', 2),
(13, 'Storage', 2),
(14, 'PSU', 2),
(15, 'Router', 3),
(16, 'Switch', 3),
(17, 'LAN Cables', 3),
(18, 'Network Adapter', 3),
(19, 'Access Point', 3),
(20, 'Modem', 3),
(21, 'HDMI Cable', 4),
(22, 'USB Hub', 4),
(23, 'Mouse Pad', 4),
(24, 'External Drive', 4),
(25, 'Adapters', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`AccountID`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`CategoryID`);

--
-- Indexes for table `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`LogID`),
  ADD KEY `AccountID` (`AccountID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `SupplierID` (`SupplierID`),
  ADD KEY `TypeID` (`TypeID`);

--
-- Indexes for table `stockin`
--
ALTER TABLE `stockin`
  ADD PRIMARY KEY (`StockInID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `AccountID` (`AccountID`);

--
-- Indexes for table `stockout`
--
ALTER TABLE `stockout`
  ADD PRIMARY KEY (`StockOutID`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`SupplierID`);

--
-- Indexes for table `type`
--
ALTER TABLE `type`
  ADD PRIMARY KEY (`TypeID`),
  ADD KEY `CategoryID` (`CategoryID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `AccountID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `CategoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `logs`
--
ALTER TABLE `logs`
  MODIFY `LogID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `stockin`
--
ALTER TABLE `stockin`
  MODIFY `StockInID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `stockout`
--
ALTER TABLE `stockout`
  MODIFY `StockOutID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `SupplierID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `type`
--
ALTER TABLE `type`
  MODIFY `TypeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `logs`
--
ALTER TABLE `logs`
  ADD CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `accounts` (`AccountID`),
  ADD CONSTRAINT `logs_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`SupplierID`) REFERENCES `suppliers` (`SupplierID`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`TypeID`) REFERENCES `type` (`TypeID`);

--
-- Constraints for table `stockin`
--
ALTER TABLE `stockin`
  ADD CONSTRAINT `stockin_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`),
  ADD CONSTRAINT `stockin_ibfk_2` FOREIGN KEY (`AccountID`) REFERENCES `accounts` (`AccountID`);

--
-- Constraints for table `type`
--
ALTER TABLE `type`
  ADD CONSTRAINT `type_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
