import boto3
from botocore.exceptions import ClientError
import json
import os
import time

# Import from config.json
with open('config.json', "r") as config_file:
  data = json.load(config_file)
  config_file.close()

# Variables
key = data['aws_access_key_id']
secret_key = data['aws_secret_access_key']
session_token = data['aws_session_token']
ids = data['instance_ids']
security_group_id = data['security_group_id']
key_name = data['key_name']

ec2_client = boto3.client('ec2',
  aws_access_key_id=key,
  aws_secret_access_key=secret_key,
  aws_session_token=session_token,
  region_name='us-east-1'
)

session = boto3.session.Session(
  aws_access_key_id=key,
  aws_secret_access_key=secret_key,
  aws_session_token=session_token,
  region_name='us-east-1'
)
ec2 = session.resource('ec2')

try:
  # Terminate all instances
  print("Terminating all instances...")
  ec2.instances.filter(InstanceIds=ids).terminate()
  time.sleep(10)
  print("All instances terminated!")

  # Delete security group
  print("Deleting security group...")
  ec2_client.delete_security_group(GroupId=security_group_id)
  print("Security group deleted!")

  # Delete the key pair
  key_file = "{0}.pem".format(key_name)
  print("Deleting {0}...".format(key_file))
  ec2_client.delete_key_pair(KeyName=key_name)
  if os.path.exists(key_file):
    os.remove(key_file)
  else:
    print("{0} does not exist!".format(key_file))
  print("{0} deleted!".format(key_file))

except ClientError as e:
  print(e)