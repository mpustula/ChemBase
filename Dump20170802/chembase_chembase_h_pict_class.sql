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
-- Table structure for table `chembase_h_pict_class`
--

DROP TABLE IF EXISTS `chembase_h_pict_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chembase_h_pict_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `h_code` varchar(8) NOT NULL,
  `ghs_class_id` int(11) NOT NULL,
  `pictogram_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chembase_h_pict_clas_ghs_class_id_5c5961f8_fk_chembase_` (`ghs_class_id`),
  KEY `chembase_h_pict_clas_pictogram_id_b3ec9534_fk_chembase_` (`pictogram_id`),
  CONSTRAINT `chembase_h_pict_clas_ghs_class_id_5c5961f8_fk_chembase_` FOREIGN KEY (`ghs_class_id`) REFERENCES `chembase_ghsclass` (`id`),
  CONSTRAINT `chembase_h_pict_clas_pictogram_id_b3ec9534_fk_chembase_` FOREIGN KEY (`pictogram_id`) REFERENCES `chembase_pictogram` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chembase_h_pict_class`
--

LOCK TABLES `chembase_h_pict_class` WRITE;
/*!40000 ALTER TABLE `chembase_h_pict_class` DISABLE KEYS */;
INSERT INTO `chembase_h_pict_class` VALUES (1,'H200',23,1),(2,'H201',5,1),(3,'H202',5,1),(4,'H203',5,1),(5,'H204',5,1),(6,'H220',7,2),(8,'H222',7,2),(9,'H223',7,2),(10,'H224',7,2),(11,'H225',7,2),(12,'H226',7,2),(13,'H228',7,2),(14,'H240',12,1),(15,'H241',12,2),(16,'H242',12,2),(17,'H250',13,2),(18,'H251',17,2),(19,'H252',17,2),(20,'H260',24,2),(21,'H261',24,2),(22,'H270',11,3),(23,'H271',11,3),(24,'H272',11,3),(25,'H280',8,4),(26,'H281',8,4),(27,'H290',9,5),(28,'H300',1,6),(29,'H301',1,6),(30,'H302',2,7),(31,'H304',3,8),(32,'H310',1,6),(33,'H311',1,6),(34,'H312',2,7),(35,'H314',18,5),(36,'H315',20,7),(37,'H317',19,7),(38,'H318',6,5),(39,'H319',20,7),(40,'H320',20,7),(41,'H330',1,6),(42,'H331',1,6),(43,'H332',2,7),(44,'H334',16,8),(45,'H335',22,7),(46,'H336',22,7),(47,'H340',10,8),(48,'H341',10,8),(49,'H350',4,8),(50,'H351',4,8),(51,'H360',15,8),(52,'H361',15,8),(54,'H370',21,8),(55,'H371',21,8),(56,'H372',21,8),(57,'H373',21,8);
/*!40000 ALTER TABLE `chembase_h_pict_class` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-02 16:27:16
