/********************
 Data definition
 ********************/

/* We create have an "if not exists" because if the container is started
   with MYSQL_DATABASE defined in the environment then the database name
   will already exist. */
CREATE DATABASE IF NOT EXISTS CorpDb;

USE CorpDb;

CREATE TABLE menu (
  menu_item_id INT NOT NULL AUTO_INCREMENT,
  item_name CHAR(30) NOT NULL,
  PRIMARY KEY (menu_item_id));

/********************
 User setup
 ********************/
CREATE USER 'a_user'@'%' IDENTIFIED BY 'a_password';
GRANT ALL PRIVILEGES ON CorpDb.* TO 'a_user'@'%';

/********************
 Data creation
 ********************/

INSERT INTO `menu` (`item_name`) VALUES ('Americano');
INSERT INTO `menu` (`item_name`) VALUES ('Espresso');
INSERT INTO `menu` (`item_name`) VALUES ('Hot Cocoa');
INSERT INTO `menu` (`item_name`) VALUES ('Jelly Doughnut');
INSERT INTO `menu` (`item_name`) VALUES ('Croissant');
INSERT INTO `menu` (`item_name`) VALUES ('Latte');
