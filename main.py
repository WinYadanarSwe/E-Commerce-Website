import create_vpc
import create_ecs_autoscaling
import create_rds_read_replica

def main():
    print("Starting AWS Infrastructure Setup...")
    
    # Step 1: Create VPC & Subnets
    print("Creating VPC and Subnets...")
    vpc_id = create_vpc.create_vpc()
    create_vpc.create_subnets(vpc_id)
    
    # Step 2: Setup ECS Auto Scaling
    print("Setting up ECS Auto Scaling...")
    create_ecs_autoscaling.create_ecs_autoscaling()
    
    # Step 3: Setup RDS Read Replicas
    print("Creating RDS Read Replicas...")
    create_rds_read_replica.create_rds_read_replica()

    print("✅ AWS Infrastructure Setup Complete!")

if __name__ == "__main__":
    main()
