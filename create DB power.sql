CREATE DATABASE `power` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_czech_ci */;
CREATE TABLE `power` (
  `datum` datetime DEFAULT NULL,
  `id_phase` int(1) DEFAULT NULL,
  `voltage` float(4,1) DEFAULT NULL,
  `current` float(5,2) DEFAULT NULL,
  `power` float(6,1) DEFAULT NULL,
  `energy` float(10,1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `idx_power_datum` (`datum`),
  KEY `idx_power_id_phase` (`id_phase`),
  KEY `idx_power_voltage` (`voltage`),
  KEY `idx_power_current` (`current`),
  KEY `idx_power_power` (`power`),
  KEY `idx_power_energy` (`energy`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

