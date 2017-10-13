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
-- Table structure for table `chembase_cmpd_class`
--

DROP TABLE IF EXISTS `chembase_cmpd_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chembase_cmpd_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(10) NOT NULL,
  `compound_id` int(11) NOT NULL,
  `ghs_class_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chembase_cmpd_class_compound_id_e3a14784_fk_chembase_compound_id` (`compound_id`),
  KEY `chembase_cmpd_class_ghs_class_id_a108aad8_fk_chembase_` (`ghs_class_id`),
  CONSTRAINT `chembase_cmpd_class_compound_id_e3a14784_fk_chembase_compound_id` FOREIGN KEY (`compound_id`) REFERENCES `chembase_compound` (`id`),
  CONSTRAINT `chembase_cmpd_class_ghs_class_id_a108aad8_fk_chembase_` FOREIGN KEY (`ghs_class_id`) REFERENCES `chembase_ghsclass` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2066 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chembase_cmpd_class`
--

LOCK TABLES `chembase_cmpd_class` WRITE;
/*!40000 ALTER TABLE `chembase_cmpd_class` DISABLE KEYS */;
INSERT INTO `chembase_cmpd_class` VALUES (1,'3',1420,7),(2,'1A',1420,18),(3,'2',1,20),(4,'1',1,6),(5,'1B',2,18),(6,'3',2,22),(7,'2',3,7),(8,'2',3,20),(9,'1B',3,10),(10,'1A',3,4),(11,'1',3,21),(12,'1',3,3),(13,'3',4,1),(14,'1B',4,19),(15,'2',4,4),(16,'1',4,21),(17,'2',5,7),(18,'1',5,1),(19,'1',6,1),(20,'1',6,6),(21,'1',7,9),(22,'1',7,1),(23,'1',7,21),(24,'2',8,1),(25,'2',8,21),(26,'1',9,9),(27,'4',9,2),(28,'1A',9,18),(29,'1',10,9),(30,'1A',10,18),(31,'1',11,9),(32,'1B',11,18),(33,'3',11,22),(34,'2',12,24),(35,'1B',12,18),(36,'1',13,1),(37,'2',13,21),(38,'1',14,1),(39,'1B',14,18),(40,'1',14,16),(41,'1',15,9),(42,'1A',15,18),(43,'2',16,20),(44,'1A',17,18),(45,'1B',18,18),(46,'1B',19,18),(47,'4',20,2),(48,'3',20,1),(49,'1A',20,18),(50,'4',21,2),(51,'2',21,1),(52,'1B',21,18),(53,'2',21,21),(54,'4',22,2),(55,'1B',22,18),(56,'1',22,16),(57,'1',22,19),(58,'2',22,21),(59,'2',24,20),(60,'4',25,2),(61,'1A',25,18),(62,'1B',25,15),(63,'1',25,21),(64,'4',26,2),(65,'4',27,2),(66,'1',27,6),(67,'3',27,22),(68,'3',28,7),(69,'3',28,1),(70,'1',28,6),(71,'3',29,7),(72,'2',30,7),(73,'2',30,20),(74,'2',32,20),(75,'4',33,2),(76,'2',33,20),(77,'1',33,6),(78,'1',33,16),(79,'1',33,19),(80,'3',33,22),(81,'4',34,2),(82,'2',36,7),(83,'2',36,20),(84,'1B',36,15),(85,'4',37,2),(86,'1B',37,18),(87,'2',38,1),(88,'3',39,1),(89,'1',40,6),(90,'1',40,16),(91,'1',40,19),(92,'4',42,2),(93,'1B',42,18),(94,'1',42,16),(95,'1',42,19),(96,'3',42,22),(97,'1',43,6),(98,'1',43,16),(99,'1',43,19),(100,'4',44,2),(101,'2',44,20),(102,'1',44,6),(103,'3',44,22),(104,'2',45,20),(105,'3',45,22),(106,'3',46,7),(107,'4',46,2),(108,'3',46,1),(109,'4',47,2),(110,'2',47,20),(111,'3',47,22),(112,'2',49,24),(113,'4',50,2),(114,'2',50,20),(115,'1',50,6),(116,'3',50,22),(117,'4',51,2),(118,'1B',51,18),(119,'2',52,20),(120,'2',53,20),(121,'3',53,22),(122,'1',54,19),(123,'4',55,2),(124,'3',56,7),(125,'2',56,1),(126,'2',56,20),(127,'2',57,7),(128,'2',57,15),(129,'1',57,21),(130,'2',57,20),(131,'1',58,7),(132,'4',58,2),(133,'2',58,20),(134,'3',58,22),(135,'2',59,7),(136,'2',59,20),(137,'3',59,22),(138,'4',60,2),(139,'2',60,20),(140,'3',60,22),(141,'2',61,20),(142,'3',61,22),(143,'1',63,1),(144,'2',63,20),(145,'1',63,16),(146,'3',63,22),(147,'4',65,2),(148,'2',68,20),(149,'1',68,19),(150,'3',68,22),(151,'3',70,7),(152,'2',70,20),(153,'2',71,20),(154,'3',72,7),(155,'4',72,2),(156,'2',72,20),(157,'1',72,6),(158,'3',73,7),(159,'4',73,2),(160,'3',74,7),(161,'3',75,7),(162,'4',75,2),(163,'3',76,7),(164,'4',76,2),(165,'1',76,6),(166,'2',77,20),(167,'3',77,22),(168,'2',78,7),(169,'2',78,20),(170,'3',78,22),(171,'2',79,7),(172,'2',79,20),(173,'',79,22),(174,'1',80,1),(175,'1B',80,18),(176,'2',80,10),(177,'4',81,2),(178,'2',81,20),(179,'3',81,22),(180,'3',82,1),(181,'1B',82,18),(182,'1',82,19),(183,'2',83,4),(184,'4',84,2),(185,'2',84,20),(186,'3',84,22),(187,'4',85,2),(188,'2',85,20),(189,'3',85,22),(190,'2',86,1),(191,'4',86,2),(192,'2',86,20),(193,'1',86,6),(194,'3',86,22),(195,'4',87,2),(196,'2',88,20),(197,'1',88,19),(198,'2',89,20),(199,'3',89,22),(200,'4',90,2),(201,'3',92,1),(202,'3',106,1),(203,'1',106,19),(204,'2',116,20),(205,'3',116,22),(206,'4',117,2),(207,'1',117,6),(208,'2',118,20),(209,'3',118,22),(210,'4',119,2),(211,'2',119,20),(212,'1',119,6),(213,'3',119,22),(214,'2',120,20),(215,'3',121,22),(216,'1',121,6),(217,'1',121,19),(218,'4',121,2),(219,'2',122,20),(220,'3',122,22),(221,'4',124,2),(222,'2',125,20),(223,'1',125,6),(224,'3',125,22),(225,'4',126,2),(226,'1',126,6),(227,'4',127,2),(228,'1',127,19),(229,'1',127,6),(230,'2',128,20),(231,'3',128,22),(232,'4',131,2),(233,'2',131,20),(234,'3',131,22),(235,'2',132,20),(236,'2',132,4),(237,'2',132,15),(238,'3',132,22),(239,'4',133,2),(240,'1',133,6),(241,'2',134,20),(242,'3',134,22),(243,'1A',137,18),(244,'3',137,1),(245,'1',137,19),(246,'4',138,2),(247,'1B',138,18),(248,'2',139,20),(249,'4',140,2),(250,'1B',140,18),(251,'2',141,20),(252,'1',141,6),(253,'2',142,20),(254,'3',142,22),(255,'1B',143,18),(256,'1',144,6),(257,'1B',145,18),(258,'1',146,9),(259,'1B',146,18),(260,'3',146,22),(261,'2',147,20),(262,'3',147,22),(263,'1',149,6),(264,'2',157,20),(265,'3',157,22),(266,'4',158,2),(267,'2',158,20),(268,'1',158,6),(269,'3',158,22),(270,'3',160,1),(271,'2',160,21),(272,'4',161,2),(273,'2',161,20),(274,'4',162,2),(275,'2',162,20),(276,'3',162,22),(277,'2',163,1),(278,'2',163,20),(279,'3',163,22),(280,'4',164,2),(281,'3',164,1),(282,'2',164,20),(283,'1',164,6),(284,'3',164,22),(285,'4',166,2),(286,'2',167,7),(287,'4',167,2),(288,'2',167,20),(289,'3',168,7),(290,'4',168,2),(291,'3',168,1),(292,'1A',168,18),(293,'3',169,7),(294,'2',169,20),(295,'3',169,22),(296,'2',170,7),(297,'4',170,2),(298,'1B',170,18),(299,'3',171,1),(300,'4',171,2),(301,'2',171,20),(302,'1',171,19),(303,'2',171,10),(304,'2',171,4),(305,'3',172,7),(306,'3',172,1),(307,'4',172,2),(308,'1B',172,18),(309,'4',173,2),(310,'2',173,20),(311,'3',173,22),(312,'2',174,7),(313,'4',174,2),(314,'3',174,1),(315,'1B',174,18),(316,'3',174,22),(317,'2',175,7),(318,'1B',175,18),(319,'3',175,22),(320,'2',176,7),(321,'3',176,1),(322,'2',176,20),(323,'1',176,6),(324,'1',176,21),(325,'3',177,7),(326,'4',177,2),(327,'3',177,1),(328,'1A',177,18),(329,'1',177,16),(330,'1',177,19),(331,'2',178,7),(332,'4',178,2),(333,'3',178,1),(334,'1A',178,18),(335,'2',179,7),(336,'4',179,2),(337,'3',179,1),(338,'1A',179,18),(339,'2',180,20),(340,'4',181,2),(341,'1',181,1),(342,'2',181,20),(343,'4',182,2),(344,'2',182,20),(345,'1',182,19),(346,'2',182,10),(347,'2',182,4),(348,'3',183,1),(349,'2',183,20),(350,'3',183,22),(351,'2',184,20),(352,'2',185,7),(353,'4',185,2),(354,'3',185,1),(355,'1A',185,18),(356,'2',186,20),(357,'3',186,22),(358,'1',187,7),(359,'3',187,1),(360,'1A',187,18),(361,'3',187,22),(362,'4',188,2),(363,'1B',188,18),(364,'1B',189,18),(365,'4',190,2),(366,'2',190,20),(367,'3',190,22),(368,'3',191,1),(369,'1',191,6),(370,'1',191,19),(371,'2',191,10),(372,'2',191,4),(373,'1',191,21),(374,'3',192,1),(375,'2',193,10),(376,'4',193,2),(377,'1B',194,18),(378,'4',194,2),(379,'3',195,1),(380,'1',196,7),(381,'4',197,2),(382,'4',199,2),(383,'2',199,20),(384,'1',199,6),(385,'4',201,2),(386,'1B',201,18),(387,'4',202,2),(388,'2',202,20),(389,'2',203,20),(390,'3',203,22),(391,'2',204,20),(392,'2',205,20),(393,'3',205,22),(394,'2',208,11),(395,'2',208,20),(396,'3',208,22),(397,'2',210,20),(398,'3',210,22),(399,'2',212,11),(400,'1',212,9),(401,'4',212,2),(402,'1C',212,18),(403,'1',212,19),(404,'4',217,2),(405,'2',217,20),(406,'3',217,22),(407,'1',217,21),(408,'2',218,20),(409,'3',218,22),(410,'1',219,7),(411,'4',222,2),(412,'1B',222,19),(413,'1B',222,15),(414,'1',223,24),(415,'1',223,13),(416,'1B',224,18),(417,'2',226,7),(418,'1',227,7),(419,'1',227,19),(420,'2',227,4),(421,'4',228,2),(422,'1',228,6),(423,'1',228,16),(424,'1',228,19),(425,'2',228,10),(426,'1B',228,4),(427,'1B',228,15),(428,'4',229,2),(429,'1B',229,18),(430,'1',229,19),(431,'2',229,10),(432,'2',229,15),(433,'3',229,22),(434,'',229,21),(435,'4',230,2),(436,'1B',231,18),(437,'',231,21),(438,'3',232,1),(439,'2',232,20),(440,'1',232,16),(441,'1',232,19),(442,'2',232,10),(443,'1A',232,4),(444,'1B',232,15),(445,'1',232,21),(446,'4',233,2),(447,'3',233,1),(448,'2',233,20),(449,'3',233,22),(450,'1',234,11),(451,'2',234,1),(452,'1A',234,18),(453,'1',234,16),(454,'1',234,19),(455,'1B',234,10),(456,'1A',234,4),(457,'2',234,15),(458,'1',234,21),(459,'4',235,2),(460,'1A',235,18),(461,'3',235,22),(462,'3',236,1),(463,'2',236,21),(464,'4',238,2),(465,'1',240,1),(466,'2',240,21),(467,'4',241,2),(468,'1B',241,18),(469,'4',242,2),(470,'2',242,20),(471,'4',244,2),(472,'1B',244,18),(473,'1',245,9),(474,'4',245,2),(475,'2',245,20),(476,'1',245,19),(477,'2',245,4),(478,'2',245,21),(479,'4',246,2),(480,'3',247,11),(481,'2',247,20),(482,'1',247,16),(483,'1',247,19),(484,'4',247,2),(485,'3',247,22),(486,'4',248,2),(487,'2',248,4),(488,'2',248,15),(489,'2',252,20),(490,'2',253,20),(491,'1',253,6),(492,'3',253,22),(493,'2',254,20),(494,'1',254,6),(495,'3',254,22),(496,'1',255,24),(497,'3',256,1),(498,'1',258,7),(499,'1',258,24),(500,'1A',258,18),(501,'1',259,24),(502,'1B',259,18),(503,'2',261,20),(504,'4',262,2),(505,'2',262,20),(506,'2',264,11),(507,'2',264,1),(508,'4',264,2),(509,'1B',264,18),(510,'1',264,16),(511,'1',264,19),(512,'1B',264,10),(513,'1B',264,4),(514,'1B',264,15),(515,'1',264,21),(516,'4',265,2),(517,'3',266,11),(518,'2',267,11),(519,'4',267,2),(520,'1B',267,18),(521,'4',268,2),(522,'2',268,20),(523,'4',269,2),(524,'1B',269,18),(525,'1',270,24),(526,'1A',270,18),(527,'2',271,20),(528,'3',272,1),(529,'2',273,11),(530,'2',273,1),(531,'4',273,2),(532,'1B',273,18),(533,'1',273,16),(534,'1',273,19),(535,'1B',273,10),(536,'1B',273,4),(537,'1B',273,15),(538,'1',273,21),(539,'1',274,24),(540,'3',274,1),(541,'1B',274,18),(542,'1B',274,15),(543,'1',275,24),(544,'2',276,11),(545,'4',276,2),(546,'1',276,6),(547,'1B',276,15),(548,'3',276,22),(549,'1',278,11),(550,'1C',278,18),(551,'1',278,21),(552,'2',279,20),(553,'1',282,17),(554,'4',282,2),(555,'4',283,2),(556,'1',283,6),(557,'3',284,11),(558,'3',284,1),(559,'2',284,20),(560,'4',286,2),(561,'2',286,20),(562,'3',286,22),(563,'2',289,20),(564,'3',289,22),(565,'2',291,20),(566,'3',291,22),(567,'4',292,2),(568,'2',292,20),(569,'2',293,7),(570,'4',293,2),(571,'2',293,20),(572,'3',293,22),(573,'3',296,7),(574,'1',296,9),(575,'1',296,1),(576,'1',296,6),(577,'3',298,7),(578,'3',298,1),(579,'4',298,2),(580,'2',298,20),(581,'1',298,6),(582,'3',298,22),(583,'3',300,1),(584,'1B',300,18),(585,'2',300,10),(586,'2',300,21),(587,'4',301,2),(588,'4',302,2),(589,'2',302,20),(590,'4',303,2),(591,'3',304,1),(592,'2',304,20),(593,'2',305,20),(594,'1',305,6),(595,'3',305,22),(596,'2',307,10),(597,'4',307,2),(598,'3',310,1),(599,'4',310,2),(600,'2',310,20),(601,'1',310,6),(602,'1',310,19),(603,'2',310,10),(604,'2',311,4),(605,'4',311,2),(606,'2',311,20),(607,'2',313,20),(608,'3',313,22),(609,'4',314,2),(610,'2',314,20),(611,'2',320,1),(612,'4',320,2),(613,'1',320,6),(614,'2',320,4),(615,'1B',320,15),(616,'1',321,6),(617,'2',322,7),(618,'4',322,2),(619,'2',322,20),(620,'3',322,22),(621,'4',323,2),(622,'2',323,20),(623,'1',323,16),(624,'1',323,19),(625,'3',323,22),(626,'2',324,1),(627,'1',324,19),(628,'3',325,7),(629,'4',325,2),(630,'2',325,20),(631,'3',326,7),(632,'2',326,20),(633,'3',326,22),(634,'2',327,7),(635,'2',328,20),(636,'3',328,22),(637,'4',329,2),(638,'2',329,20),(639,'3',329,22),(640,'3',330,7),(641,'4',330,2),(642,'1B',331,18),(643,'1',331,19),(644,'2',331,1),(645,'1B',332,18),(646,'3',333,7),(647,'1B',334,18),(648,'4',335,2),(649,'1',335,19),(650,'4',336,2),(651,'2',336,20),(652,'1',336,19),(653,'3',336,22),(654,'4',337,2),(655,'1',337,1),(656,'2',337,20),(657,'1',337,6),(658,'1',337,19),(659,'1B',337,10),(660,'1B',337,4),(661,'3',337,22),(662,'2',337,21),(663,'1B',338,18),(664,'2',339,4),(665,'2',339,20),(666,'4',340,2),(667,'4',342,2),(668,'2',342,20),(669,'3',344,1),(670,'2',344,20),(671,'1',344,6),(672,'3',344,22),(673,'2',345,20),(674,'2',346,20),(675,'1',346,19),(676,'2',346,4),(677,'',346,22),(678,'3',347,1),(679,'4',347,2),(680,'2',347,20),(681,'3',347,22),(682,'3',348,1),(683,'4',348,2),(684,'2',348,20),(685,'1',348,16),(686,'1',348,19),(687,'2',348,4),(688,'3',348,22),(689,'2',349,7),(690,'1A',349,15),(691,'2',349,21),(692,'2',352,11),(693,'1',352,19),(694,'1B',352,4),(695,'3',353,7),(696,'1',353,3),(697,'2',354,7),(698,'3',354,1),(699,'4',354,2),(700,'1A',354,18),(701,'4',355,2),(702,'2',356,7),(703,'1B',356,10),(704,'1A',356,4),(705,'2',356,21),(706,'4',358,2),(707,'1',358,19),(708,'',358,21),(709,'3',359,7),(710,'1',359,13),(711,'4',359,2),(712,'1B',359,18),(713,'1B',361,18),(714,'3',362,7),(715,'2',362,20),(716,'3',362,22),(717,'4',364,2),(718,'3',365,1),(719,'1B',365,18),(720,'1',368,9),(721,'3',368,1),(722,'1B',368,18),(723,'2',369,7),(724,'2',369,1),(725,'4',369,2),(726,'1B',369,18),(727,'2',371,20),(728,'3',371,22),(729,'1B',372,18),(730,'3',373,7),(731,'4',375,2),(732,'2',375,20),(733,'2',375,4),(734,'3',377,7),(735,'4',378,2),(736,'1B',378,18),(737,'4',379,2),(738,'3',379,1),(739,'1B',379,18),(740,'2',380,20),(741,'3',380,22),(742,'2',381,20),(743,'3',381,22),(744,'4',384,2),(745,'3',384,1),(746,'2',384,20),(747,'2',384,4),(748,'2',384,15),(749,'1',384,21),(750,'2',385,20),(751,'2',385,4),(752,'3',385,22),(753,'',385,21),(754,'1',386,6),(755,'2',387,7),(756,'1',387,9),(757,'2',387,20),(758,'2',387,4),(759,'3',387,22),(760,'D',388,12),(761,'2',388,20),(762,'1',388,19),(763,'3',388,22),(764,'3',389,7),(765,'4',389,2),(766,'3',389,1),(767,'1A',389,18),(768,'1B',390,18),(769,'2',391,7),(770,'4',391,2),(771,'2',391,20),(772,'2',391,15),(773,'2',391,21),(774,'3',391,22),(775,'1',391,3),(776,'2',392,7),(777,'4',392,2),(778,'2',392,20),(779,'1',393,1),(780,'2',394,7),(781,'2',394,20),(782,'3',394,22),(783,'1',396,7),(784,'2',396,20),(785,'3',396,22),(786,'3',397,1),(787,'2',397,21),(788,'4',398,2),(789,'1B',398,18),(790,'2',399,7),(791,'3',399,1),(792,'1B',399,18),(793,'1B',399,4),(794,'3',399,22),(795,'1',400,7),(796,'4',400,2),(797,'2',400,20),(798,'2',400,10),(799,'1B',400,4),(800,'2',400,21),(801,'2',401,7),(802,'1',401,1),(803,'1B',401,18),(804,'1',401,19),(805,'2',403,7),(806,'4',403,2),(807,'3',403,1),(808,'2',403,20),(809,'1',403,6),(810,'3',403,22),(811,'2',404,7),(812,'2',404,20),(813,'1',404,19),(814,'3',404,22),(815,'2',405,20),(816,'1B',406,18),(817,'3',406,22),(818,'3',407,7),(819,'2',407,1),(820,'2',407,20),(821,'1',407,6),(822,'1',407,16),(823,'1',407,19),(824,'3',407,22),(825,'2',408,20),(826,'3',408,22),(827,'2',409,20),(828,'3',409,22),(829,'3',410,7),(830,'3',411,1),(831,'3',412,7),(832,'4',412,2),(833,'2',412,1),(834,'2',412,20),(835,'3',412,22),(836,'1',414,7),(837,'4',414,2),(838,'2',415,7),(839,'4',415,2),(840,'3',415,1),(841,'1A',415,18),(842,'3',415,22),(843,'2',416,7),(844,'3',416,1),(845,'1A',416,18),(846,'3',417,7),(847,'4',417,2),(848,'3',417,1),(849,'1B',417,18),(850,'1',417,16),(851,'1',417,19),(852,'2',418,7),(853,'1B',418,18),(854,'4',418,2),(855,'2',419,7),(856,'2',419,20),(857,'3',419,22),(858,'3',420,7),(859,'3',420,1),(860,'4',420,2),(861,'1',420,6),(862,'1',422,7),(863,'2',422,20),(864,'2',422,4),(865,'3',422,22),(866,'2',424,7),(867,'4',425,2),(868,'1B',425,18),(869,'1',425,19),(870,'3',426,7),(871,'3',426,1),(872,'3',427,7),(873,'3',428,7),(874,'4',428,2),(875,'1B',430,18),(876,'1B',430,4),(877,'3',430,22),(878,'4',431,2),(879,'2',431,20),(880,'1',431,6),(881,'3',431,22),(882,'3',432,7),(883,'4',432,2),(884,'4',434,2),(885,'1B',434,18),(886,'2',435,7),(887,'3',435,1),(888,'1B',435,18),(889,'1B',435,10),(890,'1B',435,4),(891,'4',436,2),(892,'2',438,7),(893,'2',438,20),(894,'2',438,15),(895,'3',438,22),(896,'2',438,21),(897,'1',438,3),(898,'2',439,1),(899,'1A',439,18),(900,'2',440,7),(901,'1',440,24),(902,'4',440,2),(903,'2',440,20),(904,'1',440,6),(905,'2',440,4),(906,'3',440,22),(907,'2',441,7),(908,'3',442,7),(909,'2',442,20),(910,'3',442,22),(911,'3',443,7),(912,'1',443,1),(913,'3',444,7),(914,'3',444,1),(915,'2',444,20),(916,'3',444,22),(917,'2',445,7),(918,'4',445,2),(919,'3',445,1),(920,'3',446,1),(921,'1B',446,18),(922,'3',447,7),(923,'3',447,1),(924,'4',447,2),(925,'2',447,20),(926,'1',447,21),(927,'2',449,7),(928,'1',449,13),(929,'2',449,24),(930,'1A',449,18),(931,'2',449,4),(932,'3',449,22),(933,'',449,21),(934,'2',450,7),(935,'4',450,2),(936,'1B',450,18),(937,'2',450,4),(938,'3',450,22),(939,'2',451,7),(940,'1B',451,18),(941,'2',451,4),(942,'3',451,22),(943,'2',452,7),(944,'1',452,13),(945,'1',452,24),(946,'1B',452,18),(947,'2',452,15),(948,'3',452,22),(949,'2',452,21),(950,'1',452,3),(951,'2',453,7),(952,'1',453,13),(953,'2',453,24),(954,'1B',453,18),(955,'2',453,15),(956,'3',453,22),(957,'2',453,21),(958,'1',453,3),(959,'1',454,24),(960,'3',454,1),(961,'1B',454,18),(962,'2',455,7),(963,'1',455,24),(964,'1B',455,18),(965,'3',455,22),(966,'2',456,1),(967,'2',456,21),(968,'4',457,2),(969,'1',461,9),(970,'4',461,2),(971,'2',461,20),(972,'1',461,6),(973,'1',461,19),(974,'2',461,4),(975,'3',461,22),(976,'2',461,21),(977,'2',462,20),(978,'1',462,6),(979,'3',462,22),(980,'3',465,7),(981,'4',465,2),(982,'3',465,1),(983,'2',465,20),(984,'1',465,6),(985,'1',465,19),(986,'3',465,22),(987,'2',465,21),(988,'1',465,3),(989,'2',466,20),(990,'2',466,4),(991,'3',466,22),(992,'2',466,21),(993,'1',467,19),(994,'2',468,20),(995,'3',468,22),(996,'2',469,7),(997,'1',469,13),(998,'1',469,24),(999,'1B',469,18),(1000,'2',469,15),(1001,'3',469,22),(1002,'2',469,21),(1003,'1',469,3),(1004,'2',470,7),(1005,'4',470,2),(1006,'2',470,20),(1007,'1B',470,15),(1008,'',470,21),(1009,'2',472,20),(1010,'1',472,16),(1011,'3',472,22),(1012,'1B',473,18),(1013,'1',473,16),(1014,'1',473,19),(1015,'1B',474,18),(1016,'3',475,7),(1017,'4',475,2),(1018,'2',475,20),(1019,'3',475,22),(1020,'1B',476,18),(1021,'3',477,7),(1022,'1B',477,18),(1023,'3',477,22),(1024,'1',479,6),(1025,'4',481,2),(1026,'2',481,20),(1027,'2',481,4),(1028,'3',481,22),(1029,'',481,21),(1030,'2',482,20),(1031,'3',482,22),(1032,'3',483,1),(1033,'2',486,7),(1034,'3',486,1),(1035,'1',488,1),(1036,'1B',488,18),(1037,'3',489,1),(1038,'1B',489,18),(1039,'3',489,22),(1040,'2',491,7),(1041,'2',491,20),(1042,'3',491,22),(1043,'1B',492,18),(1044,'1B',493,18),(1045,'1B',494,18),(1046,'4',495,2),(1047,'2',495,20),(1048,'3',497,1),(1049,'1',497,6),(1050,'1B',498,18),(1051,'1',498,6),(1052,'4',500,2),(1053,'2',500,20),(1054,'3',500,22),(1055,'2',501,20),(1056,'3',501,22),(1057,'2',502,20),(1058,'3',502,22),(1059,'1',503,6),(1060,'1',504,1),(1061,'1B',504,18),(1062,'3',504,22),(1063,'2',505,20),(1064,'3',505,22),(1065,'4',506,2),(1066,'2',509,20),(1067,'3',509,22),(1068,'4',511,2),(1069,'1B',511,18),(1070,'3',511,22),(1071,'2',513,7),(1072,'3',513,1),(1073,'1B',513,18),(1074,'1',513,21),(1075,'1B',516,18),(1076,'2',519,7),(1077,'4',519,2),(1078,'3',519,1),(1079,'1A',519,18),(1080,'3',520,1),(1081,'1B',520,18),(1082,'1',520,19),(1083,'1B',520,4),(1084,'2',521,1),(1085,'2',521,20),(1086,'3',521,22),(1087,'2',522,20),(1088,'3',522,22),(1089,'3',523,1),(1090,'2',523,21),(1091,'4',525,2),(1092,'2',525,20),(1093,'3',525,22),(1094,'2',526,7),(1095,'4',526,2),(1096,'3',526,1),(1097,'1B',526,18),(1098,'4',527,2),(1099,'1',527,16),(1100,'4',528,2),(1101,'2',528,20),(1102,'1',528,19),(1103,'3',528,22),(1104,'4',530,2),(1105,'3',530,1),(1106,'2',530,21),(1107,'4',531,2),(1108,'3',532,7),(1109,'4',532,2),(1110,'1B',532,18),(1111,'2',533,20),(1112,'3',533,22),(1113,'2',534,20),(1114,'3',534,22),(1115,'2',535,20),(1116,'3',535,22),(1117,'2',536,7),(1118,'1B',536,18),(1119,'2',538,7),(1120,'4',538,2),(1121,'3',538,1),(1122,'1B',538,18),(1123,'1B',539,18),(1124,'4',542,2),(1125,'4',543,2),(1126,'2',543,20),(1127,'3',544,7),(1128,'4',544,2),(1129,'3',544,1),(1130,'1A',544,18),(1131,'4',545,2),(1132,'2',545,20),(1133,'3',545,22),(1134,'2',546,20),(1135,'3',546,22),(1136,'2',547,7),(1137,'1B',547,18),(1138,'3',547,22),(1139,'3',548,11),(1140,'1',548,9),(1141,'1A',548,18),(1142,'2',549,20),(1143,'3',549,22),(1144,'2',551,20),(1145,'3',551,22),(1146,'3',552,7),(1147,'4',552,2),(1148,'3',552,1),(1149,'1B',552,18),(1150,'1B',553,15),(1151,'3',554,7),(1152,'2',554,20),(1153,'3',554,22),(1154,'3',555,7),(1155,'1',555,1),(1156,'2',555,20),(1157,'1',555,6),(1158,'1',555,19),(1159,'3',555,22),(1160,'4',558,2),(1161,'1B',558,18),(1162,'2',559,20),(1163,'3',559,22),(1164,'2',560,20),(1165,'3',560,22),(1166,'1',561,1),(1167,'2',561,7),(1168,'1B',561,18),(1169,'2',562,7),(1170,'2',562,20),(1171,'4',563,2),(1172,'4',565,2),(1173,'2',565,20),(1174,'3',565,22),(1175,'2',567,20),(1176,'1B',568,18),(1177,'3',569,7),(1178,'2',571,20),(1179,'3',571,22),(1180,'4',573,2),(1181,'2',573,20),(1182,'2',577,20),(1183,'3',577,22),(1184,'3',578,7),(1185,'2',578,20),(1186,'3',578,22),(1187,'D',579,12),(1188,'2',579,20),(1189,'1',579,19),(1190,'3',579,22),(1191,'2',581,7),(1192,'4',581,2),(1193,'3',581,1),(1194,'2',581,20),(1195,'1',581,19),(1196,'3',581,22),(1197,'C',583,12),(1198,'2',583,20),(1199,'1',583,19),(1200,'4',584,2),(1201,'1A',584,18),(1202,'1C',585,18),(1203,'1',585,6),(1204,'1B',586,18),(1205,'1',587,9),(1206,'4',587,2),(1207,'1B',587,18),(1208,'3',587,22),(1209,'1',589,1),(1210,'1A',589,18),(1211,'1',589,21),(1212,'1',590,11),(1213,'1',590,9),(1214,'4',590,2),(1215,'1A',590,18),(1216,'2',590,21),(1217,'1B',591,18),(1218,'1B',592,18),(1219,'4',593,2),(1220,'1',593,21),(1221,'1B',594,18),(1222,'3',594,22),(1223,'4',597,2),(1224,'2',597,20),(1225,'3',597,22),(1226,'3',598,7),(1227,'1B',598,18),(1228,'1',599,1),(1229,'2',599,20),(1230,'1',599,6),(1231,'3',599,22),(1232,'2',600,7),(1233,'1',600,13),(1234,'1',600,24),(1235,'1B',600,18),(1236,'',600,22),(1237,'1',600,3),(1238,'3',601,1),(1239,'1B',601,18),(1240,'2',601,4),(1241,'3',601,22),(1242,'2',601,21),(1243,'1',603,9),(1244,'1B',603,18),(1245,'2',605,7),(1246,'4',605,2),(1247,'1B',605,18),(1248,'4',611,2),(1249,'2',611,20),(1250,'3',612,7),(1251,'2',612,20),(1252,'3',612,22),(1253,'1',614,11),(1254,'1',614,6),(1255,'1',616,1),(1256,'4',617,2),(1257,'1B',617,18),(1258,'1B',619,18),(1259,'3',619,22),(1260,'2',620,20),(1261,'1',623,24),(1262,'2',624,11),(1263,'1B',624,18),(1264,'4',626,2),(1265,'1B',626,18),(1266,'4',630,2),(1267,'2',630,20),(1268,'3',632,1),(1269,'1B',632,18),(1270,'2',635,20),(1271,'1',635,6),(1272,'3',635,22),(1273,'2',636,20),(1274,'3',636,22),(1275,'1',639,7),(1276,'2',639,1),(1277,'1B',639,18),(1278,'2',640,7),(1279,'2',640,24),(1280,'2',640,20),(1281,'3',640,22),(1282,'4',641,2),(1283,'1',641,6),(1284,'1B',642,18),(1285,'3',644,1),(1286,'3',647,1),(1287,'2',647,20),(1288,'1',647,6),(1289,'2',647,15),(1290,'1B',649,18),(1291,'3',649,22),(1292,'4',650,2),(1293,'2',650,20),(1294,'1',650,19),(1295,'2',651,11),(1296,'2',651,20),(1297,'3',651,22),(1298,'2',656,20),(1299,'3',656,22),(1300,'2',657,20),(1301,'3',657,22),(1302,'2',658,10),(1303,'1B',658,4),(1304,'2',658,15),(1305,'2',659,20),(1306,'2',662,20),(1307,'3',662,22),(1308,'2',663,20),(1309,'3',663,22),(1310,'2',664,20),(1311,'3',664,22),(1312,'2',665,7),(1313,'2',665,20),(1314,'3',665,22),(1315,'2',666,20),(1316,'3',666,22),(1317,'2',667,20),(1318,'3',667,22),(1319,'2',668,20),(1320,'3',668,22),(1321,'2',675,20),(1322,'3',675,22),(1323,'4',676,2),(1324,'2',676,20),(1325,'3',676,22),(1326,'4',680,2),(1327,'1B',680,18),(1328,'2',684,20),(1329,'3',684,22),(1330,'1',685,6),(1331,'2',686,20),(1332,'3',686,22),(1333,'2',687,20),(1334,'3',687,22),(1335,'1',688,7),(1336,'4',688,2),(1337,'2',688,20),(1338,'3',688,22),(1339,'2',689,20),(1340,'3',689,22),(1341,'4',690,2),(1342,'1B',690,18),(1343,'3',691,7),(1344,'1B',691,18),(1345,'3',691,22),(1346,'4',694,2),(1347,'1B',695,18),(1348,'3',695,22),(1349,'4',697,2),(1350,'2',697,20),(1351,'1',697,19),(1352,'4',699,2),(1353,'2',701,20),(1354,'3',701,22),(1355,'4',703,2),(1356,'2',703,20),(1357,'3',703,22),(1358,'4',706,2),(1359,'4',707,2),(1360,'2',708,20),(1361,'3',708,22),(1362,'2',709,7),(1363,'4',709,2),(1364,'2',709,20),(1365,'1',709,6),(1366,'3',709,22),(1367,'2',712,7),(1368,'4',712,2),(1369,'2',712,20),(1370,'1',712,6),(1371,'1',712,19),(1372,'2',712,4),(1373,'3',712,22),(1374,'2',718,1),(1375,'1B',718,18),(1376,'4',720,2),(1377,'4',723,2),(1378,'2',723,20),(1379,'1',723,19),(1380,'3',723,22),(1381,'2',725,20),(1382,'3',725,22),(1383,'4',728,2),(1384,'2',728,15),(1385,'2',729,20),(1386,'3',729,22),(1387,'2',730,20),(1388,'3',730,22),(1389,'4',731,2),(1390,'2',731,20),(1391,'3',731,22),(1392,'2',732,20),(1393,'2',736,20),(1394,'3',736,22),(1395,'1',742,7),(1396,'3',742,1),(1397,'2',742,20),(1398,'1',742,6),(1399,'3',742,22),(1400,'3',746,1),(1401,'1B',746,18),(1402,'1',748,9),(1403,'1B',748,18),(1404,'3',748,22),(1405,'2',749,1),(1406,'2',750,1),(1407,'1B',751,4),(1408,'3',751,1),(1409,'2',751,20),(1410,'3',751,22),(1411,'2',753,20),(1412,'3',753,22),(1413,'3',755,7),(1414,'1B',757,18),(1415,'1',757,16),(1416,'2',758,20),(1417,'3',758,22),(1418,'1B',759,18),(1419,'3',759,22),(1420,'4',760,2),(1421,'2',760,20),(1422,'3',760,22),(1423,'2',765,20),(1424,'3',765,22),(1425,'4',766,2),(1426,'2',767,20),(1427,'3',767,22),(1428,'4',768,2),(1429,'2',769,20),(1430,'4',771,2),(1431,'2',771,20),(1432,'3',771,22),(1433,'1B',772,18),(1434,'2',773,20),(1435,'3',773,22),(1436,'2',775,7),(1437,'3',775,1),(1438,'1',775,21),(1439,'4',776,2),(1440,'2',776,20),(1441,'3',776,22),(1442,'4',777,2),(1443,'',778,20),(1444,'2',779,20),(1445,'3',779,22),(1446,'2',780,20),(1447,'3',780,22),(1448,'4',781,2),(1449,'2',781,1),(1450,'1B',781,18),(1451,'4',782,2),(1452,'2',783,20),(1453,'3',783,22),(1454,'2',784,20),(1455,'3',784,22),(1456,'1B',785,18),(1457,'1',786,7),(1458,'1',786,17),(1459,'1B',786,18),(1460,'4',787,2),(1461,'2',787,10),(1462,'1B',788,18),(1463,'4',790,2),(1464,'2',790,20),(1465,'1',790,6),(1466,'3',790,22),(1467,'4',791,2),(1468,'2',792,7),(1469,'1',792,19),(1470,'4',793,2),(1471,'2',793,20),(1472,'1',793,6),(1473,'2',793,21),(1474,'1',794,7),(1475,'4',794,2),(1476,'2',795,20),(1477,'3',795,22),(1478,'4',796,2),(1479,'2',796,20),(1480,'3',796,22),(1481,'3',797,1),(1482,'1',797,19),(1483,'1B',797,4),(1484,'3',799,1),(1485,'4',799,2),(1486,'1B',799,18),(1487,'1',799,19),(1488,'2',800,20),(1489,'3',800,22),(1490,'4',801,2),(1491,'1B',801,18),(1492,'1',801,19),(1493,'2',804,20),(1494,'3',804,22),(1495,'2',805,20),(1496,'3',805,22),(1497,'3',806,1),(1498,'2',806,20),(1499,'2',806,21),(1500,'1B',807,4),(1501,'3',807,1),(1502,'1',807,19),(1503,'4',811,2),(1504,'2',811,20),(1505,'1',811,6),(1506,'4',815,2),(1507,'2',815,20),(1508,'3',815,22),(1509,'4',824,2),(1510,'4',828,2),(1511,'2',828,20),(1512,'3',828,22),(1513,'4',835,2),(1514,'2',835,20),(1515,'2',840,20),(1516,'3',840,22),(1517,'2',843,20),(1518,'3',843,22),(1519,'2',847,20),(1520,'3',847,22),(1521,'2',848,20),(1522,'3',848,22),(1523,'4',853,2),(1524,'1B',853,18),(1525,'4',859,2),(1526,'2',859,20),(1527,'3',859,22),(1528,'4',860,2),(1529,'1B',860,18),(1530,'4',861,2),(1531,'2',862,20),(1532,'3',862,22),(1533,'2',866,20),(1534,'3',866,22),(1535,'1B',867,18),(1536,'4',869,2),(1537,'2',869,20),(1538,'3',869,22),(1539,'2',871,20),(1540,'3',871,22),(1541,'2',872,20),(1542,'3',872,22),(1543,'2',873,20),(1544,'3',873,22),(1545,'2',875,20),(1546,'3',875,22),(1547,'2',877,20),(1548,'3',877,22),(1549,'2',881,20),(1550,'3',881,22),(1551,'4',888,2),(1552,'2',888,20),(1553,'1',888,19),(1554,'2',889,20),(1555,'4',894,2),(1556,'2',894,20),(1557,'3',894,22),(1558,'1B',896,18),(1559,'2',903,20),(1560,'2',904,20),(1561,'2',905,20),(1562,'3',905,22),(1563,'2',910,20),(1564,'3',910,22),(1565,'2',911,20),(1566,'3',911,22),(1567,'4',912,2),(1568,'2',912,20),(1569,'3',912,22),(1570,'2',913,20),(1571,'3',913,22),(1572,'2',914,20),(1573,'3',914,22),(1574,'2',915,20),(1575,'3',915,22),(1576,'3',916,7),(1577,'2',918,7),(1578,'3',918,1),(1579,'1B',918,18),(1580,'1',918,21),(1581,'3',918,22),(1582,'2',920,1),(1583,'1B',920,18),(1584,'1',920,21),(1585,'2',921,7),(1586,'4',921,2),(1587,'3',921,1),(1588,'1A',921,18),(1589,'3',921,22),(1590,'1B',922,18),(1591,'2',923,20),(1592,'3',923,22),(1593,'2',924,20),(1594,'3',924,22),(1595,'2',925,7),(1596,'1B',925,18),(1597,'2',925,4),(1598,'3',925,22),(1599,'2',926,20),(1600,'3',926,22),(1601,'3',927,7),(1602,'4',927,2),(1603,'1B',927,18),(1604,'2',928,7),(1605,'1B',928,18),(1606,'3',929,7),(1607,'2',929,20),(1608,'3',929,22),(1609,'1',931,24),(1610,'4',935,2),(1611,'2',935,20),(1612,'1',935,16),(1613,'1',935,19),(1614,'2',935,10),(1615,'1A',935,4),(1616,'1B',935,15),(1617,'1',935,21),(1618,'4',936,2),(1619,'1',936,16),(1620,'1',936,19),(1621,'2',936,10),(1622,'1B',936,4),(1623,'1B',936,15),(1624,'2',938,7),(1625,'4',938,2),(1626,'1A',938,18),(1627,'2',942,7),(1628,'2',943,7),(1629,'2',943,1),(1630,'1',944,1),(1631,'2',944,21),(1632,'3',946,7),(1633,'4',946,2),(1634,'3',946,1),(1635,'1B',946,18),(1636,'3',947,7),(1637,'4',947,2),(1638,'3',947,1),(1639,'1A',947,18),(1640,'3',951,11),(1641,'1',951,9),(1642,'1A',951,18),(1643,'1B',952,18),(1644,'3',952,22),(1645,'1',953,9),(1646,'1B',953,18),(1647,'2',954,1),(1648,'1A',954,18),(1649,'1A',955,18),(1650,'1',956,11),(1651,'1',956,9),(1652,'4',956,2),(1653,'1A',956,18),(1654,'2',956,21),(1655,'1B',959,18),(1656,'3',959,22),(1657,'2',963,20),(1658,'3',963,22),(1659,'4',964,2),(1660,'2',966,7),(1661,'1',966,13),(1662,'2',966,24),(1663,'1B',966,18),(1664,'2',966,15),(1665,'3',966,22),(1666,'2',966,21),(1667,'1',966,3),(1668,'2',967,20),(1669,'3',967,22),(1670,'4',968,2),(1671,'2',968,20),(1672,'3',968,22),(1673,'4',969,2),(1674,'2',969,20),(1675,'1',969,6),(1676,'3',969,22),(1677,'1B',972,18),(1678,'3',973,11),(1679,'4',973,2),(1680,'2',973,20),(1681,'3',973,22),(1682,'2',979,7),(1683,'3',979,22),(1684,'2',980,7),(1685,'2',980,20),(1686,'4',984,2),(1687,'2',984,20),(1688,'2',985,20),(1689,'1',985,6),(1690,'3',985,22),(1691,'3',988,1),(1692,'1',988,21),(1693,'1A',988,18),(1694,'3',989,1),(1695,'2',990,20),(1696,'3',990,22),(1697,'2',992,7),(1698,'2',992,20),(1699,'2',992,4),(1700,'3',992,22),(1701,'2',992,21),(1702,'2',995,7),(1703,'1',995,6),(1704,'3',995,22),(1705,'3',996,7),(1706,'4',996,2),(1707,'2',996,20),(1708,'1',996,6),(1709,'3',996,22),(1710,'2',997,7),(1711,'2',997,20),(1712,'3',997,22),(1713,'2',998,7),(1714,'2',998,20),(1715,'',998,22),(1716,'4',999,2),(1717,'2',999,20),(1718,'3',999,22),(1719,'2',1001,20),(1720,'2',1003,20),(1721,'3',1003,22),(1722,'2',1004,20),(1723,'3',1004,22),(1724,'3',1005,7),(1725,'4',1005,2),(1726,'1',1005,6),(1727,'2',1006,20),(1728,'3',1006,22),(1729,'2',1007,20),(1730,'3',1007,22),(1731,'2',1009,20),(1732,'3',1009,22),(1733,'4',1014,2),(1734,'2',1015,20),(1735,'3',1015,22),(1736,'4',1018,2),(1737,'2',1018,20),(1738,'1',1018,6),(1739,'3',1018,22),(1740,'4',1021,2),(1741,'2',1022,20),(1742,'3',1022,22),(1743,'2',1023,20),(1744,'3',1023,22),(1745,'2',1024,7),(1746,'4',1024,2),(1747,'3',1024,1),(1748,'1',1024,6),(1749,'3',1024,22),(1750,'4',1025,2),(1751,'2',1025,20),(1752,'3',1025,22),(1753,'2',1026,7),(1754,'4',1026,2),(1755,'2',1026,20),(1756,'3',1026,22),(1757,'2',1027,7),(1758,'4',1027,2),(1759,'3',1027,1),(1760,'2',1027,20),(1761,'1B',1027,4),(1762,'3',1027,22),(1763,'3',1028,7),(1764,'1B',1028,18),(1765,'1B',1029,18),(1766,'2',1030,7),(1767,'4',1030,2),(1768,'1B',1030,18),(1769,'4',1031,2),(1770,'2',1031,20),(1771,'1',1033,6),(1772,'4',1037,2),(1773,'1',1037,6),(1774,'2',1038,20),(1775,'3',1038,22),(1776,'3',1042,7),(1777,'2',1042,20),(1778,'3',1042,22),(1779,'1B',1044,4),(1780,'1',1046,9),(1781,'4',1046,2),(1782,'2',1046,20),(1783,'1',1046,6),(1784,'4',1048,2),(1785,'2',1049,1),(1786,'2',1049,20),(1787,'1',1049,6),(1788,'1',1049,19),(1789,'',1049,21),(1790,'1B',1051,15),(1791,'4',1055,2),(1792,'2',1055,21),(1793,'4',1060,2),(1794,'1B',1060,18),(1795,'1B',1060,15),(1796,'2',1062,20),(1797,'3',1066,7),(1798,'1',1066,1),(1799,'2',1066,20),(1800,'2',1066,15),(1801,'1',1066,21),(1802,'3',1066,22),(1803,'1A',1067,18),(1804,'2',1069,20),(1805,'4',1070,2),(1806,'1',1070,6),(1807,'3',1072,7),(1808,'2',1072,20),(1809,'2',1074,7),(1810,'1',1074,9),(1811,'2',1074,20),(1812,'3',1074,22),(1813,'2',1076,7),(1814,'4',1076,2),(1815,'2',1076,20),(1816,'3',1077,7),(1817,'4',1077,2),(1818,'2',1077,20),(1819,'1B',1077,15),(1820,'2',1078,7),(1821,'2',1078,20),(1822,'1B',1078,10),(1823,'1A',1078,4),(1824,'1',1078,21),(1825,'1',1078,3),(1826,'4',1080,2),(1827,'1A',1080,18),(1828,'2',1081,7),(1829,'2',1081,20),(1830,'3',1081,22),(1831,'3',1083,1),(1832,'4',1083,2),(1833,'2',1083,20),(1834,'1',1083,16),(1835,'1',1083,19),(1836,'2',1083,4),(1837,'2',1083,21),(1838,'3',1083,22),(1839,'4',1086,2),(1840,'3',1086,1),(1841,'2',1086,20),(1842,'2',1086,4),(1843,'2',1086,15),(1844,'1',1086,21),(1845,'3',1087,1),(1846,'2',1087,4),(1847,'1B',1087,15),(1848,'1',1087,21),(1849,'4',1088,2),(1850,'1B',1088,18),(1851,'1B',1089,4),(1852,'1B',1089,10),(1853,'4',1090,2),(1854,'1B',1090,15),(1855,'3',1091,7),(1856,'4',1091,2),(1857,'1B',1091,18),(1858,'3',1092,7),(1859,'1A',1092,18),(1860,'3',1093,7),(1861,'1A',1093,18),(1862,'3',1094,11),(1863,'1A',1094,18),(1864,'1',1095,7),(1865,'3',1096,7),(1866,'1A',1096,18),(1867,'3',1097,7),(1868,'4',1097,2),(1869,'3',1097,1),(1870,'2',1097,4),(1871,'1B',1098,18),(1872,'4',1100,2),(1873,'1A',1100,18),(1874,'3',1100,22),(1875,'1B',1101,18),(1876,'3',1101,22),(1877,'2',1102,7),(1878,'2',1103,7),(1879,'3',1103,1),(1880,'1',1103,21),(1881,'4',1104,2),(1882,'1A',1105,18),(1883,'2',1106,7),(1884,'2',1106,20),(1885,'2',1106,4),(1886,'3',1106,22),(1887,'1',1107,6),(1888,'2',1108,20),(1889,'3',1108,22),(1890,'2',1110,20),(1891,'3',1110,22),(1892,'4',1112,2),(1893,'1A',1112,18),(1894,'2',1114,1),(1895,'1A',1114,18),(1896,'2',1114,4),(1897,'3',1114,22),(1898,'2',1114,21),(1899,'4',1115,2),(1900,'1B',1115,18),(1901,'1',1115,16),(1902,'1',1115,19),(1903,'2',1116,20),(1904,'1',1116,6),(1905,'3',1116,22),(1906,'2',1117,20),(1907,'2',1118,20),(1908,'1',1118,6),(1909,'3',1118,22),(1910,'2',1119,20),(1911,'4',1119,2),(1912,'2',1120,20),(1913,'3',1120,22),(1914,'3',1121,7),(1915,'2',1121,20),(1916,'3',1121,22),(1917,'4',1122,2),(1918,'2',1122,1),(1919,'1B',1122,18),(1920,'1',1122,19),(1921,'3',1122,22),(1922,'2',1123,7),(1923,'4',1123,2),(1924,'2',1123,20),(1925,'3',1123,22),(1926,'2',1125,20),(1927,'3',1125,22),(1928,'1B',1126,18),(1929,'4',1127,2),(1930,'4',1128,2),(1931,'1',1128,19),(1932,'2',1128,15),(1933,'2',1128,21),(1934,'2',1129,20),(1935,'1',1129,16),(1936,'1',1129,19),(1937,'1B',1131,18),(1938,'3',1132,1),(1939,'2',1132,4),(1940,'1B',1132,15),(1941,'1',1132,21),(1942,'3',1133,7),(1943,'4',1133,2),(1944,'2',1133,20),(1945,'3',1133,22),(1946,'1',1133,3),(1947,'2',1135,21),(1948,'1',1136,1),(1949,'1B',1137,4),(1950,'1B',1137,10),(1951,'4',1139,2),(1952,'2',1139,20),(1953,'3',1139,22),(1954,'4',1140,2),(1955,'3',1140,22),(1956,'4',1142,2),(1957,'2',1142,21),(1958,'1B',1144,4),(1959,'2',1144,15),(1960,'2',1149,7),(1961,'2',1149,20),(1962,'3',1149,22),(1963,'2',1151,7),(1964,'3',1151,1),(1965,'1',1151,21),(1966,'2',1152,7),(1967,'4',1152,2),(1968,'2',1152,20),(1969,'2',1153,7),(1970,'1',1153,3),(1971,'2',1153,20),(1972,'3',1153,22),(1973,'2',1153,15),(1974,'2',1153,21),(1975,'1',1154,13),(1976,'1B',1154,18),(1977,'1',1155,7),(1978,'4',1161,2),(1979,'1',1161,6),(1980,'2',1162,20),(1981,'3',1162,22),(1982,'2',1164,4),(1983,'2',1165,7),(1984,'2',1165,20),(1985,'3',1165,22),(1986,'1',1166,7),(1987,'4',1166,2),(1988,'3',1166,22),(1989,'2',1167,7),(1990,'2',1167,20),(1991,'2',1167,15),(1992,'2',1167,21),(1993,'1',1167,3),(1994,'4',1168,2),(1995,'2',1168,20),(1996,'2',1168,4),(1997,'2',1168,21),(1998,'2',1169,7),(1999,'1',1169,3),(2000,'2',1169,20),(2001,'3',1169,22),(2002,'2',1170,7),(2003,'1',1170,3),(2004,'2',1170,20),(2005,'3',1170,22),(2006,'2',1170,15),(2007,'2',1170,21),(2008,'2',1171,7),(2009,'2',1171,4),(2010,'2',1171,20),(2011,'3',1171,22),(2012,'3',1172,7),(2013,'4',1172,2),(2014,'2',1172,20),(2015,'1B',1172,15),(2016,'2',1173,7),(2017,'2',1173,20),(2018,'3',1173,22),(2019,'2',1175,7),(2020,'2',1175,20),(2021,'3',1175,22),(2022,'2',1176,7),(2023,'4',1179,2),(2024,'2',1179,20),(2025,'3',1179,22),(2026,'2',1180,7),(2027,'2',1180,20),(2028,'3',1180,22),(2029,'3',1181,1),(2030,'1B',1181,18),(2031,'2',1182,20),(2032,'3',1182,22),(2033,'4',1270,2),(2034,'1',1270,6),(2035,'4',1286,2),(2036,'4',1316,2),(2037,'1A',1316,18),(2038,'3',1316,22),(2039,'2',1322,7),(2040,'2',1322,20),(2041,'2',1322,4),(2042,'2',1369,7),(2043,'1',1369,3),(2044,'2',1369,20),(2045,'3',1369,22),(2046,'2',1369,15),(2047,'2',1369,21),(2048,'2',1374,7),(2049,'4',1374,2),(2050,'3',1374,1),(2051,'1A',1374,18),(2052,'3',1374,22),(2053,'2',1418,20),(2054,'1',1418,6),(2055,'1',1418,16),(2056,'1',1418,19),(2057,'2',1418,10),(2058,'2',1418,15),(2059,'3',1418,22),(2060,'2',1419,7),(2061,'1',1419,3),(2062,'2',1419,20),(2063,'3',1419,22),(2064,'2',1419,15),(2065,'2',1419,21);
/*!40000 ALTER TABLE `chembase_cmpd_class` ENABLE KEYS */;
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