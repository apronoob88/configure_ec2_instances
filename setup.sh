sudo apt-get update
sudo apt-get install -y python3-pip
python3 -m pip install boto3
sudo apt-get install -y python3-paramiko

wget https://raw.githubusercontent.com/apronoob88/configure_ec2_instances/master/configure_ec2_instances.py
python3 configure_ec2_instances.py