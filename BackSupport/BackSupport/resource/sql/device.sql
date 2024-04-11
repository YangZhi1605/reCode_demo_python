/*
 Navicat Premium Data Transfer

 Source Server         : mysql8.0
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : graduate

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 04/04/2024 15:11:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS `device_upload`;
CREATE TABLE `device_upload`  (
  `ID` int(0) NOT NULL AUTO_INCREMENT,
  `InfoType` int(0) NULL DEFAULT NULL,
  `DeviceNodeID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `DeviceName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `UserID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `CollectTime` datetime(0) NULL DEFAULT NULL,
  `Voltage1` float NULL DEFAULT NULL,
  `Voltage2` float NULL DEFAULT NULL,
  `Voltage3` float NULL DEFAULT NULL,
  `Voltage4` float NULL DEFAULT NULL,
  `Voltage5` float NULL DEFAULT NULL,
  `Voltage6` float NULL DEFAULT NULL,
  `Voltage7` float NULL DEFAULT NULL,
  `Voltage8` float NULL DEFAULT NULL,
  `Voltage9` float NULL DEFAULT NULL,
  `Voltage10` float NULL DEFAULT NULL,
  `Voltage11` float NULL DEFAULT NULL,
  `Voltage12` float NULL DEFAULT NULL,
  `Voltage13` float NULL DEFAULT NULL,
  `Voltage14` float NULL DEFAULT NULL,
  `Voltage15` float NULL DEFAULT NULL,
  `Voltage16` float NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 654378 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
ALTER TABLE my_table AUTO_INCREMENT = 1;


