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

 Date: 13/04/2024 16:45:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device_circuit_weight
-- ----------------------------
DROP TABLE IF EXISTS `device_circuit_weight`;
CREATE TABLE `device_circuit_weight`  (
  `DataID` int(0) NOT NULL AUTO_INCREMENT,
  `RuleName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '某套权重分配规则的名称',
  `Circuit1` float(40, 4) NULL DEFAULT NULL COMMENT '电路权重',
  `Circuit2` float(40, 4) NULL DEFAULT NULL,
  `Circuit3` float(40, 4) NULL DEFAULT NULL,
  `Circuit4` float(40, 4) NULL DEFAULT NULL,
  `Circuit5` float(40, 4) NULL DEFAULT NULL,
  `Circuit6` float(40, 4) NULL DEFAULT NULL,
  `Circuit7` float(40, 4) NULL DEFAULT NULL,
  `Circuit8` float(40, 4) NULL DEFAULT NULL,
  `IsSet` int(0) NULL DEFAULT NULL COMMENT '通过0和1表示是否运用',
  PRIMARY KEY (`DataID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
ALTER TABLE device_circuit_weight AUTO_INCREMENT = 1;
