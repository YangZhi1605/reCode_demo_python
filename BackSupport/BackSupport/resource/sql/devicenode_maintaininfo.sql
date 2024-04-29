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

 Date: 15/04/2024 15:27:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for devicenode_maintaininfo
-- ----------------------------
DROP TABLE IF EXISTS `devicenode_maintaininfo`;
CREATE TABLE `devicenode_maintaininfo`  (
  `DeviceNodeID` int(0) NOT NULL AUTO_INCREMENT,
  `MaintenanceDate` datetime(0) NULL DEFAULT NULL,
  `MaintenanceUser` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `MaintenanceRport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '检测建议',
  `MaintenanceTage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否处理',
  PRIMARY KEY (`DeviceNodeID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
ALTER TABLE `devicenode_maintaininfo` AUTO_INCREMENT = 1;
