CREATE DATABASE  IF NOT EXISTS `productdesign` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `productdesign`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: productdesign
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add design request',7,'add_designrequest'),(26,'Can change design request',7,'change_designrequest'),(27,'Can delete design request',7,'delete_designrequest'),(28,'Can view design request',7,'view_designrequest'),(29,'Can add design attachment',8,'add_designattachment'),(30,'Can change design attachment',8,'change_designattachment'),(31,'Can delete design attachment',8,'delete_designattachment'),(32,'Can view design attachment',8,'view_designattachment'),(33,'Can add product',9,'add_product'),(34,'Can change product',9,'change_product'),(35,'Can delete product',9,'delete_product'),(36,'Can view product',9,'view_product'),(37,'Can add product status log',10,'add_productstatuslog'),(38,'Can change product status log',10,'change_productstatuslog'),(39,'Can delete product status log',10,'delete_productstatuslog'),(40,'Can view product status log',10,'view_productstatuslog'),(41,'Can add feedback',11,'add_feedback'),(42,'Can change feedback',11,'change_feedback'),(43,'Can delete feedback',11,'delete_feedback'),(44,'Can view feedback',11,'view_feedback');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_myapp_customuser_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_myapp_customuser_user_id` FOREIGN KEY (`user_id`) REFERENCES `myapp_customuser` (`user_id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(6,'myapp','customuser'),(8,'myapp','designattachment'),(7,'myapp','designrequest'),(11,'myapp','feedback'),(9,'myapp','product'),(10,'myapp','productstatuslog'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'myapp','0001_initial','2025-02-09 11:24:31.568226'),(2,'contenttypes','0001_initial','2025-02-09 11:24:31.616943'),(3,'admin','0001_initial','2025-02-09 11:24:31.796137'),(4,'admin','0002_logentry_remove_auto_add','2025-02-09 11:24:31.801290'),(5,'admin','0003_logentry_add_action_flag_choices','2025-02-09 11:24:31.805082'),(6,'contenttypes','0002_remove_content_type_name','2025-02-09 11:24:31.945739'),(7,'auth','0001_initial','2025-02-09 11:24:32.384314'),(8,'auth','0002_alter_permission_name_max_length','2025-02-09 11:24:32.470497'),(9,'auth','0003_alter_user_email_max_length','2025-02-09 11:24:32.478299'),(10,'auth','0004_alter_user_username_opts','2025-02-09 11:24:32.484321'),(11,'auth','0005_alter_user_last_login_null','2025-02-09 11:24:32.491301'),(12,'auth','0006_require_contenttypes_0002','2025-02-09 11:24:32.494134'),(13,'auth','0007_alter_validators_add_error_messages','2025-02-09 11:24:32.499500'),(14,'auth','0008_alter_user_username_max_length','2025-02-09 11:24:32.505485'),(15,'auth','0009_alter_user_last_name_max_length','2025-02-09 11:24:32.513426'),(16,'auth','0010_alter_group_name_max_length','2025-02-09 11:24:32.542349'),(17,'auth','0011_update_proxy_permissions','2025-02-09 11:24:32.554320'),(18,'auth','0012_alter_user_first_name_max_length','2025-02-09 11:24:32.561300'),(19,'myapp','0002_designrequest_designattachment_product_and_more','2025-02-09 11:24:33.004603'),(20,'sessions','0001_initial','2025-02-09 11:24:33.041958'),(21,'myapp','0003_feedback','2025-02-09 11:25:15.945269');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6xoy4f0kacbzm6f8wlewfevea1dositq','.eJxVzMsOgjAQheF36doQ2g5Txp36IGRapoEYLqHtwhjfXUlYyPZ8Of9bdVzy0JUkWzf26qqMuvxvnsNT5h2mF69rtYvMeQycx2WuDq4eJeVlup3wflxPvYHT8It5gkhkeocCjXMetLagG8KmNwKePKJxWIutrQhzy2hDTagjRIQ2RPX5Ag1VPcU:1tmPHP:h3EKS9IzF6IAR8PLAGGsEVx-BgvbRMaXo5LT5ZceB7s','2025-03-10 03:37:15.933446'),('mg55ucphg90zavgwga6bgi8chcwenrey','.eJxVzMsOgjAQheF36doQ2g5Txp36IGRapoEYLqHtwhjfXUlYyPZ8Of9bdVzy0JUkWzf26qqMuvxvnsNT5h2mF69rtYvMeQycx2WuDq4eJeVlup3wflxPvYHT8It5gkhkeocCjXMetLagG8KmNwKePKJxWIutrQhzy2hDTagjRIQ2RPX5Ag1VPcU:1tlt0e:kDOIyATYnx9CtuOLKuUUbUvzECtwALoCtdKglfVUpSU','2025-03-08 17:09:48.487017');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myapp_customuser`
--

DROP TABLE IF EXISTS `myapp_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_customuser` (
  `last_login` datetime(6) DEFAULT NULL,
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_customuser`
--

LOCK TABLES `myapp_customuser` WRITE;
/*!40000 ALTER TABLE `myapp_customuser` DISABLE KEYS */;
INSERT INTO `myapp_customuser` VALUES ('2025-02-24 03:36:51.745016',1,'nva@gmail.com','123','Thư ký','2000-12-12 00:00:00.000000'),('2025-02-24 03:37:15.929455',2,'admin@gmail.com','123','Trưởng phòng','2025-02-10 02:25:05.219968'),('2025-02-24 03:36:19.475907',3,'designer@gmail.com','123','Người thiết kế','2025-02-10 02:29:41.683611');
/*!40000 ALTER TABLE `myapp_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myapp_designrequest`
--

DROP TABLE IF EXISTS `myapp_designrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_designrequest` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `designer_id` int NOT NULL,
  `product_id` int NOT NULL,
  `file_path` text,
  PRIMARY KEY (`request_id`),
  KEY `myapp_designrequest_product_id_12c6d252_fk_myapp_pro` (`product_id`),
  KEY `myapp_designrequest_designer_id_9199dac5_fk_myapp_cus` (`designer_id`),
  CONSTRAINT `myapp_designrequest_designer_id_9199dac5_fk_myapp_cus` FOREIGN KEY (`designer_id`) REFERENCES `myapp_customuser` (`user_id`),
  CONSTRAINT `myapp_designrequest_product_id_12c6d252_fk_myapp_pro` FOREIGN KEY (`product_id`) REFERENCES `myapp_product` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_designrequest`
--

LOCK TABLES `myapp_designrequest` WRITE;
/*!40000 ALTER TABLE `myapp_designrequest` DISABLE KEYS */;
INSERT INTO `myapp_designrequest` VALUES (8,'Gundam (ガンダム Gandamu?) là dòng sản phẩm truyền thông khoa học viễn tưởng được sản xuất bởi Sunrise, dòng sản phẩm này xoay quanh những người máy khổng lồ (mecha) với tên gọi \"Gundam\"','Chấp nhận','2025-02-22 17:09:01.752626',3,3,'design_requests\\gundam.png'),(10,'Test 1','Chấp nhận','2025-02-24 03:36:38.218878',3,2,'design_requests\\images.ico');
/*!40000 ALTER TABLE `myapp_designrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myapp_product`
--

DROP TABLE IF EXISTS `myapp_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_product` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int NOT NULL,
  `designer_id` int DEFAULT NULL,
  `file_path` text,
  PRIMARY KEY (`product_id`),
  KEY `myapp_product_created_by_id_87da7bca_fk_myapp_customuser_user_id` (`created_by_id`),
  KEY `fk_designer` (`designer_id`),
  CONSTRAINT `fk_designer` FOREIGN KEY (`designer_id`) REFERENCES `myapp_customuser` (`user_id`) ON DELETE SET NULL,
  CONSTRAINT `myapp_product_created_by_id_87da7bca_fk_myapp_customuser_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `myapp_customuser` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_product`
--

LOCK TABLES `myapp_product` WRITE;
/*!40000 ALTER TABLE `myapp_product` DISABLE KEYS */;
INSERT INTO `myapp_product` VALUES (1,'Sản phẩm 1','Tạo yêu cầu 1','Chờ phát hành','2025-02-21 16:03:54.889676',1,3,'design_requests\\Dump20250222.sql'),(2,'Test','Test 1','Đã phát hành','2025-02-21 16:58:49.533171',1,3,'design_requests\\images.ico'),(3,'Mô hình gundam 123','Gundam (ガンダム Gandamu?) là dòng sản phẩm truyền thông khoa học viễn tưởng được sản xuất bởi Sunrise, dòng sản phẩm này xoay quanh những người máy khổng lồ (mecha) với tên gọi \"Gundam\"','Đã phát hành','2025-02-22 17:07:56.265018',1,3,'design_requests\\gundam.png');
/*!40000 ALTER TABLE `myapp_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myapp_productfeedback`
--

DROP TABLE IF EXISTS `myapp_productfeedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_productfeedback` (
  `product_feedback_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_feedback_id`),
  KEY `myapp_productfeedback_ibfk_1` (`product_id`),
  KEY `myapp_productfeedback_ibfk_2` (`sender_id`),
  KEY `myapp_productfeedback_ibfk_3` (`receiver_id`),
  CONSTRAINT `myapp_productfeedback_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `myapp_product` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `myapp_productfeedback_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `myapp_customuser` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `myapp_productfeedback_ibfk_3` FOREIGN KEY (`receiver_id`) REFERENCES `myapp_customuser` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_productfeedback`
--

LOCK TABLES `myapp_productfeedback` WRITE;
/*!40000 ALTER TABLE `myapp_productfeedback` DISABLE KEYS */;
INSERT INTO `myapp_productfeedback` VALUES (1,1,2,1,'Cần sửa vài file','2025-02-24 03:33:26'),(2,1,2,1,'Cần sửa vài file','2025-02-24 03:33:35'),(3,1,2,1,'Cần sửa vài file','2025-02-24 03:33:41'),(4,1,2,1,'Alo','2025-02-24 03:33:46');
/*!40000 ALTER TABLE `myapp_productfeedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myapp_productstatuslog`
--

DROP TABLE IF EXISTS `myapp_productstatuslog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_productstatuslog` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `status` varchar(50) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `product_id` int NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `myapp_productstatusl_product_id_f28ed197_fk_myapp_pro` (`product_id`),
  CONSTRAINT `myapp_productstatusl_product_id_f28ed197_fk_myapp_pro` FOREIGN KEY (`product_id`) REFERENCES `myapp_product` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_productstatuslog`
--

LOCK TABLES `myapp_productstatuslog` WRITE;
/*!40000 ALTER TABLE `myapp_productstatuslog` DISABLE KEYS */;
/*!40000 ALTER TABLE `myapp_productstatuslog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myapp_requestfeedback`
--

DROP TABLE IF EXISTS `myapp_requestfeedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myapp_requestfeedback` (
  `request_feedback_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int NOT NULL,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_feedback_id`),
  KEY `myapp_requestfeedback_ibfk_1` (`request_id`),
  KEY `myapp_requestfeedback_ibfk_2` (`sender_id`),
  KEY `myapp_requestfeedback_ibfk_3` (`receiver_id`),
  CONSTRAINT `myapp_requestfeedback_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `myapp_designrequest` (`request_id`) ON DELETE CASCADE,
  CONSTRAINT `myapp_requestfeedback_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `myapp_customuser` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `myapp_requestfeedback_ibfk_3` FOREIGN KEY (`receiver_id`) REFERENCES `myapp_customuser` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myapp_requestfeedback`
--

LOCK TABLES `myapp_requestfeedback` WRITE;
/*!40000 ALTER TABLE `myapp_requestfeedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `myapp_requestfeedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'productdesign'
--

--
-- Dumping routines for database 'productdesign'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-24 10:40:25
