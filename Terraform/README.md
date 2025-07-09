# Terraform AWS Configuration

![terraform](https://github.com/user-attachments/assets/25f7ffe6-2f75-46b7-a1ec-8a5ba2ca0016)

# AWS Infrastructure for DistriTask (Terraform)

This repository contains Terraform code to provision a secure, scalable AWS infrastructure for the DistriTask application. The architecture is designed for high availability, security, and operational monitoring.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Diagram](#diagram)
- [Getting Started](#getting-started)
- [Key Components](#key-components)
- [Monitoring & Alerts](#monitoring--alerts)
- [Teardown](#teardown)
- [Notes](#notes)

---

## **Architecture Overview**

- **Region:** us-east-1
- **VPC:** Custom VPC with public and private subnets across multiple Availability Zones
- **Subnets:**
  - Public subnets (for app servers, NAT gateways, load balancer)
  - Private subnets (for database and internal services)
- **Internet Gateway:** Allows public subnet access to the internet
- **NAT Gateway:** Allows private subnet instances to access the internet securely
- **Security Groups:**
  - Public: Allows HTTP, HTTPS, SSH, app ports
  - Private: Restricts access, allows DB and internal traffic
- **EC2 Instances:**
  - Public: Application servers
  - Private: Database servers with EBS volumes for data persistence
- **Load Balancer:** (Planned) For distributing traffic across public instances
- **CloudWatch:** Dashboards and alarms for monitoring CPU, health, and network
- **SNS:** Email alerts for critical events

---

## **Diagram**

<img width="1041" height="941" alt="Image" src="https://github.com/user-attachments/assets/d38f4208-86a2-4e42-b58f-fe9c7f9c06bc" />
---

## **Getting Started**

### **Prerequisites**

- [Terraform](https://www.terraform.io/downloads.html) >= 1.2.0
- AWS CLI configured with appropriate credentials
- SSH key pair for EC2 access

### **Setup Steps**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MUSTAFA-3LI/DistriTask.git
   cd DistriTask/Terraform/AWS
   ```

2. **Initialize Terraform**

   ```bash
   terraform init
   ```

3. **Review the Plan**

   ```bash
   terraform plan
   ```

4. **Apply the Configuration**

   ```bash
   terraform apply
   ```

   - Confirm with `yes` when prompted.

5. **Outputs**
   - After apply, Terraform will output public/private IPs for your EC2 instances.

---

## **Key Components**

- **VPC & Subnets:** Isolated network with public/private zones.
- **Internet Gateway & NAT Gateway:** Secure internet access for public and private resources.
- **Security Groups:** Fine-grained access control for each tier.
- **EC2 Instances:**
  - Public: Hosts application containers
  - Private: Hosts MySQL database with persistent EBS storage
- **CloudWatch:**
  - Dashboards for real-time monitoring
  - Alarms for CPU, health, and network usage
- **SNS:** Email notifications for alerts

---

## **Monitoring & Alerts**

- **CloudWatch Dashboard:** Visualizes CPU usage for all active instances.
- **Alarms:**
  - High CPU usage
  - Health check failures
  - High network traffic
- **SNS:** Sends email notifications for triggered alarms.

---

## **Teardown**

To destroy all resources when finished:

```bash
terraform destroy
```

---

## **Notes**

- **Sensitive Data:** No secrets are stored in the codebase. Use AWS Secrets Manager or SSM for production secrets.
- **Scaling:** The architecture is ready for horizontal scaling by adding more subnets/instances.
- **Extensibility:** Load balancer and multi-AZ support can be enabled by uncommenting and extending the provided resources.

---

**This setup is intended for educational and development purposes. For production, review and enhance security, backup, and compliance settings.**

![Image](https://github.com/user-attachments/assets/5569d319-49f4-4c36-a489-123deedf3d72)

After finishing from AWS machines

```bash
terraform destory
```
