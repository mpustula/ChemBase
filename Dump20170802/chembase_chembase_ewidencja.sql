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
-- Table structure for table `chembase_ewidencja`
--

DROP TABLE IF EXISTS `chembase_ewidencja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chembase_ewidencja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(50) NOT NULL,
  `compound_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chembase_ewidencja_compound_id_819c17cc_fk_chembase_compound_id` (`compound_id`),
  CONSTRAINT `chembase_ewidencja_compound_id_819c17cc_fk_chembase_compound_id` FOREIGN KEY (`compound_id`) REFERENCES `chembase_compound` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chembase_ewidencja`
--

LOCK TABLES `chembase_ewidencja` WRITE;
/*!40000 ALTER TABLE `chembase_ewidencja` DISABLE KEYS */;
INSERT INTO `chembase_ewidencja` VALUES (1,'ewidencja',1420),(2,'ewidencja',3),(3,'ewidencja',5),(4,'ewidencja',6),(5,'ewidencja',9),(6,'ewidencja',10),(7,'ewidencja',11),(8,'ewidencja',13),(9,'ewidencja',15),(10,'ewidencja',20),(11,'ewidencja',63),(12,'ewidencja',181),(13,'ewidencja',232),(14,'ewidencja',234),(15,'ewidencja',240),(16,'ewidencja',264),(17,'ewidencja',273),(18,'ewidencja',296),(19,'ewidencja',337),(20,'ewidencja',352),(21,'ewidencja',356),(22,'ewidencja',488),(23,'ewidencja',504),(24,'ewidencja',520),(25,'ewidencja',548),(26,'ewidencja',555),(27,'ewidencja',561),(28,'ewidencja',589),(29,'ewidencja',599),(30,'ewidencja',605),(31,'ewidencja',616),(32,'ewidencja',658),(33,'ewidencja',751),(34,'ewidencja',797),(35,'ewidencja',807),(36,'ewidencja',935),(37,'ewidencja',936),(38,'ewidencja',944),(39,'ewidencja',946),(40,'ewidencja',947),(41,'ewidencja',951),(42,'ewidencja',954),(43,'ewidencja',1027),(44,'ewidencja',1044),(45,'ewidencja',1066),(46,'ewidencja',1078),(47,'ewidencja',1089),(48,'ewidencja',1136),(49,'ewidencja',1137),(50,'ewidencja',1144),(51,'ewidencja',1151);
/*!40000 ALTER TABLE `chembase_ewidencja` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-02 16:27:15
