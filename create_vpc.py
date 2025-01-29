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

def create_security_groups(vpc_id):
    security_groups = {
        "alb_sg": {"name": "prod-alb-sg", "description": "Allow HTTP/HTTPS traffic", "rules": [(80, "0.0.0.0/0"), (443, "0.0.0.0/0")]},
        "frontend_sg": {"name": "prod-frontend-sg", "description": "Allow traffic from ALB", "rules": [(3000, "prod-alb-sg"), (443, "prod-alb-sg")]},
        "backend_sg": {"name": "prod-backend-sg", "description": "Allow traffic from Frontend ECS", "rules": [(5000, "prod-frontend-sg")]},
        "rds_sg": {"name": "prod-rds-sg", "description": "Allow traffic from Backend ECS", "rules": [(3306, "prod-backend-sg")]}
    }
    sg_ids = {}
    for key, sg in security_groups.items():
        response = ec2_client.create_security_group(
            GroupName=sg["name"],
            Description=sg["description"],
            VpcId=vpc_id
        )
        sg_id = response["GroupId"]
        ec2_client.create_tags(Resources=[sg_id], Tags=[{"Key": "Name", "Value": sg["name"]}])
        for port, source in sg["rules"]:
            ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {"IpProtocol": "tcp", "FromPort": port, "ToPort": port, "IpRanges": [{"CidrIp": source}]} if "0.0.0.0/0" in source else
                    {"IpProtocol": "tcp", "FromPort": port, "ToPort": port, "UserIdGroupPairs": [{"GroupName": source}]}
                ]
            )
        sg_ids[key] = sg_id
        print(f"Security Group {sg['name']} created: {sg_id}")
    return sg_ids

def create_network_acls(vpc_id):
    acl = ec2_client.create_network_acl(VpcId=vpc_id)
    acl_id = acl["NetworkAcl"]["NetworkAclId"]
    ec2_client.create_tags(Resources=[acl_id], Tags=[{"Key": "Name", "Value": "prod-acl"}])
    print(f"Network ACL created: {acl_id}")

def create_route_tables(vpc_id):
    public_rt = ec2_client.create_route_table(VpcId=vpc_id)
    public_rt_id = public_rt["RouteTable"]["RouteTableId"]
    ec2_client.create_tags(Resources=[public_rt_id], Tags=[{"Key": "Name", "Value": "prod-public-rt"}])
    print(f"Public Route Table created: {public_rt_id}")
    
    private_rt = ec2_client.create_route_table(VpcId=vpc_id)
    private_rt_id = private_rt["RouteTable"]["RouteTableId"]
    ec2_client.create_tags(Resources=[private_rt_id], Tags=[{"Key": "Name", "Value": "prod-private-rt"}])
    print(f"Private Route Table created: {private_rt_id}")

if __name__ == "__main__":
    vpc_id = create_vpc()
    create_subnets(vpc_id)
    create_security_groups(vpc_id)
    create_network_acls(vpc_id)
    create_route_tables(vpc_id)
