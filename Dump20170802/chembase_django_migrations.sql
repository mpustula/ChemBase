CREATE DATABASE  IF NOT EXISTS `chembase` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `chembase`;
-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: chembase
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-07-26 16:44:01.085289'),(2,'auth','0001_initial','2017-07-26 16:44:05.876872'),(3,'admin','0001_initial','2017-07-26 16:44:07.013378'),(4,'admin','0002_logentry_remove_auto_add','2017-07-26 16:44:07.110036'),(5,'contenttypes','0002_remove_content_type_name','2017-07-26 16:44:07.663009'),(6,'auth','0002_alter_permission_name_max_length','2017-07-26 16:44:08.049148'),(7,'auth','0003_alter_user_email_max_length','2017-07-26 16:44:08.531123'),(8,'auth','0004_alter_user_username_opts','2017-07-26 16:44:08.570109'),(9,'auth','0005_alter_user_last_login_null','2017-07-26 16:44:08.932435'),(10,'auth','0006_require_contenttypes_0002','2017-07-26 16:44:08.947489'),(11,'auth','0007_alter_validators_add_error_messages','2017-07-26 16:44:08.968763'),(12,'auth','0008_alter_user_username_max_length','2017-07-26 16:44:09.451741'),(13,'sessions','0001_initial','2017-07-26 16:44:09.769889'),(14,'chembase','0001_initial','2017-07-27 11:54:13.971679'),(15,'chembase','0002_auto_20170728_0645','2017-07-28 06:45:27.258014'),(16,'chembase','0003_auto_20170728_1055','2017-07-28 10:55:47.163112'),(17,'chembase','0004_auto_20170728_1211','2017-07-28 12:11:54.534961'),(18,'chembase','0005_auto_20170802_0954','2017-08-02 09:55:09.623116');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-02 16:27:14
