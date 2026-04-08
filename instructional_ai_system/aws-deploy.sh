#!/bin/bash
# aws-deploy.sh
# Run this on a fresh Ubuntu EC2 Instance

echo "Starting deployment setup..."

# 1. Update and install Docker & Git
sudo apt-get update -y
sudo apt-get install -y git docker.io docker-compose

# 2. Start and enable Docker
sudo systemctl enable docker
sudo systemctl start docker

# 3. Add current user to docker group (so no sudo is needed)
sudo usermod -aG docker ubuntu

# 4. Add 2GB Swap Space (CRUCIAL for AWS Free Tier t2.micro to prevent crashing during build)
echo "Allocating 2GB Swap Space..."
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo sysctl vm.swappiness=10

# 5. Clone the repository
git clone https://github.com/Srirajop/AI-Instructional-Design-Automation-System.git
cd AI-Instructional-Design-Automation-System

# 6. Create .env file for Docker Compose
cat <<EOF > .env
GROQ_API_KEY=your_production_groq_api_key_here
DB_PASSWORD=secure_database_password_123
SECRET_KEY=$(openssl rand -hex 32)
EOF

echo "Deployment fetched!"
echo "Please edit the .env file with your actual GROQ_API_KEY: nano .env"
echo "After editing, run: sudo docker-compose -f docker-compose.yml up -d --build"
echo "Note: If docker-compose command is not found, you can run: sudo apt install docker-compose-v2 then use docker compose up -d --build"
