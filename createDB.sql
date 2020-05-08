DROP DATABASE IF EXISTS `ssp`;
CREATE DATABASE IF NOT EXISTS `ssp` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE ssp;

-- DROP TABLE IF EXISTS `information_systems`;
CREATE TABLE `information_systems` (
  `information_system_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`information_system_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- DROP TABLE IF EXISTS `securityControls`;
CREATE TABLE `securityControls` (
  `system_id` int(11) NOT NULL,
  `control_id` varchar(10) NOT NULL,
  `responsableRole` varchar(255) DEFAULT NULL,
  `parameterList` varchar(1000) DEFAULT NULL,
  `implementationStatus` varchar(1000) DEFAULT NULL,
  `controlOrigination` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`control_id`),
  KEY `fk_securityControls_1_idx` (`system_id`),
  CONSTRAINT `fk_securityControls_1` FOREIGN KEY (`system_id`) REFERENCES `information_systems` (`information_system_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- DROP TABLE IF EXISTS `controlResponse`;
CREATE TABLE `controlResponse` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `control_id` varchar(10) NOT NULL,
  `part` varchar(45) DEFAULT NULL,
  `value` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_controlResponse_control_id_idx` (`control_id`),
  KEY `fk_controlResponse_2_idx` (`system_id`),
  CONSTRAINT `fk_controlResponse_1` FOREIGN KEY (`control_id`) REFERENCES `securityControls` (`control_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_controlResponse_2` FOREIGN KEY (`system_id`) REFERENCES `information_systems` (`information_system_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=latin1;

-- DROP TABLE IF EXISTS `sspSections`;
CREATE TABLE `sspSections` (
  `system_id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL AUTO_INCREMENT,
  `sectionTitle` varchar(255) NOT NULL,
  `sectionText` longtext,
  PRIMARY KEY (`section_id`),
  KEY `fk_sspSections_1_idx` (`system_id`),
  CONSTRAINT `fk_sspSections_1` FOREIGN KEY (`system_id`) REFERENCES `information_systems` (`information_system_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=latin1;