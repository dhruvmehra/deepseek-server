# DeepSeek EC2 Setup Guide

This guide provides step-by-step instructions for setting up a DeepSeek server on AWS EC2.

## EC2 Instance Setup

### Instance Requirements
- **AMI**: Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.5 (Ubuntu 22.04)
- **Instance Type**: g5.2xlarge
- **Storage**: 200 GB gp3 (root volume)

### Security Group Configuration
Configure the following inbound rules:
- SSH (Port 22): Your IP
- Custom TCP (Port 8000): Your IP or Anywhere

## Installation

### 1. Create Setup Script
Create a file named `setup.sh` with the following content:

```bash
#!/bin/bash

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Clone your repository
git clone https://github.com/dhruv-pype/deepseek-server.git
cd deepseek-server

# Start the service
docker compose up -d
```

### 2. Connect and Deploy

1. Connect to your EC2 instance:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

3. Monitor the deployment:
```bash
docker compose logs -f
```

## Troubleshooting

If you encounter any issues:
1. Check Docker service status: `sudo systemctl status docker`
2. Verify NVIDIA drivers: `nvidia-smi`
3. Check container logs: `docker compose logs`

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE) - See the [LICENSE](LICENSE) file for details.