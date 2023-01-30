
DROP TABLE IF EXISTS `derby_web`.`tbl_account`;
CREATE TABLE `derby_web`.`tbl_account` (
  `uid` BIGINT NOT NULL AUTO_INCREMENT,
  `id` VARCHAR(45) NOT NULL,
  `pw` VARCHAR(45) NOT NULL,
  `nickname` VARCHAR(45) NOT NULL,
  `create_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`, `id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;
