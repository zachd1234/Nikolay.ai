#!/bin/bash

# AWS Deployment Script for Nikolay.ai Hack Event

echo "========================================"
echo "AWS Deployment for Nikolay.ai Hack Event"
echo "========================================"

# Check if required files exist
required_files=("app.py" "requirements.txt" "hack_event_invitation.html" "assets/logo.png" "assets/nikolayTalk.mp4" ".env")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "Error: Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

# Create deployment directory
DEPLOY_DIR="deploy_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEPLOY_DIR"

# Copy files to deployment directory
echo "Preparing deployment files..."
cp app.py requirements.txt "$DEPLOY_DIR/"
cp hack_event_invitation.html "$DEPLOY_DIR/"
cp -r assets "$DEPLOY_DIR/"
cp .env "$DEPLOY_DIR/"

# Create Dockerfile
echo "Creating Dockerfile..."
cat > "$DEPLOY_DIR/Dockerfile" << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create docker-compose.yml for local testing
echo "Creating docker-compose.yml..."
cat > "$DEPLOY_DIR/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=password
      - DB_NAME=nikolay_hack_event
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=nikolay_hack_event
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
EOF

# Create AWS deployment script
echo "Creating AWS deployment script..."
cat > "$DEPLOY_DIR/deploy_aws.sh" << 'EOF'
#!/bin/bash

# Build and push Docker image
docker build -t nikolay-hack-event .
docker tag nikolay-hack-event:latest your-aws-account-id.dkr.ecr.your-region.amazonaws.com/nikolay-hack-event:latest

# Push to ECR (you need to be logged in to AWS ECR first)
docker push your-aws-account-id.dkr.ecr.your-region.amazonaws.com/nikolay-hack-event:latest

# Create ECS task definition (replace with your actual values)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Update ECS service
aws ecs update-service --cluster your-cluster --service your-service --task-definition your-task-definition

echo "Deployment complete!"
EOF

chmod +x "$DEPLOY_DIR/deploy_aws.sh"

# Create task definition template
echo "Creating ECS task definition template..."
cat > "$DEPLOY_DIR/task-definition.json" << 'EOF'
{
  "family": "nikolay-hack-event",
  "networkMode": "awsvpc",
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::your-aws-account-id:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::your-aws-account-id:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "nikolay-hack-event",
      "image": "your-aws-account-id.dkr.ecr.your-region.amazonaws.com/nikolay-hack-event:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DB_HOST",
          "value": "your-rds-endpoint"
        },
        {
          "name": "DB_USER",
          "value": "your-db-user"
        },
        {
          "name": "DB_PASSWORD",
          "value": "your-db-password"
        },
        {
          "name": "DB_NAME",
          "value": "nikolay_hack_event"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/nikolay-hack-event",
          "awslogs-region": "your-region",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

echo ""
echo "========================================"
echo "Deployment files prepared in: $DEPLOY_DIR"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Review and update the configuration files in $DEPLOY_DIR"
echo "2. For local testing: cd $DEPLOY_DIR && docker-compose up"
echo "3. For AWS deployment: cd $DEPLOY_DIR && ./deploy_aws.sh"
echo ""
echo "Note: Make sure to replace placeholder values in the AWS configuration files"
