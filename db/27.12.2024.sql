/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 10.4.10-MariaDB : Database - sentimentalanalysis
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`sentimentalanalysis` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `sentimentalanalysis`;

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` varchar(100) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`chat_id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`chat_id`,`sender_id`,`receiver_id`,`message`,`date`) values 
(1,2,3,'hai','2024-12-21 17:03:36'),
(2,3,2,'hello','2024-12-21 17:03:54'),
(3,3,2,'how are u?','2024-12-21 17:17:25'),
(4,2,3,'im fine thank you','2024-12-21 17:18:13'),
(5,2,3,'how u doing?','2024-12-22 20:50:09');

/*Table structure for table `comment` */

DROP TABLE IF EXISTS `comment`;

CREATE TABLE `comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` varchar(500) NOT NULL,
  `out` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `post_id` (`post_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `comment` */

insert  into `comment`(`comment_id`,`post_id`,`user_id`,`comment`,`out`) values 
(1,2,2,'looking good!',NULL),
(2,1,1,'perfect ok',NULL),
(3,1,1,'goood!',NULL),
(4,1,1,'its good','positive'),
(5,1,1,'not good','negative');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `complaint` text NOT NULL,
  `reply` text DEFAULT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`complaint_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`user_id`,`complaint`,`reply`,`date`) values 
(1,1,'kjbshbsbhkcsbhk','sasdaaaaaaaaaaa','2024-12-20 22:32:19'),
(2,2,'hhdhhbdhbhbdjd','pending','2024-12-21 08:18:33'),
(3,1,'bad comments','we will manage that','2024-12-22 20:50:30');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `usertype` varchar(100) NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin11','admin11','admin'),
(2,'mrwick11','mrwick11','Blocked'),
(3,'peakyblinders','peakyblinders','user');

/*Table structure for table `post` */

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `post` varchar(2000) NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  `date` datetime NOT NULL,
  `status` enum('pending','approved','rejected') NOT NULL,
  `sentiment` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `post` */

insert  into `post`(`post_id`,`user_id`,`post`,`path`,`date`,`status`,`sentiment`) values 
(3,1,'good vibes','static/images/0f5a07b4-0f79-4ef9-bb69-a7545ecf3f8cteam-3.jpg','2024-12-22 20:33:43','pending',NULL),
(4,1,'Chil Guy!','static/images/98f1e8ac-5a97-433a-957f-15ef3c2681d8team-1.jpg','2024-12-22 20:48:44','pending',NULL),
(5,1,'kjnkjnkjnm','static/images/64adcd2f-1e12-4a15-a99c-e513e250bb2cfinance1.jpg','2024-12-26 09:39:59','pending',NULL),
(7,1,'feeling sad','static/images/f2bb081f-2f73-46a0-b516-3da7842fa0a7finance1.jpg','2024-12-26 09:53:37','pending','negative'),
(8,1,'crying','static/images/09d09076-bba3-4fb4-b030-40a1ed208497finance1.jpg','2024-12-26 09:53:55','pending','negative'),
(9,1,'idont know how to explain','static/images/58dc3737-bd0d-4367-a55f-f857619a268ffinance1.jpg','2024-12-26 09:54:19','pending','neutral'),
(10,1,'She believed she could, so she did','static/images/47943cd4-72f1-42a9-9e1d-f5acec53cd91finance1.jpg','2024-12-26 09:55:52','pending','neutral');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `place` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `login_id` (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(1,2,'john','wick','NY','2222222222','john@gmail.com'),
(2,3,'Thomassss','shelbyss','ssss','4444444444','wwwww@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
