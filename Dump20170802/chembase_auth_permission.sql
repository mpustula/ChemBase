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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add user',2,'add_user'),(5,'Can change user',2,'change_user'),(6,'Can delete user',2,'delete_user'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add groups',7,'add_groups'),(20,'Can change groups',7,'change_groups'),(21,'Can delete groups',7,'delete_groups'),(22,'Can add history',8,'add_history'),(23,'Can change history',8,'change_history'),(24,'Can delete history',8,'delete_history'),(25,'Can add pictogram',9,'add_pictogram'),(26,'Can change pictogram',9,'change_pictogram'),(27,'Can delete pictogram',9,'delete_pictogram'),(28,'Can add item',10,'add_item'),(29,'Can change item',10,'change_item'),(30,'Can delete item',10,'delete_item'),(31,'Can add compound',11,'add_compound'),(32,'Can change compound',11,'change_compound'),(33,'Can delete compound',11,'delete_compound'),(34,'Can add ghs class',12,'add_ghsclass'),(35,'Can change ghs class',12,'change_ghsclass'),(36,'Can delete ghs class',12,'delete_ghsclass'),(37,'Can add annotation',13,'add_annotation'),(38,'Can change annotation',13,'change_annotation'),(39,'Can delete annotation',13,'delete_annotation'),(40,'Can add h_ pict_ class',14,'add_h_pict_class'),(41,'Can change h_ pict_ class',14,'change_h_pict_class'),(42,'Can delete h_ pict_ class',14,'delete_h_pict_class'),(43,'Can add cmpd_ class',15,'add_cmpd_class'),(44,'Can change cmpd_ class',15,'change_cmpd_class'),(45,'Can delete cmpd_ class',15,'delete_cmpd_class'),(46,'Can add ewidencja',16,'add_ewidencja'),(47,'Can change ewidencja',16,'change_ewidencja'),(48,'Can delete ewidencja',16,'delete_ewidencja'),(49,'Can add group',7,'add_group'),(50,'Can change group',7,'change_group'),(51,'Can delete group',7,'delete_group');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
