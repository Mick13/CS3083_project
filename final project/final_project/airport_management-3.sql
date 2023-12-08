-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 03, 2023 at 07:11 AM
-- Server version: 5.7.39
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airport management`
--

-- --------------------------------------------------------

--
-- Table structure for table `Airline`
--

CREATE TABLE `Airline` (
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airline`
--

INSERT INTO `Airline` (`name`) VALUES
('Jet Blue'),
('United');

-- --------------------------------------------------------

--
-- Table structure for table `Airline_Staff`
--

CREATE TABLE `Airline_Staff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airline_Staff`
--

INSERT INTO `Airline_Staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('a', '0cc175b9c0f1b6a831c399e269772661', 'Albert', 'Z', '1999-06-05', 'Jet Blue'),
('ab', '187ef4436122d1cc2f40dc2b92f0eba0', 'Jon', 'Ryan', '2011-07-09', 'United');

-- --------------------------------------------------------

--
-- Table structure for table `Airline_Staff_Email`
--

CREATE TABLE `Airline_Staff_Email` (
  `username` varchar(50) NOT NULL,
  `email_address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airline_Staff_Email`
--

INSERT INTO `Airline_Staff_Email` (`username`, `email_address`) VALUES
('a', 'aa@jetblue.com'),
('a', 'Albert@gmail.com'),
('a', 'Albert@jetblue.com'),
('ab', 'Jon.Ryan@united.com');

-- --------------------------------------------------------

--
-- Table structure for table `Airline_Staff_Phone`
--

CREATE TABLE `Airline_Staff_Phone` (
  `username` varchar(50) NOT NULL,
  `phone_number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airline_Staff_Phone`
--

INSERT INTO `Airline_Staff_Phone` (`username`, `phone_number`) VALUES
('a', '9171111111'),
('ab', '9171234567');

-- --------------------------------------------------------

--
-- Table structure for table `Airplane`
--

CREATE TABLE `Airplane` (
  `identification_number` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `number_of_seats` int(11) DEFAULT NULL,
  `manufacturing_company` varchar(255) DEFAULT NULL,
  `model_number` varchar(255) DEFAULT NULL,
  `manufacturing_date` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airplane`
--

INSERT INTO `Airplane` (`identification_number`, `airline_name`, `number_of_seats`, `manufacturing_company`, `model_number`, `manufacturing_date`, `age`) VALUES
('11', 'Jet Blue', 300, 'Boeing', 'G111', '1999-03-25', 24),
('12', 'Jet Blue', 45, 'Airbus', 'F11', '2023-09-19', 0),
('1801', 'Jet Blue', 15, 'Airbus', 'g1', '2021-11-23', 2),
('A001', 'Jet Blue', 200, 'Airbus', 'G20', '2023-11-26', 1),
('AB101', 'Jet Blue', 600, 'Boeing', 'G111', '2023-01-18', 0),
('B011f', 'Jet Blue', 200, 'Airbus', 'Fe21', '2023-10-18', 0),
('JB001', 'Jet Blue', 200, 'Airbus', 'A320', '2010-04-01', 13),
('JB002', 'Jet Blue', 250, 'Airbus', 'A321', '2012-05-02', 11),
('JB003', 'Jet Blue', 300, 'Boeing', 'A323', '2015-07-02', 8),
('P000', 'Jet Blue', 22, 'Boeing', 'F2', '2023-11-13', 2),
('plane000', 'Jet Blue', 2, 'Airbus', 'F111', '2023-11-13', 1),
('United101', 'Jet Blue', 50, 'Boeing', 'A200', '2022-10-18', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Airport`
--

CREATE TABLE `Airport` (
  `code` varchar(3) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `number_of_terminals` int(11) DEFAULT NULL,
  `airport_type` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airport`
--

INSERT INTO `Airport` (`code`, `name`, `city`, `country`, `number_of_terminals`, `airport_type`) VALUES
('JFK', 'John F Kennedy International Airport', 'New York City', 'USA', 5, 'international'),
('LAX', 'Los Angeles International Airport', 'Los Angeles ', 'USA', 10, 'international'),
('MIA', 'Miami International Airport', 'Miami', 'USA', 12, 'international'),
('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'China', 2, 'international');

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--

CREATE TABLE `Customer` (
  `email_address` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `building_number` int(11) DEFAULT NULL,
  `street_name` varchar(100) DEFAULT NULL,
  `apartment_number` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip_code` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Customer`
--

INSERT INTO `Customer` (`email_address`, `password`, `first_name`, `last_name`, `building_number`, `street_name`, `apartment_number`, `city`, `state`, `zip_code`, `date_of_birth`) VALUES
('albert14@gmail.com', '0cc175b9c0f1b6a831c399e269772661', 'Albert', 'Shamah', 123, '9', NULL, 'Brooklyn', 'NY', '11239', '2000-03-04'),
('clara.elazzi@example.com', 'ClaraPassword!', 'Clara', 'El Azzi', 456, 'Maple Street', 12, 'Los Angeles', 'CA', '90001', '1992-07-25'),
('jon.mark@gmail.com', '0cc175b9c0f1b6a831c399e269772661', 'Jon', 'Mark', 10, '9th', 11, 'Queens', 'NY', '11230', '2015-10-11'),
('m@gmail.com', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'Mickey', 'Shamah', 2, '9th', NULL, 'Brooklyn', 'NY', '11230', '2023-05-30'),
('mickshamah13@gmail.com', 'Mickey13', 'Mickey', 'Shamah', 1, '9th Street', 10, 'Brooklyn', 'NY', '11230', '2003-05-13'),
('ms13209@nyu.edu', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 'Mike', 'S', 1, '5nd', 2, 'B', 'N', '1120', '2023-08-03'),
('one@gmail.com', '0cc175b9c0f1b6a831c399e269772661', 'A', 'A', 1, '54', 4, 'NYC', 'NY', '12039', '2022-11-09'),
('one@one.com', '0cc175b9c0f1b6a831c399e269772661', 'One', 'One', 1, '1', 1, 'qw', 'SG', '13826', '2001-12-03'),
('ryan_doe@gmail.com', 'RyanPass123', 'Ryan', 'Doe', 789, 'Elm Street', 5, 'New York', 'NY', '10001', '1985-12-15'),
('t@idc.com', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'Mickey', 'Shamah', 866, '9th', NULL, 'Brookyn', 'NY', '182813', '2023-09-20'),
('trial7@gmail.com', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'Ryan', 'Cho', 1, '8473sr', 8, 'LA', 'CA', '12039', '1976-03-12'),
('trial@gmail.com', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'trial', 'five', NULL, '1st', 55, 'OQH', 'CA', '2938', '1999-04-03'),
('tt@gmail.com', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'Mickey', 'Shamah', 866, '9th street', NULL, 'Brooklyn', 'NY', '1998', '2023-08-10');

-- --------------------------------------------------------

--
-- Table structure for table `Customer_Passport`
--

CREATE TABLE `Customer_Passport` (
  `email_address` varchar(100) NOT NULL,
  `passport_number` varchar(9) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Customer_Passport`
--

INSERT INTO `Customer_Passport` (`email_address`, `passport_number`, `passport_expiration`, `passport_country`) VALUES
('one@one.com', '283726', '2025-07-24', 'USA');

-- --------------------------------------------------------

--
-- Table structure for table `Customer_Phone`
--

CREATE TABLE `Customer_Phone` (
  `email_address` varchar(100) NOT NULL,
  `phone_number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Customer_Phone`
--

INSERT INTO `Customer_Phone` (`email_address`, `phone_number`) VALUES
('jon.mark@gmail.com', ''),
('one@one.com', '283726'),
('one@one.com', '9876543');

-- --------------------------------------------------------

--
-- Table structure for table `Flight`
--

CREATE TABLE `Flight` (
  `flight_number` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `departure_airport` varchar(3) NOT NULL,
  `departure_date_time` datetime NOT NULL,
  `arrival_airport` varchar(3) DEFAULT NULL,
  `arrival_date_time` datetime DEFAULT NULL,
  `base_price_of_ticket` decimal(10,2) DEFAULT NULL,
  `airplane_id` varchar(255) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Flight`
--

INSERT INTO `Flight` (`flight_number`, `airline_name`, `departure_airport`, `departure_date_time`, `arrival_airport`, `arrival_date_time`, `base_price_of_ticket`, `airplane_id`, `status`) VALUES
('JB001', 'Jet Blue', 'JFK', '2023-12-01 08:00:00', 'PVG', '2023-12-02 20:00:00', '800.00', 'JB001', 'on time'),
('JB0011', 'Jet Blue', 'JFK', '2023-11-28 23:19:00', 'LAX', '2023-11-29 23:19:00', '200.00', 'JB002', 'on time'),
('JB002', 'Jet Blue', 'JFK', '2023-12-02 09:00:00', 'PVG', '2023-12-03 21:00:00', '850.00', 'JB002', 'delayed'),
('JB003', 'Jet Blue', 'JFK', '2023-12-03 09:00:00', 'PVG', '2023-12-04 21:00:00', '850.00', 'JB003', 'delayed'),
('JB004', 'Jet Blue', 'JFK', '2023-12-18 21:56:00', 'PVG', '2023-11-13 21:57:00', '200.00', 'JB001', 'on time'),
('JB004', 'Jet Blue', 'PVG', '2024-01-01 21:44:00', 'JFK', '2024-01-03 21:44:00', '200.00', 'JB003', 'on time'),
('JB005', 'Jet Blue', 'PVG', '2023-11-30 22:02:00', 'JFK', '2023-12-01 22:02:00', '600.00', 'JB001', 'delayed'),
('JB006', 'Jet Blue', 'PVG', '2023-11-29 22:05:00', 'JFK', '2023-11-30 22:05:00', '400.00', 'JB002', 'on time'),
('JB007', 'Jet Blue', 'PVG', '2023-11-29 22:19:00', 'JFK', '2023-11-30 22:19:00', '700.00', 'JB001', 'delayed'),
('Jb0101', 'Jet Blue', 'JFK', '2024-01-01 08:00:00', 'LAX', '2024-01-01 11:00:00', '300.00', 'JB001', 'on time'),
('JB016', 'Jet Blue', 'PVG', '2023-11-12 00:21:00', 'JFK', '2023-11-13 00:21:00', '1.00', 'JB001', 'canceled');

-- --------------------------------------------------------

--
-- Table structure for table `Flight_Rating`
--

CREATE TABLE `Flight_Rating` (
  `flight_number` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `departure_date_time` datetime NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `rating` int(10) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Flight_Rating`
--

INSERT INTO `Flight_Rating` (`flight_number`, `airline_name`, `departure_date_time`, `customer_email`, `rating`, `comment`) VALUES
('JB001', 'Jet Blue', '2023-12-01 08:00:00', 'clara.elazzi@example.com', 1, 'terrible flight'),
('JB001', 'Jet Blue', '2023-12-01 08:00:00', 'mickshamah13@gmail.com', 6, 'ok flight'),
('JB002', 'Jet Blue', '2023-12-02 09:00:00', 'ryan_doe@gmail.com', 9, 'great flight');

-- --------------------------------------------------------

--
-- Table structure for table `Maintenance_procedure`
--

CREATE TABLE `Maintenance_procedure` (
  `airline_name` varchar(255) NOT NULL,
  `airplane_id` varchar(255) NOT NULL,
  `start_date_time` datetime NOT NULL,
  `end_date_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Maintenance_procedure`
--

INSERT INTO `Maintenance_procedure` (`airline_name`, `airplane_id`, `start_date_time`, `end_date_time`) VALUES
('Jet Blue', 'JB001', '2023-12-20 23:31:00', '2023-12-25 23:31:00'),
('Jet Blue', 'JB001', '2024-02-07 18:54:00', '2024-02-09 18:54:00');

-- --------------------------------------------------------

--
-- Table structure for table `Ticket`
--

CREATE TABLE `Ticket` (
  `ticket_ID` int(11) NOT NULL,
  `flight_number` varchar(255) DEFAULT NULL,
  `departure_date_time` datetime DEFAULT NULL,
  `airline_name` varchar(255) DEFAULT NULL,
  `purchase_date_time` datetime DEFAULT NULL,
  `base_ticket_price` decimal(10,2) DEFAULT NULL,
  `calculated_ticket_price` decimal(10,2) DEFAULT NULL,
  `customer_email` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `card_type` varchar(15) DEFAULT NULL,
  `card_number` varchar(19) DEFAULT NULL,
  `name_on_card` varchar(100) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Ticket`
--

INSERT INTO `Ticket` (`ticket_ID`, `flight_number`, `departure_date_time`, `airline_name`, `purchase_date_time`, `base_ticket_price`, `calculated_ticket_price`, `customer_email`, `first_name`, `last_name`, `date_of_birth`, `card_type`, `card_number`, `name_on_card`, `expiration_date`) VALUES
(1, 'JB001', '2023-12-01 08:00:00', 'Jet Blue', '2023-11-01 10:00:00', '800.00', '800.00', 'mickshamah13@gmail.com', 'Mickey', 'Shamah', '2003-05-13', 'credit', '1234567812345678', 'Mickey Shamah', '2028-05-31'),
(2, 'JB001', '2023-12-01 08:00:00', 'Jet Blue', '2023-11-02 11:00:00', '800.00', '1000.00', 'ryan_doe@gmail.com', 'Ryan', 'Doe', '1985-12-15', 'debit', '8765432187654321', 'Ryan Doe', '2030-12-31'),
(3, 'JB002', '2023-12-02 09:00:00', 'Jet Blue', '2023-11-03 12:00:00', '850.00', '850.00', 'clara.elazzi@example.com', 'Clara', 'El Azzi', '1992-07-25', 'credit', '5555666677778888', 'Clara El Azzi', '2032-07-31'),
(5, 'Jb0101', '2024-01-01 08:00:00', 'Jet Blue', '2023-12-03 00:49:03', '300.00', '300.00', 'one@one.com', 'John', 'Doe', '1980-01-01', 'credit', '1234567890123456', 'John Doe', '2025-01-01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Airline`
--
ALTER TABLE `Airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `Airline_Staff`
--
ALTER TABLE `Airline_Staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `Airline_Staff_Email`
--
ALTER TABLE `Airline_Staff_Email`
  ADD PRIMARY KEY (`username`,`email_address`);

--
-- Indexes for table `Airline_Staff_Phone`
--
ALTER TABLE `Airline_Staff_Phone`
  ADD PRIMARY KEY (`username`,`phone_number`);

--
-- Indexes for table `Airplane`
--
ALTER TABLE `Airplane`
  ADD PRIMARY KEY (`identification_number`,`airline_name`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `Airport`
--
ALTER TABLE `Airport`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`email_address`);

--
-- Indexes for table `Customer_Passport`
--
ALTER TABLE `Customer_Passport`
  ADD PRIMARY KEY (`email_address`,`passport_number`);

--
-- Indexes for table `Customer_Phone`
--
ALTER TABLE `Customer_Phone`
  ADD PRIMARY KEY (`email_address`,`phone_number`);

--
-- Indexes for table `Flight`
--
ALTER TABLE `Flight`
  ADD PRIMARY KEY (`flight_number`,`airline_name`,`departure_date_time`),
  ADD KEY `airline_name` (`airline_name`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`),
  ADD KEY `airplane_id` (`airplane_id`,`airline_name`);

--
-- Indexes for table `Flight_Rating`
--
ALTER TABLE `Flight_Rating`
  ADD PRIMARY KEY (`flight_number`,`airline_name`,`departure_date_time`,`customer_email`),
  ADD KEY `customer_email` (`customer_email`);

--
-- Indexes for table `Maintenance_procedure`
--
ALTER TABLE `Maintenance_procedure`
  ADD PRIMARY KEY (`airline_name`,`airplane_id`,`start_date_time`);

--
-- Indexes for table `Ticket`
--
ALTER TABLE `Ticket`
  ADD PRIMARY KEY (`ticket_ID`),
  ADD KEY `flight_number` (`flight_number`,`airline_name`,`departure_date_time`),
  ADD KEY `customer_email` (`customer_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Ticket`
--
ALTER TABLE `Ticket`
  MODIFY `ticket_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Airline_Staff`
--
ALTER TABLE `Airline_Staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`name`);

--
-- Constraints for table `Airline_Staff_Email`
--
ALTER TABLE `Airline_Staff_Email`
  ADD CONSTRAINT `airline_staff_email_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Airline_Staff` (`username`);

--
-- Constraints for table `Airline_Staff_Phone`
--
ALTER TABLE `Airline_Staff_Phone`
  ADD CONSTRAINT `airline_staff_phone_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Airline_Staff` (`username`);

--
-- Constraints for table `Airplane`
--
ALTER TABLE `Airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`name`) ON DELETE CASCADE;

--
-- Constraints for table `Customer_Passport`
--
ALTER TABLE `Customer_Passport`
  ADD CONSTRAINT `customer_passport_ibfk_1` FOREIGN KEY (`email_address`) REFERENCES `Customer` (`email_address`) ON DELETE CASCADE;

--
-- Constraints for table `Customer_Phone`
--
ALTER TABLE `Customer_Phone`
  ADD CONSTRAINT `customer_phone_ibfk_1` FOREIGN KEY (`email_address`) REFERENCES `Customer` (`email_address`) ON DELETE CASCADE;

--
-- Constraints for table `Flight`
--
ALTER TABLE `Flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`name`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`departure_airport`) REFERENCES `Airport` (`code`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arrival_airport`) REFERENCES `Airport` (`code`),
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`airplane_id`,`airline_name`) REFERENCES `Airplane` (`identification_number`, `airline_name`);

--
-- Constraints for table `Flight_Rating`
--
ALTER TABLE `Flight_Rating`
  ADD CONSTRAINT `flight_rating_ibfk_1` FOREIGN KEY (`flight_number`,`airline_name`,`departure_date_time`) REFERENCES `Flight` (`flight_number`, `airline_name`, `departure_date_time`),
  ADD CONSTRAINT `flight_rating_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `Customer` (`email_address`);

--
-- Constraints for table `Maintenance_procedure`
--
ALTER TABLE `Maintenance_procedure`
  ADD CONSTRAINT `maintenance_procedure_ibfk_1` FOREIGN KEY (`airline_name`,`airplane_id`) REFERENCES `Airplane` (`airline_name`, `identification_number`) ON DELETE CASCADE;

--
-- Constraints for table `Ticket`
--
ALTER TABLE `Ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`flight_number`,`airline_name`,`departure_date_time`) REFERENCES `Flight` (`flight_number`, `airline_name`, `departure_date_time`) ON DELETE CASCADE,
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `Customer` (`email_address`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
