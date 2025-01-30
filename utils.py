import boto3

def add_tags(resource_id, tags):
    ec2_client = boto3.client('ec2')
    ec2_client.create_tags(Resources=[resource_id], Tags=tags)
    print(f"Tags added to {resource_id}")
