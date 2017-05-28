-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 03, 2017 at 02:02 AM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `_databases_427`
--

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Jet Blue');

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('AirlineStaff', 'e19d5cd5af0378da05f63f891c7467af', 'Joe', 'Bland', '1980-02-05', 'Jet Blue');

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('Jet Blue', 1, 100),
('Jet Blue', 2, 50),
('Jet Blue', 3, 75);

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('JFK', 'New York City'),
('La Guardia', 'New York City'),
('Louisville SDF', 'Louisville'),
('O\'Hare', 'Chicago'),
('SFO', 'San Francisco');

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('Booking@agent.com', 'e19d5cd5af0378da05f63f891c7467af', 1),
('Professional@booking.com', 'e19d5cd5af0378da05f63f891c7467af', 2);

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('Customer@nyu.edu', 'Customer', 'e19d5cd5af0378da05f63f891c7467af', '2', 'Metrotech', 'New York', 'New York', 2125551234, 'P123456', '2020-10-24', 'USA', '1990-04-01'),
('one@nyu.edu', 'One', '098f6bcd4621d373cade4e832627b4f6', '6', 'Metrotech', 'New York', 'New York', 2125559873, 'P53412', '2021-04-05', 'USA', '1990-04-04'),
('two@nyu.edu', 'Two', '098f6bcd4621d373cade4e832627b4f6', '5', 'Metrotech', 'New York', 'New York', 2125558123, 'P436246', '2027-04-20', 'USA', '1992-04-18');

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('Jet Blue', 177, 'SFO', '2017-05-20 23:50:00', 'JFK', '2017-05-21 08:50:00', '200', 'On Time', 1),
('Jet Blue', 253, 'O\'Hare', '2017-06-01 12:00:00', 'SFO', '2017-06-01 14:00:00', '420', 'On Time', 1),
('Jet Blue', 394, 'La Guardia', '2017-05-19 22:00:00', 'SFO', '2017-05-20 02:00:00', '600', 'On Time', 1),
('Jet Blue', 488, 'JFK', '2017-05-25 05:00:00', 'Louisville SDF', '2017-05-25 07:00:00', '97', 'On Time', 3),
('Jet Blue', 915, 'O\'Hare', '2017-03-01 00:00:00', 'SFO', '2017-03-01 04:00:00', '500', 'Delayed', 2);

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(1, 'Jet Blue', 177),
(2, 'Jet Blue', 394),
(3, 'Jet Blue', 915),
(4, 'Jet Blue', 915);

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(1, 'Customer@nyu.edu', NULL, '2017-05-01'),
(2, 'Customer@nyu.edu', 1, '2017-05-01'),
(3, 'one@nyu.edu', 2, '2017-02-01'),
(4, 'two@nyu.edu', 2, '2017-02-01');


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
