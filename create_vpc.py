import boto3

ec2_client = boto3.client('ec2')

VPC_CIDR = "10.10.0.0/16"
VPC_NAME = "prod-vpc"
SUBNETS = [
    {"Name": "prod-public-subnet-a", "CIDR": "10.10.1.0/24", "Zone": "us-central1a", "Public": True},
    {"Name": "prod-public-subnet-b", "CIDR": "10.10.2.0/24", "Zone": "us-central1b", "Public": True},
    {"Name": "prod-private-ecs-frontend-a", "CIDR": "10.10.3.0/24", "Zone": "us-central1a", "Public": False},
    {"Name": "prod-private-ecs-frontend-b", "CIDR": "10.10.4.0/24", "Zone": "us-central1b", "Public": False},
    {"Name": "prod-private-ecs-backend-a", "CIDR": "10.10.5.0/24", "Zone": "us-central1a", "Public": False},
    {"Name": "prod-private-ecs-backend-b", "CIDR": "10.10.6.0/24", "Zone": "us-central1b", "Public": False},
    {"Name": "prod-private-db-a", "CIDR": "10.10.7.0/24", "Zone": "us-central1a", "Public": False},
    {"Name": "prod-private-db-b", "CIDR": "10.10.8.0/24", "Zone": "us-central1b", "Public": False}
]

def create_vpc():
    vpc = ec2_client.create_vpc(CidrBlock=VPC_CIDR)
    vpc_id = vpc["Vpc"]["VpcId"]
    ec2_client.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": VPC_NAME}])
    print(f"VPC {VPC_NAME} created: {vpc_id}")
    return vpc_id

def create_subnets(vpc_id):
    for subnet in SUBNETS:
        response = ec2_client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=subnet["CIDR"],
            AvailabilityZone=subnet["Zone"]
        )
        subnet_id = response["Subnet"]["SubnetId"]
        ec2_client.create_tags(Resources=[subnet_id], Tags=[{"Key": "Name", "Value": subnet["Name"]}])
        print(f"Subnet {subnet['Name']} created: {subnet_id}")

if __name__ == "__main__":
    vpc_id = create_vpc()
    create_subnets(vpc_id)
