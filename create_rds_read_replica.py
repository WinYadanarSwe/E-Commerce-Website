import boto3

rds_client = boto3.client('rds')

def create_rds_read_replica():
    response = rds_client.create_db_instance_read_replica(
        DBInstanceIdentifier="my-rds-read-replica",
        SourceDBInstanceIdentifier="my-primary-db",
        DBInstanceClass="db.m5.large",
        AvailabilityZone="us-central1b"
    )
    print(f"RDS Read Replica Created: {response['DBInstance']['DBInstanceIdentifier']}")

if __name__ == "__main__":
    create_rds_read_replica()
