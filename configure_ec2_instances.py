import boto3
from botocore.exceptions import ClientError
import paramiko
import time
import os

key = input("Enter your aws_access_key_id: ")
secrete_key = input("Enter your aws_secret_access_key: ")
session_token = input("Enter your aws_session_token: ")

ec2_client = boto3.client('ec2',
    aws_access_key_id=key,
    aws_secret_access_key=secrete_key,
    aws_session_token= session_token,
    region_name='us-east-1')

response = ec2_client.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')


# ensure the security group name entered does not exist 
existing_security_group_names = []
available_security_groups_info=ec2_client.describe_security_groups().get('SecurityGroups')

for security_group_info in available_security_groups_info:
    existing_security_group_names.append(security_group_info['GroupName'])
print (existing_security_group_names)

security_group = input("Enter a new security group name: ")

while (security_group in existing_security_group_names):
    security_group = input(f"{security_group} already exist, please enter an unique security group name: ")
print(security_group)


# create security group
security_group_id = None
try:
    response = ec2_client.create_security_group(GroupName=security_group,
                                         Description='testing for security group for mongo',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
except ClientError as e:
	print(e)

try:
    data = ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 27017,
             'ToPort': 27017,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
             {'IpProtocol': 'tcp',
             'FromPort': 3306,
             'ToPort': 3306,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])

    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)


# ensure the key_name entered does not exist
existing_key_pairs = []
existing_keys_info = ec2_client.describe_key_pairs().get('KeyPairs')
for key_info in existing_keys_info:
    existing_key_pairs.append(key_info['KeyName'])

key_name = input("Enter a new ec2 key-pair name(without '.pem' behind): ")

while (key_name in existing_key_pairs):
    key_name = input(f"{key_name} already exist, please enter an unique key-pair name: ")
print(key_name)


# generate new ec2 key
keypair = ec2_client.create_key_pair(KeyName=key_name)
key_content = str(keypair['KeyMaterial'])
ec2_key = key_name +".pem" 
key_gen = open(ec2_key,'w')
key_gen.write(key_content)
key_gen.close()
os.system("chmod 400 {}.pem".format(key_name))

session = boto3.session.Session(
        aws_access_key_id=key,
        aws_secret_access_key=secrete_key,
        aws_session_token= session_token,
        region_name='us-east-1')
ec2 = session.resource('ec2')

# create new EC2 instances
instances = ec2.create_instances(
        ImageId='ami-0817d428a6fb68645',
        MinCount=1,
        MaxCount=3,
        InstanceType='t2.micro',
        SecurityGroups=[security_group],
        KeyName=key_name
)

mongodb = instances[0]
mysql = instances[1]
frontend = instances[2]
print("Please wait for your instances to be created.....")

# wait for instance to load
for instance in instances:
	instance.wait_until_running()
	instance.load()

# sleep for 30 seconds for the instance to be fully loaded up
for i in range(30):
	time.sleep(1)

print("MongoDB public IP address is: ", mongodb.public_ip_address)
#print("MongoDB private IP address is: ", mongodb.private_ip_address)
print("MySQL public IP address is: ", mysql.public_ip_address)
print("FrontEnd public IP address is: ", frontend.public_ip_address)


key = paramiko.RSAKey.from_private_key_file(ec2_key)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

mongodb_ip = str(mongodb.public_ip_address)
print(f"setting up mongoDB in ec2 instance with public IP address: {mongodb_ip}. This may take a while....")

# Connect/ssh to mongodb instance
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    ssh_client.connect(hostname=mongodb_ip, username="ubuntu", pkey=key)

    # Execute the commands after connecting/ssh to an instance
    cmd1 = 'wget https://raw.githubusercontent.com/apronoob88/configure_ec2_instances/master/mongo_setup.sh'
    cmd2 = 'sh mongo_setup.sh'
    stdin, stdout, stderr = ssh_client.exec_command(cmd1)
    stdout.read()

    stdin, stdout, stderr = ssh_client.exec_command(cmd2)
    stdout.read()
    print("mongodb successfully set up!")
    # close the client connection once the job is done
    ssh_client.close()
    #break

except Exception as e:
    print (e)
