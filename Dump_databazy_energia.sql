CREATE DATABASE  IF NOT EXISTS `energia` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `energia`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: energia
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dieta`
--

DROP TABLE IF EXISTS `dieta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dieta` (
  `id_dieta` int NOT NULL AUTO_INCREMENT,
  `nazov_diety` varchar(255) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_dieta`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dieta`
--

LOCK TABLES `dieta` WRITE;
/*!40000 ALTER TABLE `dieta` DISABLE KEYS */;
INSERT INTO `dieta` VALUES (1,'Dieta I','2023-08-14 18:52:23'),(2,'Dieta II','2023-08-14 18:54:07');
/*!40000 ALTER TABLE `dieta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kategoria_jedla`
--

DROP TABLE IF EXISTS `kategoria_jedla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategoria_jedla` (
  `id_kategoria_jedla` int NOT NULL AUTO_INCREMENT,
  `nazov_kategorie` varchar(255) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_kategoria_jedla`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategoria_jedla`
--

LOCK TABLES `kategoria_jedla` WRITE;
/*!40000 ALTER TABLE `kategoria_jedla` DISABLE KEYS */;
INSERT INTO `kategoria_jedla` VALUES (1,'Ovocie','2023-08-08 15:40:19'),(2,'Strukoviny','2023-08-08 15:40:33'),(3,'Zelenina','2023-08-08 15:40:48'),(4,'Mäso','2023-08-08 15:41:07'),(5,'Mlieko a mliečne výrobky','2023-08-08 15:41:25'),(6,'Chlieb a obilné výrobky','2023-08-08 16:50:49'),(7,'Alko a nealko nápoje','2023-08-08 16:51:25'),(8,'Orechy','2023-08-08 16:51:39'),(9,'Oleje a tuky','2023-08-08 16:51:55'),(10,'Iné','2023-08-08 16:52:04');
/*!40000 ALTER TABLE `kategoria_jedla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `potraviny`
--

DROP TABLE IF EXISTS `potraviny`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `potraviny` (
  `id_potravina` int NOT NULL AUTO_INCREMENT,
  `id_kategoria_jedla` int DEFAULT NULL,
  `nazov` varchar(255) DEFAULT NULL,
  `sacharidy` varchar(5) DEFAULT NULL,
  `tuky` varchar(5) DEFAULT NULL,
  `bielkoviny` varchar(5) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_potravina`)
) ENGINE=MyISAM AUTO_INCREMENT=332 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `potraviny`
--

LOCK TABLES `potraviny` WRITE;
/*!40000 ALTER TABLE `potraviny` DISABLE KEYS */;
INSERT INTO `potraviny` VALUES (2,1,'Egreš','10.6','0.5','0.9','2023-08-08 13:49:50'),(3,1,'Arónia','17','0.7','1.7','2023-08-08 13:49:50'),(4,1,'Avokádo','1.9','19.5','1.9','2023-08-08 13:49:50'),(5,1,'Banán','23','0.3','0.3','2023-08-08 13:49:50'),(6,1,'Čučoriedky','14.7','0.7','0.8','2023-08-08 13:49:50'),(7,1,'Broskyne','12.5','0.2','0.8','2023-08-08 13:49:50'),(8,1,'Brusnice','13.7','0.8','0.4','2023-08-08 13:49:50'),(9,1,'Čerešne','14.7','0.5','0.9','2023-08-08 13:49:50'),(10,1,'Citróny','10.5','0.5','0.7','2023-08-08 13:49:50'),(11,1,'Datle','31.3','0.1','1.5','2023-08-08 13:49:50'),(12,1,'Drienky','14','0.2','0.8','2023-08-08 13:49:50'),(13,1,'Fígy','9.5','0.3','1.3','2023-08-08 13:49:50'),(14,1,'Granátové jablko','11.8','0.2','1.3','2023-08-08 13:49:50'),(15,1,'Grapefruit','9.6','0.3','0.5','2023-08-08 13:49:50'),(16,1,'Grenadila','7.5','0.3','2.8','2023-08-08 13:49:50'),(17,1,'Hrozno','18.2','0.5','0.7','2023-08-08 13:49:50'),(18,1,'Hruška','15.8','0.4','0.5','2023-08-08 13:49:50'),(19,1,'Jablko','14.4','0.4','0.4','2023-08-08 13:49:50'),(20,1,'Jahody','8.8','0.6','0.9','2023-08-08 13:49:50'),(21,1,'Jarabiny','22.6','0.3','1','2023-08-08 13:49:50'),(22,1,'Dula','12.4','0.4','0.4','2023-08-08 13:49:50'),(23,1,'Kiwi','9.1','0.5','1','2023-08-08 13:49:50'),(24,1,'Klementinky','8.7','0.1','0.9','2023-08-08 13:49:50'),(25,1,'Liči','16','0.5','0.9','2023-08-08 13:49:50'),(26,1,'Limetky','10.6','0','0.4','2023-08-08 13:49:50'),(27,1,'Maliny','11.6','0','1','2023-08-08 13:49:50'),(28,1,'Mandarinky','10.6','0.3','0.9','2023-08-08 13:49:50'),(29,1,'Mango','16','0.3','0.6','2023-08-08 13:49:50'),(30,1,'Maracuja','9','0','0.6','2023-08-08 13:49:50'),(31,1,'Melón','6.5','0.1','0.5','2023-08-08 13:49:50'),(32,1,'Melón vodný','5','0.3','0.6','2023-08-08 13:49:50'),(33,1,'Marhule','13.4','0.3','1','2023-08-08 13:49:50'),(34,1,'Mirabelky','12.8','0.2','0.7','2023-08-08 13:49:50'),(35,1,'Moruše','8.1','0','1.3','2023-08-08 13:49:50'),(36,1,'Nektarinky','8','0.1','1.2','2023-08-08 13:49:51'),(38,1,'Papája','9','0.1','0.5','2023-08-08 13:49:51'),(39,1,'Pomaranč','11.7','0.3','0.9','2023-08-08 13:49:51'),(40,1,'Rakytník','5','3.9','1.2','2023-08-08 13:49:51'),(41,1,'Rýbezle biele','5.6','0.3','1.3','2023-08-08 13:49:51'),(42,1,'Rýbezle červené','13.8','0.3','1.1','2023-08-08 13:49:51'),(43,1,'Rýbezle čierne','16.4','0.3','1.3','2023-08-08 13:49:51'),(44,1,'Ryngle','16.6','0.2','0.8','2023-08-08 13:49:51'),(45,1,'Šípky','22','0.4','3.6','2023-08-08 13:49:51'),(46,1,'Slivky','16.2','0.3','0.8','2023-08-08 13:49:51'),(47,1,'Višne','12.6','4.4','0.8','2023-08-08 13:49:51'),(50,4,'Baranie stehno','0','11','12.9','2023-08-08 13:50:30'),(51,4,'Bažant','0.2','14.8','19.8','2023-08-08 13:50:30'),(52,4,'Bravčové stehno','0','7','21','2023-08-08 13:50:30'),(53,4,'Bravčový bôčik','0','50.4','8.2','2023-08-08 13:50:30'),(54,5,'Bryndza polotučná','19','8.7','20','2023-08-08 13:50:30'),(55,5,'Bryndza tučná','1.7','17.6','19.8','2023-08-08 13:50:30'),(56,6,'Celozrnný chlieb','51.7','1.6','11.6','2023-08-08 13:50:30'),(57,6,'Celozrnný chlieb podpoliansky','76','1','11.5','2023-08-08 13:50:30'),(58,5,'Cottage Cheese (čerstvý syr) - Rajo','3','4','13','2023-08-08 13:50:30'),(59,5,'Eidam','1.8','14.6','29.2','2023-08-08 13:50:30'),(60,5,'Ementál','2.1','25.6','25.8','2023-08-08 13:50:30'),(61,5,'Encián (Hermelín)','1.6','20.2','20.2','2023-08-08 13:50:30'),(62,2,'Fazuľa','61.6','1.6','21.4','2023-08-08 13:50:30'),(63,4,'Filé z tresky','0','0.4','16.5','2023-08-08 13:50:30'),(64,1,'Granola','59','18.3','10.1','2023-08-08 13:50:30'),(65,4,'Holubie mäso','0','0','22.1','2023-08-08 13:50:30'),(66,4,'Hovädzie predné','0','9.8','20.7','2023-08-08 13:50:30'),(67,4,'Hovädzie zadné','0','6.5','20.8','2023-08-08 13:50:30'),(68,2,'Hrach','60.2','1.4','23.8','2023-08-08 13:50:30'),(69,6,'Chlieb grahamový','51.7','1.6','11.6','2023-08-08 13:50:30'),(70,6,'Chlieb pšeničný biely','56.7','1','8','2023-08-08 13:50:30'),(71,4,'Jahňacina','0','13.6','12.9','2023-08-08 13:50:30'),(72,5,'Jogurt biely','9.7','4.5','5.7','2023-08-08 13:50:30'),(73,5,'Jogurt ovocný','18.7','3.8','4.8','2023-08-08 13:50:30'),(74,4,'Kačka ; hus','0','17','12','2023-08-08 13:50:30'),(76,5,'Kefír','1.7','3.6','3.3','2023-08-08 13:50:30'),(77,4,'Králik domáci','0','5.5','14.8','2023-08-08 13:50:30'),(78,6,'Krupica','75.6','0.7','9.7','2023-08-08 13:50:30'),(79,4,'Kura - broiler','0','4.1','15','2023-08-08 13:50:30'),(80,5,'Kyslá smotana 12% tuku','4.2','12','3.2','2023-08-08 13:50:30'),(81,4,'Ladvinky bravčové','0.8','4.4','15.5','2023-08-08 13:50:30'),(82,4,'Ladvinky hovädzie','0.8','7.3','13.5','2023-08-08 13:50:30'),(83,4,'Makrela (bez vnútorností)','0','7.3','11.4','2023-08-08 13:50:30'),(84,4,'Makrela (pečená)','3.5','14','16','2023-08-08 13:50:30'),(85,4,'Makrela - udenáč','0','10','14','2023-08-08 13:50:31'),(86,5,'Mlieko nízkotučné','4.6','0.5','3.2','2023-08-08 13:50:31'),(88,4,'Morka','0.2','15','15','2023-08-08 13:50:31'),(89,4,'Mozoček','0.8','8.2','10.1','2023-08-08 13:50:31'),(90,5,'Niva','0.8','25.7','19.2','2023-08-08 13:50:31'),(91,5,'Olomoucké syrečky','2','0.8','30','2023-08-08 13:50:31'),(92,4,'Ostatné teľacie s kosťami','0.3','4.8','14.4','2023-08-08 13:50:31'),(93,6,'Ovsené vločky','68','3.6','16.3','2023-08-08 13:50:31'),(94,4,'Pečeň bravčová','2','4.5','19','2023-08-08 13:50:31'),(95,4,'Pečeň hovädzia','3.3','4.1','19','2023-08-08 13:50:31'),(96,3,'Pečené zemiaky','50','0.5','2.5','2023-08-08 13:50:31'),(97,10,'Piškóty detské OPAVIA','77.8','1.1','8.3','2023-08-08 13:50:31'),(98,4,'Prepelica','0','0','24.3','2023-08-08 13:50:31'),(100,5,'Romadur','2.4','17.2','18.1','2023-08-08 13:50:31'),(101,10,'Ryža','79','0.6','7.6','2023-08-08 13:50:31'),(102,4,'Sardinky v oleji (vo vlastnej šťave)','0','27','21.1','2023-08-08 13:50:31'),(103,4,'Sardinky v tomate','2.4','15','15','2023-08-08 13:50:31'),(104,4,'Sleď - udenáč','0','12.9','22.2','2023-08-08 13:50:31'),(105,4,'Sleď - zavináč','0','14.8','19.8','2023-08-08 13:50:31'),(106,4,'Slezina','1','4','16.9','2023-08-08 13:50:31'),(107,4,'Sliepka','0.2','16','11.5','2023-08-08 13:50:31'),(108,2,'Soja','30.9','2','49.6','2023-08-08 13:50:31'),(109,4,'Srdce bravčové','0.4','4.6','16.4','2023-08-08 13:50:31'),(110,4,'Srdce hovädzie','0.6','3.5','16','2023-08-08 13:50:31'),(111,4,'Srnec','0.3','1.2','13.5','2023-08-08 13:50:31'),(112,5,'Sušené plnotučné mlieko','38','25','25','2023-08-08 13:50:31'),(113,5,'Syr - Žervé','1.8','15','12.4','2023-08-08 13:50:31'),(114,5,'Syr tavený 30% tuku v sušine (t.v.s.)','0.8','11.4','19.6','2023-08-08 13:50:31'),(115,5,'Syr zlato','2.5','13.8','25.7','2023-08-08 13:50:31'),(116,5,'Šľahačka 33% tuku','2.7','33','2.4','2023-08-08 13:50:31'),(117,2,'Šošovica','59.5','1','25','2023-08-08 13:50:31'),(118,10,'Špagety','77','1','11','2023-08-08 13:50:31'),(119,4,'Šťuka','0','0','18.8','2023-08-08 13:50:31'),(120,5,'Tavený ementál 35% tuku v sušine (t.v.s.)','1.2','23.4','21.2','2023-08-08 13:50:32'),(121,5,'Tavený smotanový syr 45% tuku v sušine (t.v.s.)','1.2','18','15.9','2023-08-08 13:50:32'),(122,4,'Teľacie stehno','0.5','3','21.8','2023-08-08 13:50:32'),(123,10,'Tofu','10.5','5.2','14.4','2023-08-08 13:50:32'),(124,5,'Tvaroh Danone jemný','2.4','0.6','14','2023-08-08 13:50:32'),(125,5,'Tvaroh mäkký (netučný)','4.8','0.3','19.4','2023-08-08 13:50:32'),(126,5,'Tvaroh Rajo nízkotučný','4.2','2.5','17.5','2023-08-08 13:50:32'),(127,4,'Úhor','0','0','18.6','2023-08-08 13:50:32'),(128,4,'Vnútornosti priemer (ostatné)','1','7.9','16.3','2023-08-08 13:50:32'),(129,5,'Zahustené mlieko nesladené (v plechovke)','12','9','8.3','2023-08-08 13:50:32'),(130,5,'Zahustené mlieko sladené (v plechovke)','53.3','9.5','10','2023-08-08 13:50:32'),(131,4,'Zajac','0.2','0.8','16.8','2023-08-08 13:50:32'),(132,3,'Rajčiny','4','0.23','0.9','2023-08-08 13:50:32'),(134,4,'Bravčové mäso','0','25','17','2023-08-08 13:50:59'),(135,4,'Cigánska pečienka','0','22','19','2023-08-08 13:50:59'),(136,4,'Hovädzie mäso','0','12','25','2023-08-08 13:50:59'),(137,4,'Husacie mäso','0','32.5','15','2023-08-08 13:50:59'),(138,4,'Kačacie prsia','0.17','10.4','18.2','2023-08-08 13:50:59'),(139,4,'Klobáska','0.1','23','12','2023-08-08 13:50:59'),(140,4,'Králik','0.2','6','12','2023-08-08 13:50:59'),(141,4,'Kuracia šunka','10.3','0.7','13','2023-08-08 13:50:59'),(142,4,'Kuracie kridielka','0','14.1','18.8','2023-08-08 13:50:59'),(143,4,'Kuracie prsia','0','6','27','2023-08-08 13:50:59'),(144,4,'Kuracie stehno','0','3.8','20','2023-08-08 13:50:59'),(145,4,'Morčacie mäso','0.2','4.7','21.9','2023-08-08 13:50:59'),(146,4,'Telacie mäso','0','12','14','2023-08-08 13:51:00'),(147,4,'Hejk','0','3','17','2023-08-08 13:51:00'),(148,4,'Kalamár','3.1','1.5','11','2023-08-08 13:51:00'),(149,4,'Kapor','0.1','6.1','15','2023-08-08 13:51:00'),(150,4,'Krabie tyčinky','14.5','0.9','6.5','2023-08-08 13:51:00'),(151,4,'Krevety','0.1','0.8','16.5','2023-08-08 13:51:00'),(152,4,'Losos','0.1','8','19','2023-08-08 13:51:00'),(153,4,'Makrela údená','0','18','23','2023-08-08 13:51:00'),(154,4,'Pangasius','0','0','16','2023-08-08 13:51:00'),(155,4,'Pstruh','0.1','3','18','2023-08-08 13:51:00'),(156,4,'Sumec','0','11.3','15.3','2023-08-08 13:51:00'),(157,4,'Surimi','14.6','2.1','7.9','2023-08-08 13:51:00'),(158,4,'Sushi','25.3','2.2','6.7','2023-08-08 13:51:00'),(159,4,'Tuniak','0','8','22','2023-08-08 13:51:00'),(160,4,'Ústrice','4.8','1.2','9','2023-08-08 13:51:00'),(161,4,'Žralok','0','4.5','21','2023-08-08 13:51:00'),(163,6,'Croisant','30','20','6','2023-08-08 13:51:00'),(164,6,'Graham rohlík','58','2.3','9.6','2023-08-08 13:51:00'),(165,6,'Kaiserka','65','2','12','2023-08-08 13:51:00'),(166,6,'Rohlík','51','1','8','2023-08-08 13:51:00'),(168,6,'Tortila','56','7','8','2023-08-08 13:51:00'),(169,6,'Toustový chlieb','43','4.9','9.9','2023-08-08 13:51:00'),(171,6,'Žemla','57','3.7','9.7','2023-08-08 13:51:00'),(172,3,'Brokolica','2.9','0.9','4.4','2023-08-08 13:51:00'),(173,3,'Cibuľa','5.8','0.2','2','2023-08-08 13:51:00'),(176,3,'Kapusta','6.7','0.5','3.1','2023-08-08 13:51:01'),(178,3,'Ľadový šalát','1.9','0.3','0.7','2023-08-08 13:51:01'),(180,3,'Paprika','3.9','0.4','0.9','2023-08-08 13:51:01'),(181,3,'Paradajka','4.6','0.3','1.1','2023-08-08 13:51:01'),(182,3,'Reďkovka','5','0.1','1.5','2023-08-08 13:51:01'),(183,3,'Šalátová uhorka','2.6','0.2','0.7','2023-08-08 13:51:01'),(184,3,'Špenát','4.1','0.6','3.4','2023-08-08 13:51:01'),(185,3,'Šampiňóny','4.8','0.6','3.3','2023-08-08 13:51:01'),(186,5,'Mlieko','4.6','1.5','3.2','2023-08-08 13:51:01'),(187,5,'Mlieko polotučné','4.7','1.5','3.2','2023-08-08 13:51:01'),(188,5,'Mozzarella','0.4','18.5','19','2023-08-08 13:51:01'),(189,5,'Sojové Mlieko','1.5','2','4','2023-08-08 13:51:01'),(190,10,'Müsli','53.5','14.6','14.7','2023-08-08 13:51:01'),(191,7,'Becherovka','32','0','0','2023-08-08 13:51:01'),(192,7,'Biele vino','0.1','0','0.1','2023-08-08 13:51:01'),(193,7,'Coca cola','10.6','0','0','2023-08-08 13:51:01'),(194,7,'Káva','15','1','3','2023-08-08 13:51:01'),(195,7,'Kofola','20','0.1','0','2023-08-08 13:51:01'),(196,7,'Pepsi cola','11.2','0','0','2023-08-08 13:51:01'),(197,7,'Pivo','2.1','0','0.3','2023-08-08 13:51:01'),(198,7,'Red-bull','11.3','0','0','2023-08-08 13:51:01'),(199,7,'Rum','0','0','0','2023-08-08 13:51:01'),(200,7,'Sprite','6.9','0','0','2023-08-08 13:51:01'),(203,1,'Černice','9.61','0.49','1.39','2023-08-08 13:51:01'),(210,1,'Pomelo','9.35','0.38','0.6','2023-08-08 13:51:01'),(211,5,'Acidko 1%','4.7','1','3.1','2023-08-08 13:51:26'),(212,5,'Acidko pomaranč','13.9','3','2.7','2023-08-08 13:51:26'),(213,1,'Ananás','22.1','0.2','0.5','2023-08-08 13:51:26'),(214,10,'Bake rolls','62','17','12','2023-08-08 13:51:26'),(217,3,'Brokolica - Bonduelle - mrazená','4.9','0.1','2.7','2023-08-08 13:51:26'),(220,10,'Cukor - včelí med','77.9','0','0.2','2023-08-08 13:51:26'),(221,10,'Cukor vanilkový','97.5','0','0','2023-08-08 13:51:26'),(222,10,'Dresing cesnakový - Spak','11.9','20.6','1.8','2023-08-08 13:51:26'),(223,10,'Dresing Modrý syr - Spak','10.7','21','3','2023-08-08 13:51:26'),(225,2,'Fazule biele v paradajkovej omáčke','9','3.5','4.7','2023-08-08 13:51:26'),(226,2,'Fazule s kuk. v chili om. - Bonduelle','18.3','3.1','4.6','2023-08-08 13:51:26'),(227,2,'Fazuľové strúčky','6.4','0.2','2','2023-08-08 13:51:26'),(228,10,'Horalka','54.5','31.6','8.9','2023-08-08 13:51:26'),(229,10,'Horčica - dionska','8','9','0','2023-08-08 13:51:26'),(230,10,'Horčica - plnotučná','8','9','0','2023-08-08 13:51:26'),(231,10,'Hranolky','35.83','13.83','3.59','2023-08-08 13:51:26'),(232,10,'Hrebeň makový','60.3','8.5','7.2','2023-08-08 13:51:26'),(235,6,'Chlieb maces','79.8','0','11.5','2023-08-08 13:51:26'),(236,6,'Chlieb žitný','36.5','1.3','4.3','2023-08-08 13:51:26'),(238,5,'Jogurt Danone 7 tromfov','13.7','2','3.1','2023-08-08 13:51:27'),(239,5,'Jogurt Danone Activia biely','5.9','3.3','4.2','2023-08-08 13:51:27'),(240,5,'Jogurt Danone Activia müsli','15.2','3','3.7','2023-08-08 13:51:27'),(241,5,'Jogurt Danone Activia ovocny','15.5','2.6','3.5','2023-08-08 13:51:27'),(242,5,'Jogurt Danone Vitalinea','7.9','0.1','4.1','2023-08-08 13:51:27'),(243,5,'Jogurt Danone Vitalinea biely','6.8','0.1','4.9','2023-08-08 13:51:27'),(244,5,'Jogurt Danone Vitalinea marhuľa','6.9','0.1','4.2','2023-08-08 13:51:27'),(245,5,'Jogurt Danone Vitalinea višňa; ananás','7.2','0.1','4.2','2023-08-08 13:51:27'),(246,5,'Jogurt domáci','4.94','1.73','3.42','2023-08-08 13:51:27'),(247,5,'Jogurt Rajo Klasik','15.5','2.5','4.1','2023-08-08 13:51:27'),(248,5,'Jogurt Rajo Nízkotučný','14.7','0.1','3.6','2023-08-08 13:51:27'),(249,5,'Jogurt Rajo Nízkotučný biely','6.6','0.1','4.6','2023-08-08 13:51:27'),(250,3,'Kaleráb','5.8','0.2','2.1','2023-08-08 13:51:27'),(251,3,'Kapusta biela hlávková','4.5','0.2','1.5','2023-08-08 13:51:27'),(252,3,'Kapusta červená hlávková','6.1','0.3','1.6','2023-08-08 13:51:27'),(253,3,'Kapusta čínska','2.4','0.3','1.2','2023-08-08 13:51:27'),(254,3,'Karfiol','4.4','0.3','2.4','2023-08-08 13:51:27'),(255,10,'Knedle na pare','42.25','1.56','6.94','2023-08-08 13:51:27'),(256,8,'Kokos strúhaný','16','68.8','8.9','2023-08-08 13:51:27'),(257,1,'Kukurica sterilizovaná','44.7','3','8.9','2023-08-08 13:51:27'),(258,4,'Kura pečené','1.08','3.2','12.64','2023-08-08 13:51:27'),(260,4,'Makrely','0.1','11.6','18.8','2023-08-08 13:51:27'),(262,9,'Maslo - Flora','0.3','70','0.1','2023-08-08 13:51:27'),(263,9,'Maslo - Flora light','0','40','0','2023-08-08 13:51:27'),(264,9,'Maslo - Veto (100g)','0','38','0','2023-08-08 13:51:27'),(265,5,'Mlieko ovsené (ml)','6.1','2.5','0.5','2023-08-08 13:51:27'),(266,5,'Mlieko polotučné - Wittmann (ml)','4.7','1.5','3.3','2023-08-08 13:51:27'),(267,5,'Mlieko Tesco trvanlivé polotučné (ml)','4.8','1.5','3.3','2023-08-08 13:51:27'),(268,3,'Mrkva','9.7','0.3','1.4','2023-08-08 13:51:27'),(269,6,'Múka hladká extra špeciál','72.8','1.3','9.7','2023-08-08 13:51:27'),(270,9,'Olej olivový','0','100','0','2023-08-08 13:51:28'),(271,8,'Oriešky - Arašidy','23.6','44.2','16.9','2023-08-08 13:51:28'),(272,3,'Paprika červená','5.2','0.5','1.2','2023-08-08 13:51:28'),(273,3,'Paprika zelená','2.6','0.3','0.8','2023-08-08 13:51:28'),(275,3,'Paradajkový pretlak','22.4','0.5','2.3','2023-08-08 13:51:28'),(276,4,'Pečienka kuracia','1.1','4','18.9','2023-08-08 13:51:28'),(278,3,'Pór','8.6','0.3','2.5','2023-08-08 13:51:28'),(280,6,'Rožky Active celozrnné','73','9','11','2023-08-08 13:51:28'),(281,6,'Rožky Active pšeničné','68','9','10','2023-08-08 13:51:28'),(282,4,'Ryby - Filé z aljašskej tresky','0','0.1','16','2023-08-08 13:51:28'),(283,4,'Ryby - Sardinky v oleji','0','13.9','24.1','2023-08-08 13:51:28'),(284,4,'Ryby - Slede mexické','28.7','8','19','2023-08-08 13:51:28'),(286,5,'Smotana do kávy 10%','4.2','10','3.2','2023-08-08 13:51:28'),(288,5,'Syr Apetito Línia','7','8.8','11.8','2023-08-08 13:51:28'),(289,5,'Syr Eidam 45%','0.9','24.5','24.2','2023-08-08 13:51:28'),(290,5,'Syr Karička fitnes s jogurtom','3','10.5','15','2023-08-08 13:51:28'),(291,5,'Syr Niva 50%','0.8','26.5','19.8','2023-08-08 13:51:28'),(292,5,'Syrová pomazánka (hrubý odhad)','4','18','10','2023-08-08 13:51:28'),(293,3,'Šalát ľadový','1.9','0.3','0.7','2023-08-08 13:51:28'),(294,10,'Šalát zemiakový','12','17.5','1.9','2023-08-08 13:51:28'),(295,7,'Šampanské','1.4','0','0.2','2023-08-08 13:51:28'),(296,3,'Šampiňóny sterilizované','2.7','0.4','0.8','2023-08-08 13:51:28'),(297,10,'Špagety - bezvaječné - Cessi','69.8','1.3','9.5','2023-08-08 13:51:28'),(298,4,'Šunka hydinová','0','12.9','26.6','2023-08-08 13:51:28'),(299,4,'Šunka kuracia jemná','0.05','6.8','8.15','2023-08-08 13:51:28'),(300,3,'Tekvica obyčajná','6.2','0.2','1.2','2023-08-08 13:51:28'),(301,10,'Tofu - lahôdkové (AlfaBio)','6.5','8','12','2023-08-08 13:51:28'),(302,10,'Tofu - natural','6.9','2.4','15.5','2023-08-08 13:51:29'),(303,10,'Tofu - špeciál (AlfaBio)','11','4','16','2023-08-08 13:51:29'),(304,10,'Tofu - udené - priemer','10.9','3.5','16.6','2023-08-08 13:51:29'),(305,10,'Tofu - udené (AlfaBio)','12','7','13','2023-08-08 13:51:29'),(306,10,'Tofu - udené (Sojaprodukt)','10','4','16','2023-08-08 13:51:29'),(307,5,'Tvaroh 2.5% (CBA)','4.2','2.5','17.5','2023-08-08 13:51:29'),(308,5,'Tvaroh bez tuku','4.4','0.8','18.8','2023-08-08 13:51:29'),(309,5,'Tvaroh bez tuku (Danone)','3.8','0.3','13.5','2023-08-08 13:51:29'),(310,5,'Tvaroh bez tuku (Oké)','5','1','20','2023-08-08 13:51:29'),(311,3,'Uhorka sterilizovaná','4.9','0','0.4','2023-08-08 13:51:29'),(312,3,'Uhorka šalátová','2.6','0.2','0.7','2023-08-08 13:51:29'),(313,10,'Vajce Bielok (1 ks = 33 g)','0.61','0.3','10.91','2023-08-08 13:51:29'),(314,10,'Vajce celé (1 ks = 50 g)','0.6','13.2','13.2','2023-08-08 13:51:29'),(315,10,'Vajce Žĺtok (1 ks = 20 g)','0.5','32.5','16.5','2023-08-08 13:51:29'),(316,7,'Vermut sladký','15.9','0','0','2023-08-08 13:51:29'),(317,10,'Závin makový','55.6','14.5','8.7','2023-08-08 13:51:29'),(318,3,'Zelenina Wok + Chicken - Red Curry','13','1.5','5','2023-08-08 13:51:29'),(319,3,'Zelenina Wok + Noodles - Coconut & Lime','16','0.4','3','2023-08-08 13:51:29'),(320,3,'Zelenina Wok + Noodles - Sweet Chilli','21','0.6','3','2023-08-08 13:51:29'),(321,3,'Zelenina Wok + Prawn - Ginger & Garlic','13','1.5','4.5','2023-08-08 13:51:29'),(322,3,'Zelenina Wok Thai','7','0.3','1.5','2023-08-08 13:51:29'),(323,3,'Zelenina Wok Vietnamese','4.5','0.3','2','2023-08-08 13:51:29'),(324,3,'Zemiaky ','17','0.3','2','2023-08-08 13:51:29');
/*!40000 ALTER TABLE `potraviny` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `potraviny_diety`
--

DROP TABLE IF EXISTS `potraviny_diety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `potraviny_diety` (
  `id_potravina_diety` int NOT NULL AUTO_INCREMENT,
  `id_dieta` int DEFAULT NULL,
  `id_potravina` int DEFAULT NULL,
  `mnozstvo` varchar(255) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_potravina_diety`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `potraviny_diety`
--

LOCK TABLES `potraviny_diety` WRITE;
/*!40000 ALTER TABLE `potraviny_diety` DISABLE KEYS */;
INSERT INTO `potraviny_diety` VALUES (1,1,57,'1.5','2023-08-14 18:52:41'),(2,2,192,'','2023-08-14 18:54:14'),(3,1,134,'250','2023-08-15 19:10:41'),(4,2,134,NULL,'2023-08-15 19:11:26');
/*!40000 ALTER TABLE `potraviny_diety` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rozdelenie_do_jedal`
--

DROP TABLE IF EXISTS `rozdelenie_do_jedal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rozdelenie_do_jedal` (
  `id_rozdelenie_do_jedal` int NOT NULL AUTO_INCREMENT,
  `id_dieta` int DEFAULT NULL,
  `id_potravina` int DEFAULT NULL,
  `prve_jedlo` varchar(5) DEFAULT NULL,
  `druhe_jedlo` varchar(5) DEFAULT NULL,
  `tretie_jedlo` varchar(5) DEFAULT NULL,
  `stvrte_jedlo` varchar(5) DEFAULT NULL,
  `piate_jedlo` varchar(5) DEFAULT NULL,
  `sieste_jedlo` varchar(5) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_rozdelenie_do_jedal`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rozdelenie_do_jedal`
--

LOCK TABLES `rozdelenie_do_jedal` WRITE;
/*!40000 ALTER TABLE `rozdelenie_do_jedal` DISABLE KEYS */;
/*!40000 ALTER TABLE `rozdelenie_do_jedal` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-29 14:51:24
