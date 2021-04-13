-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 13, 2021 at 05:30 PM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gp_practice`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointees`
--

DROP TABLE IF EXISTS `appointees`;
CREATE TABLE IF NOT EXISTS `appointees` (
  `APPID` int(11) NOT NULL AUTO_INCREMENT,
  `APPname` text NOT NULL,
  `APPtype` tinyint(4) NOT NULL,
  `APPdob` date NOT NULL,
  `APPpostcode` text NOT NULL,
  PRIMARY KEY (`APPID`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointees`
--

INSERT INTO `appointees` (`APPID`, `APPname`, `APPtype`, `APPdob`, `APPpostcode`) VALUES
(1, 'Lily Smith', 0, '1991-01-05', 'S3UG9'),
(2, 'Priya Patel', 1, '1998-05-14', 'NW127TQ'),
(3, 'Richard OBrien', 0, '1963-11-04', 'SW75AA'),
(4, 'Rita Wentworth', 1, '1987-09-26', 'E8W35');

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
CREATE TABLE IF NOT EXISTS `appointments` (
  `APMID` int(11) NOT NULL AUTO_INCREMENT,
  `APMdate` timestamp NOT NULL,
  `APMstaff` tinyint(4) NOT NULL,
  `APMpatient` tinyint(4) NOT NULL,
  PRIMARY KEY (`APMID`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`APMID`, `APMdate`, `APMstaff`, `APMpatient`) VALUES
(1, '2021-03-28 10:15:00', 1, 4);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
