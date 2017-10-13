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
-- Table structure for table `chembase_annotation`
--

DROP TABLE IF EXISTS `chembase_annotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chembase_annotation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `annotation` longtext NOT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chembase_annotation_item_id_c3106c01_fk_chembase_item_id` (`item_id`),
  CONSTRAINT `chembase_annotation_item_id_c3106c01_fk_chembase_item_id` FOREIGN KEY (`item_id`) REFERENCES `chembase_item` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=167 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chembase_annotation`
--

LOCK TABLES `chembase_annotation` WRITE;
/*!40000 ALTER TABLE `chembase_annotation` DISABLE KEYS */;
INSERT INTO `chembase_annotation` VALUES (1,'x3',1),(2,'x2',10),(3,'x2',11),(4,'x2',12),(5,'old ?',17),(6,'x2',19),(7,'x2',20),(8,'finished',24),(9,'x6',35),(10,'x2',37),(11,'x2',44),(12,'x3',78),(13,'x3',79),(14,'x2',83),(15,'red',89),(16,'finished',96),(17,'finished',99),(18,'finished',110),(19,'finished',111),(20,'finished',120),(21,'x2',125),(22,'finished',143),(23,'finished',145),(24,'x2',160),(25,'220',163),(26,'empty',164),(27,'x3',168),(28,'finished',172),(29,'x2',174),(30,'x2',175),(31,'x2',178),(32,'x4',190),(33,'old',191),(34,'x2',196),(35,'x2',199),(36,'x3',216),(37,'moved to 220-SNG-7',228),(38,'x2',235),(39,'x3',239),(40,'finished',249),(41,'x2',264),(42,'finished',270),(43,'x2',280),(44,'x2',281),(45,'x2',284),(46,'x2',290),(47,'x2',302),(48,'x2',310),(49,'x2',322),(50,'x2',323),(51,'x2',348),(52,'x3',356),(53,'x2',357),(54,'x5',378),(55,'x2',386),(56,'x2',388),(57,'x4',398),(58,'x2 (one redistilled)',400),(59,'x2',401),(60,'x3',407),(61,'x2',427),(62,'x2',434),(63,'x2',436),(64,'x3',443),(65,'x5',451),(66,'old',453),(67,'x2',463),(68,'redistilled, 99,5%',538),(69,'old',558),(70,'old',572),(71,'x2',608),(72,'x3',611),(73,'x2',621),(74,'x2',622),(75,'x2',637),(76,'finished',719),(77,'amp. 10 ml',775),(78,'x3',830),(79,'stereochemistry not certain',832),(80,'x3',919),(81,'ampulka',940),(82,'x4',949),(83,'4x 25ml',966),(84,'50 g',967),(85,'x2',972),(86,'99% extra pure',981),(87,'reaction grade >97%',983),(88,'99,95%, amp. 1 ml x9 ',1075),(89,'x4 amp. 1 g (gold label)',1077),(90,'x11  amp. 1 ml',1078),(91,'biotechnology performance certified',1079),(92,' 99.7%, amp. 0.75 ml (x2)',1080),(93,'amp. 100 g, 99,8%',1082),(94,'amp. 1 ml (x4)',1083),(95,'50 ml',1084),(96,'amp. 0.7 ml, x4',1085),(97,'sklad: chloroform, dmso, TMS',1086),(98,'amp. 1 g (x4)  ',1088),(99,'amp. 10 ml',1092),(100,' amp. 1 ml (x2)',1096),(101,'x3',1099),(102,'amp. 10g',1100),(103,'x2',1102),(104,'x2',1103),(105,'x3',1104),(106,'x2',1105),(107,' for HPLC',1149),(108,'for HPLC',1150),(109,'for HPLC',1151),(110,' for HPLC',1152),(111,'x2',1185),(112,'x4',1227),(113,'x4',1228),(114,'99% extra pure',1288),(115,'1000 ml x2',1308),(116,'x3  99,8%,  amp. 10 ml',1309),(117,'amp. 0.75 ml x9',1310),(118,'amp. 0.75 ml x5',1311),(119,'99.96% amp. 0.8 ml',1312),(120,'99.8%, amp. 0.5 ml',1313),(121,'amp. 1 ml',1314),(122,'empty',1316),(123,' 99.7%, amp. 0.75 ml (x2)',1317),(124,' 99.7%, amp. 0.75 ml (x2)',1318),(125,' 99.7%, amp. 0.75 ml (x2)',1319),(126,' 99.7%, amp. 0.75 ml (x2)',1320),(127,'99%, amp. 1.0 ml (x6)',1321),(128,'amp. 1 ml (x6)',1327),(129,'amp. 1 g',1328),(130,'amp. 1 g',1329),(131,'amp. 1 g',1330),(132,' amp. 1 g',1331),(133,'amp. 1 g',1332),(134,' amp. 10 ml',1333),(135,'sklad: chloroform, dmso, TMS',1334),(136,'sklad: chloroform, dmso, TMS',1335),(137,'sklad: chloroform, dmso, TMS',1336),(138,'sklad: chloroform, dmso, TMS',1337),(139,'amp. 1 ml',1338),(140,'amp. 1 ml',1339),(141,'amp. 1 ml',1340),(142,' amp. 1 ml',1341),(143,'amp. 1 ml',1347),(144,'amp. 10 ml',1348),(145,'amp. 10 ml',1349),(146,' amp. 10 ml',1350),(147,' amp. 1 ml',1351),(148,'amp. 1 ml',1357),(149,'x2  amp. 1 ml',1358),(150,'x3 amp. 10 ml',1359),(151,' amp. 10 g',1360),(152,' amp. 1 ml (x5)',1361),(153,' amp. 1 ml (x3)',1362),(154,' for HPLC',1366),(155,'for HPLC',1367),(156,'for HPLC',1368),(157,' absolut, 99.8%',1370),(158,' absolut, 99.8%',1371),(159,' absolut, 99.8%',1372),(160,' absolut, 99.8%',1373),(161,'anhydrous',1375),(162,'anhydrous',1376),(163,' anhydrous',1377),(164,'anhydrous 99.8%',1378),(165,'dry',1379),(166,'unknown concentration',1387);
/*!40000 ALTER TABLE `chembase_annotation` ENABLE KEYS */;
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
