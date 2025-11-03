#!/bin/bash

# Navigate to project directory
cd "D:\College\TY SEM 1\ML\PBL\ML PROJECT\skill-gap-analyzer"

# Get actual values
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
RDS_ENDPOINT=$(aws rds describe-db-instances --db-instance-identifier skill-gap-db --query 'DBInstances[0].Endpoint.Address' --output text)

echo "Account ID: $ACCOUNT_ID"
echo "RDS Endpoint: $RDS_ENDPOINT"

# Create task definition with actual values
cat > ecs-task-definition.json << EOF
{
  "family": "skill-gap-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "600771337569.dkr.ecr.us-east-1.amazonaws.com/skill-gap-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "mysql://admin:SkillGap2024!@skill-gap-db.c43egaa0es0z.us-east-1.rds.amazonaws.com/skill_gap_analyzer"
        },
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/skill-gap-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

echo "✅ File created: ecs-task-definition.json"