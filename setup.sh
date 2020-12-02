#!/bin/bash

# Linux Setup
if [[ "$OSTYPE" == "linux-gnu"* ]]
then
  sudo apt-get update
  sudo apt-get install -y python3-pip
  python3 -m pip install boto3
  sudo apt-get install -y python3-paramiko
  # Check if this works for Windows
  python3 -m pip install scp

# MacOS Setup
elif [[ "$OSTYPE" == "darwin"* ]]
then
  brew install python3
  python3 -m pip install boto3
  python3 -m pip install paramiko
  python3 -m pip install scp

else
  echo "This script is only for Unix based systems"
fi

wget https://raw.githubusercontent.com/apronoob88/configure_ec2_instances/master/configure_ec2_instances.py
python3 configure_ec2_instances.py