# E-Commerce-Website
E-Commerce Website Migration to AWS Cloud

On-pre
- E-Commerce Web Application selling multiple types of products
- constant traffic of around 100,000 users per days
- separate Frontend and Backend Component. 
- MySQL Database - store all data (users and products)
- Production Environment
- Test Environment

Cloud (AWS)
DNS - You can use any name for the Domain Name 
Web Application - Frontend & Backend 
Database - File Storage (Images & Videos) 
Automated Deployment 

Use the following services,
High Availability: ECS, ALB, RDS (Multi-AZ), and NAT Gateways provide redundancy.
Scalability: ECS auto-scaling, CloudFront, and RDS read replicas handle traffic spikes.
Security: WAF, IAM, and private subnet isolation protect against vulnerabilities.
Cost Optimization: S3, NAT Gateways, and auto-scaling reduce unnecessary costs.
Monitoring and Compliance: CloudWatch and CloudTrail ensure visibility into operations.
