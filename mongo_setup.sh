#!/bin/bash

# install mongo
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl restart mongod
# sleep 5 second to allow mongod fully started
sleep 5

# configure mongo
mongo < create_mongo_user.js
sudo systemctl restart mongod

sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf
sudo sed -i "s/#security:/security:\n  authorization: 'enabled'/g" /etc/mongod.conf
sudo apt install unzip
wget -c https://dbproject.s3.amazonaws.com/meta_kindle_store_update.zip
unzip meta_kindle_store_update.zip
rm -rf *.zip

mongoimport --db dbproject --collection metadata --authenticationDatabase admin --username yt --password password --drop --file ~/meta_kindle_store_update.json
mongo -u yt -p password < create_mongo_index.js