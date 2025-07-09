## Ansible

![ansible](https://github.com/user-attachments/assets/e266c548-f6e0-4313-bd1d-acab5f916ca8)

This project configures a development environment on three AWS virtual machines using Ansible, encompassing the installation of essential packages, Docker, and the deployment of an application container.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security](#security)
- [Note](#note)

## Project Structure

- `ansible.cfg`: Configuration file for Ansible.
- `hosts.ini`: Inventory file containing the AWS instances.
- `ansible.yaml`: Ansible playbook that defines the tasks to be executed on the AWS instances.
- `README.md`: Documentation of steps

## Prerequisites

### Control Machine Requirements

- **Operating System**: Linux, macOS, or Windows with WSL
- **Python**: 3.8 or higher
- **Ansible**: 2.12 or higher
- **SSH Key**: Access to AWS instances

### AWS Requirements

- **EC2 Instances**: Running Ubuntu 20.04 or higher
- **Security Groups**: Configured for SSH access (port 22)
- **IAM Roles**: Appropriate permissions for instance management
- **VPC Configuration**: Public and private subnets properly configured

### Network Requirements

- **Public Instances**: Direct internet access
- **Private Instances**: Access through jump hosts in public subnets
- **SSH Connectivity**: Verified connectivity to all instances

## Installation

### 1. Install Ansible

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible

# macOS
brew install ansible

# Using pip
pip install ansible
```

### 2. Clone the Repository

```bash
git clone https://github.com/MUSTAFA-3LI/DistriTask.git
cd DistriTask/Ansible
```

### 3. Configure SSH Access

```bash
# Set proper permissions for your SSH key
chmod 600 ~/.ssh/SSH_key

# Test SSH connectivity to public instances
ssh -i ~/.ssh/SSH_key ubuntu@<public-instance-ip>

# Test SSH connectivity to private instances through jump host
ssh -i ~/.ssh/SSH_key -o "ProxyJump ubuntu@<jump-host-ip>" ubuntu@<private-instance-ip>
```

## Configuration

### 1. Inventory Configuration

Configure your `hosts.ini` file with your AWS instance details, including public and private instances with appropriate SSH jump host configurations.

### 2. Secure Variables Configuration

Create an encrypted vault file for sensitive data:

```bash
# Create the vault file
ansible-vault create vault.yml
```

Add the following content to the vault file:

```yaml
vault_mysql_database: distritask
vault_mysql_user: your_secure_user
vault_mysql_password: your_secure_password
vault_mysql_root_password: your_secure_root_password
vault_db_host: db
vault_db_port: 3306
```

### 3. Docker Compose Configuration

The playbook uses different Docker Compose configurations for public and private instances:

- `docker-compose-public.yaml`: Configuration for public instances
- `docker-compose-private.yaml`: Configuration for private instances

## Usage

### Basic Deployment

```bash
# Run the playbook with vault password
ansible-playbook -i hosts.ini ansible.yaml --ask-vault-pass
```

### Advanced Usage

```bash
# Run with verbose output
ansible-playbook -i hosts.ini ansible.yaml --ask-vault-pass -vvv

# Run only on specific instances
ansible-playbook -i hosts.ini ansible.yaml --ask-vault-pass --limit public_instance_1_az1

# Run with custom vault password file
ansible-playbook -i hosts.ini ansible.yaml --vault-password-file ~/.vault_pass

# Check connectivity before deployment
ansible all -i hosts.ini -m ping
```

### Deployment Verification

```bash
# Check Docker containers status
ansible all -i hosts.ini -m shell -a "docker ps" --ask-vault-pass

# Check application logs
ansible all -i hosts.ini -m shell -a "docker logs distritask" --ask-vault-pass

# Verify application accessibility
ansible all -i hosts.ini -m uri -a "url=http://localhost:8000" --ask-vault-pass
```

## Security

### Best Practices Implemented

1. **Ansible Vault**: All sensitive data is encrypted
2. **SSH Key Management**: Proper permissions and key rotation
3. **Network Security**: Private instances accessible only through jump hosts
4. **File Permissions**: Restricted access to configuration files
5. **Docker Security**: Non-root user execution

### Security Considerations

- **Vault Password**: Store vault password securely, never commit to version control
- **SSH Keys**: Rotate SSH keys regularly
- **Network Access**: Limit access to jump hosts
- **Monitoring**: Implement logging and monitoring for security events

---

**Note**: This playbook is designed for educational and development purposes. For production deployments, additional security measures and testing should be implemented.

![img_13](https://github.com/user-attachments/assets/40d6b0e0-ad21-4c30-9aa6-c322b1010ad5)

then we can open our application from the DNS of AWS machines with port `8000`

![Image](https://github.com/user-attachments/assets/45bbb731-3854-478b-a536-d30b8b5e64a5)
