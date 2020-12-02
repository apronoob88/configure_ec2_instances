#!/bin/bash

# install mysql
sudo apt-get update
sudo apt-get install -y mysql-server

sudo mysql -e 'update mysql.user set plugin = "mysql_native_password" where user = "root"'
sudo mysql -e 'create user "root"@"%" identified by ""'
sudo mysql -e 'grant all privileges on *.* to "root"@"%" with grant option'
sudo mysql -e 'flush privileges'
sudo service mysql restart