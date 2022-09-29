-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema belt_exam_retake
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema belt_exam_retake
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `belt_exam_retake` DEFAULT CHARACTER SET utf8 ;
USE `belt_exam_retake` ;

-- -----------------------------------------------------
-- Table `belt_exam_retake`.`magazines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam_retake`.`magazines` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `users_id` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `belt_exam_retake`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam_retake`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `pasword` VARCHAR(225) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `belt_exam_retake`.`users_has_magazines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam_retake`.`users_has_magazines` (
  `users_id` INT NOT NULL,
  `magazines_id` INT NOT NULL,
  PRIMARY KEY (`users_id`, `magazines_id`),
  INDEX `fk_users_has_magazines_magazines1_idx` (`magazines_id` ASC) VISIBLE,
  INDEX `fk_users_has_magazines_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_magazines_magazines1`
    FOREIGN KEY (`magazines_id`)
    REFERENCES `belt_exam_retake`.`magazines` (`id`),
  CONSTRAINT `fk_users_has_magazines_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `belt_exam_retake`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
