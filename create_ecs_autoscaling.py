import boto3

autoscaling_client = boto3.client('autoscaling')

def create_ecs_autoscaling():
    # Frontend ECS Scaling (ALB Request-Based)
    autoscaling_client.put_scaling_policy(
        AutoScalingGroupName="ecs-frontend-autoscale",
        PolicyName="scale-out-alb",
        AdjustmentType="ChangeInCapacity",
        ScalingAdjustment=1,
        Cooldown=60
    )

    # Backend ECS Scaling (CPU Utilization-Based)
    autoscaling_client.put_scaling_policy(
        AutoScalingGroupName="ecs-backend-autoscale",
        PolicyName="scale-out-cpu",
        AdjustmentType="ChangeInCapacity",
        ScalingAdjustment=1,
        Cooldown=60
    )
    
    print("ECS Auto Scaling Policies Created")

if __name__ == "__main__":
    create_ecs_autoscaling()
