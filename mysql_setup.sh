#!/bin/bash

# install mysql
sudo apt-get update
echo "Installing MySQL server"
sudo apt-get install -y mysql-server

echo "Initializing root user with privileges"
sudo mysql -e 'update mysql.user set plugin = "mysql_native_password" where user = "root"'
sudo mysql -e 'create user if not exists "root"@"%" identified by ""'
sudo mysql -e 'grant all privileges on *.* to "root"@"%" with grant option'
sudo mysql -e 'flush privileges'
sudo service mysql restart
# sleep 5 second to allow mysql fully started
sleep 5

echo "Access MySQL using root"
mysql -u root << EOF
CREATE DATABASE IF NOT EXISTS bookwormies;
USE bookwormies;
CREATE TABLE IF NOT EXISTS reviewers (
  reviewer_id VARCHAR(45) NOT NULL,
  reviewer_name VARCHAR(45) NOT NULL,
  username VARCHAR(45) NOT NULL,
  password VARCHAR(45) NOT NULL,
  PRIMARY KEY (reviewer_id),
  UNIQUE KEY username_UNIQUE (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS reviews (
  review_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  asin VARCHAR(45) NOT NULL,
  likes INT NOT NULL DEFAULT '0',
  dislikes INT NOT NULL DEFAULT '0',
  overall_rating INT NOT NULL DEFAULT '0',
  review_text VARCHAR(8000) NOT NULL,
  review_time DATE NOT NULL,
  reviewer_id VARCHAR(45) NOT NULL,
  summary VARCHAR(8000) DEFAULT NULL,
  unix_review_time INT DEFAULT NULL,
  PRIMARY KEY (review_id),
  FOREIGN KEY (reviewer_id) REFERENCES reviewers(reviewer_id),
  KEY idx_asin (asin)
) ENGINE=InnoDB AUTO_INCREMENT=982632 DEFAULT CHARSET=utf8;

LOAD DATA LOCAL INFILE '~/reviewers.csv' INTO TABLE reviewers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(reviewer_id, reviewer_name, username, password);

LOAD DATA LOCAL INFILE '~/reviews.csv' INTO TABLE reviews
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(review_id, asin, likes, dislikes, overall_rating, review_text, review_time, reviewer_id, summary, unix_review_time);

EOF