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
-- Table structure for table `chembase_group`
--

DROP TABLE IF EXISTS `chembase_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chembase_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chembase_group`
--

LOCK TABLES `chembase_group` WRITE;
/*!40000 ALTER TABLE `chembase_group` DISABLE KEYS */;
INSERT INTO `chembase_group` VALUES (1,'Acids'),(2,'Acyl halides'),(3,'Alcohols'),(4,'Aldehydes and ketones'),(5,'Amines'),(6,'Amino acids'),(7,'Boronic acids'),(8,'Carbohydrates'),(9,'Carboxylic acids'),(10,'Dyes'),(11,'Elements'),(12,'Esters and amides'),(13,'Ethers'),(14,'Heterocyclic'),(15,'Hydrides'),(16,'Hydrocarbons'),(17,'Hydroxides'),(18,'Inorganic salts'),(19,'NMR Spectroscopy: solvents and reagents'),(20,'Organic anhydrides'),(21,'Organic halides'),(22,'Organometalic'),(23,'Other'),(24,'Oxides'),(25,'Palladium complexes'),(26,'Phenols'),(27,'Phosphorus compounds'),(28,'Silicon compounds'),(29,'Solvents'),(30,'Solvents, dry'),(31,'Solvents, special purity'),(32,'Sulfur compounds');
/*!40000 ALTER TABLE `chembase_group` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-02 16:27:13
