## 🚀 Project Features & Skills

![Docker](https://img.shields.io/badge/Dockerization-Built%20images%20&%20Compose-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20Workflows-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Local%20Clusters%20Deployment-blueviolet)
![Terraform](https://img.shields.io/badge/Infra%20as%20Code-Terraform%20%26%20AWS-green)
![Security](https://img.shields.io/badge/Security-IAM%20%26%20Best%20Practices-red)
![Backup](https://img.shields.io/badge/Backup%20&%20Recovery-AWS%20EBS%20%26%20Disaster%20Recovery-yellow)
![Monitoring](https://img.shields.io/badge/Monitoring-CloudWatch%20%26%20Alerts-lightgrey)

# DistriTask

A comprehensive web-based task management system designed to streamline organizational workflow and enhance team collaboration. DistriTask supports two distinct user roles: Manager and Employee, with advanced features including real-time chat, AI chatbot assistance, and secure API authentication.

<img width="1903" height="915" alt="Image" src="https://github.com/user-attachments/assets/3ab8a439-69f7-4891-9129-9c648f715426" />

## Table of Contents

- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Development & Testing](#development--testing)
- [Core Features](#core-features)
- [API Overview](#api-overview)
- [DevOps & Cloud Infrastructure](#devops--cloud-infrastructure)

## Key Features

- **Secure Authentication**: Role-based access for Managers and Employees
- **Intelligent Task Assignment**: Automatic task distribution based on workload
- **Real-Time Chat**: Instant messaging with WebSocket support
- **AI-Powered Chatbot**: Natural language interaction for task queries and automation
- **Comprehensive Analytics**: Dashboards for task completion and performance tracking
- **Mobile-Responsive Design**: Seamless experience across devices

## Technologies Used

### Backend

- **Python 3.x**
- **Django 4.x**
- **Django REST Framework**
- **Django Channels** (WebSockets)
- **Celery** (Task Queue)
- **Redis** (Message Broker & Cache)

### Database

- **MySQL** or **SQLite**

### Authentication

- **Django's built-in authentication**
- **Token authentication** for API access

### Testing

- **pytest**
- **Django test framework**

### Frontend

- **HTML5**
- **CSS3**
- **JavaScript**
- **Font Awesome (icon library )**
- **SweetAlert2 (Alert message library)**

### DevOps & Cloud

- **Docker & Docker Compose** – For containerization and managing multi-service environments

- **GitHub Actions** – For building automated CI/CD pipelines

- **Terraform** – Infrastructure as Code (IaC) to provision cloud resources

- **AWS EC2, EBS, IAM, Shield** – Cloud compute, storage, security roles, and DDoS protection

- **Ansible** – For automated server configuration and environment setup

- **Kubernetes** – For container orchestration and deployment testing in local clusters

- **AWS CloudWatch** – For monitoring, alerting, and performance dashboards

## Installation

Follow these steps to set up and run DistriTask locally:

### 1. Clone the repository

```bash
git clone https://github.com/MUSTAFA-3LI/DistriTask
cd DistriTask
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure settings

Update `TaskManager/settings.py` with:

- Database settings (SQLite or MySQL)
- Email backend credentials
- Redis settings for Celery and Channels
- Static and media file configurations

### 5. Set up database

```bash
python3 manage.py migrate
```

### 6. Create superuser

```bash
python3 manage.py createsuperuser
```

## Development & Testing

Before starting the server, ensure all tests pass to maintain code quality.

### Running Tests

```bash
python3 manage.py test
# or
pytest
```

> **Test Coverage**: The project includes comprehensive test coverage for all core functionalities.

![Image](https://github.com/user-attachments/assets/2b0e842f-2a02-4c6d-805f-8c873a1c566a)

### Starting Services

Now, you can start the necessary services and the development server:

#### 1. Start Redis server (for Celery and Channels)

```bash
redis-server
```

#### 2. Start Celery worker (in a new terminal)

```bash
celery -A TaskManager worker -l info
```

#### 3. Start development server

```bash
python3 manage.py runserver
```

## Core Features

### Authentication & User Management

DistriTask features a robust authentication system allowing users to securely log in and manage their accounts. It supports a custom user model with email-based login, password reset functionality via OTP, and comprehensive role-based access control for Managers and Employees.

**Features:**

- **Custom User Model**: Email login and secure password management
- **Role-Based Access Control**: Distinct permissions for Managers and Employees
- **Session-Based Login/Logout**: Standard web session management
- **Token-Based API Authentication**: Secure access for all API interactions
- **Password Reset**: Via OTP sent to the registered email
- **CSRF Protection**: Enhanced security against cross-site request forgeries
- **Automated Deployment: Docker, CI/CD, AWS provisioning**

<img width="1919" height="915" alt="Image" src="https://github.com/user-attachments/assets/82ed96bd-b407-4214-9663-7e871d36d01f" />
<img width="1917" height="925" alt="Image" src="https://github.com/user-attachments/assets/e2c9ce14-72da-4720-81a0-2f0fd29f41cd" />
### Intelligent Task Management (Manager View)

Managers have full control over task creation, assignment, and monitoring. The system incorporates an intelligent algorithm that automatically assigns tasks to employees based on workload balancing and specific categories, ensuring optimal distribution and efficiency.

**Features:**

- **Task Creation, Editing, Deletion**: Full CRUD operations for tasks
- **Automatic Assignment**: Tasks are intelligently assigned to the employee with the least uncompleted tasks within a given category
- **Task Status Tracking**: Monitor tasks as pending or completed
- **Categories & Deadlines**: Organize tasks with categories and strict deadlines
- **Filtering & Searching**: Easily view tasks by status, assigned employee, or category
- **Task ID Lookup**: Quickly find tasks by their title

<img width="1909" height="921" alt="Image" src="https://github.com/user-attachments/assets/1ab329e7-76d4-4472-a218-8c7ab89f87f9" />
<img width="1907" height="921" alt="Image" src="https://github.com/user-attachments/assets/3f9c553d-67b5-45cd-847e-9ef2c6d486df" />
### Employee Task View

Employees are provided with a streamlined interface to view only the tasks assigned to them. They can track the status of their tasks, mark them as completed, and manage their workload effectively within the given deadlines.

**Features:**

- **Personalized Task List**: Employees only see tasks assigned specifically to them
- **Task Status Updates**: Ability to mark tasks as completed
- **Deadline Awareness**: Clear visibility of task deadlines

<img width="1920" height="920" alt="Image" src="https://github.com/user-attachments/assets/89676c4f-6f7f-461f-9d2c-0c997f80398a" />
### Real-Time Communication

DistriTask integrates a WebSocket-based chat system using Django Channels, enabling seamless real-time communication between team members.

**Features:**

- **WebSocket-Based Chat**: Powered by Django Channels for instant messaging
- **Team Collaboration**: Dedicated chat rooms for different teams or projects
- **Message History**: Access to past conversations for continuity
- **Read Status Tracking**: Know when your messages have been seen

<img width="1919" height="925" alt="Image" src="https://github.com/user-attachments/assets/93f093f8-b7ba-47f3-b029-a3268f82088f" />
### AI Chatbot Assistant

An intelligent chatbot assistant powered by natural language processing provides instant support for task-related queries and automates common operations.

**Features:**

- **Natural Language Processing**: Understands and responds to natural language queries
- **Task-Related Queries**: Get instant answers on task statuses, deadlines, and details
- **Quick Actions**: Perform common operations like task reassignment or status updates
- **Multi-Step Interactions**: Supports complex operations requiring multiple conversational turns
- **Performance Analytics**: Retrieve statistics on task completion rates, employee performance, and more

<img width="1905" height="915" alt="Image" src="https://github.com/user-attachments/assets/7739e01a-ce94-4f07-b4f9-798e5f0e8428" />
##  API Overview

### Chatbot API Endpoints (Token Authentication Required)

| Endpoint                       | Method | Description                         |
| ------------------------------ | ------ | ----------------------------------- |
| `/chatbot/total-tasks/`        | GET    | Get total task count                |
| `/chatbot/completed-tasks/`    | GET    | Get completed tasks statistics      |
| `/chatbot/delayed-tasks/`      | GET    | Get delayed tasks information       |
| `/chatbot/overdue-tasks/`      | GET    | Get overdue tasks list              |
| `/chatbot/top-employees/`      | GET    | Get top performing employees        |
| `/chatbot/completion-rate/`    | GET    | Get overall completion rate         |
| `/chatbot/tasks-due-on/`       | GET    | Get tasks due on specific date      |
| `/chatbot/tasks-per-category/` | GET    | Get tasks by category               |
| `/chatbot/tasks-for-user/`     | GET    | Get tasks assigned to specific user |
| `/chatbot/user-info/`          | GET    | Get user information                |
| `/chatbot/task-id/`            | GET    | Get task ID by title                |
| `/chatbot/reassign-task/`      | POST   | Reassign task to different user     |

### General API Endpoints

DistriTask provides a comprehensive set of RESTful API endpoints built with Django REST Framework, ensuring secure and efficient data exchange for all functionalities. All API endpoints are protected with token authentication and CSRF protection.

| Endpoint                   | Method | Description               |
| -------------------------- | ------ | ------------------------- |
| `/chatbot/api-token-auth/` | POST   | Get API token for chatbot |

## DevOps & Cloud Infrastructure

This project includes a complete setup for automated deployment, infrastructure management, and operational reliability.

**Dockerization**

- Built project images for isolated, reproducible deployments.

- Used Docker Compose to orchestrate multiple containers on the same network.

- Containerized Django backend for portable, consistent deployment environments.

**CI/CD Pipelines**

- Created automated GitHub Actions workflows for testing, building, and deploying on every push.

- Built new Docker images and pushed them to Docker Hub.

- Included team notifications for build failures or deployment status.

**Kubernetes Deployment**

- Deployed Dockerized application to local Kubernetes clusters for orchestration testing.

- Managed container scaling, rolling updates, and rollbacks.

**Infrastructure Provisioning (Terraform & AWS)**

- Defined infrastructure as code to provision consistent AWS environments.

- Automated deployment of highly available infrastructure on AWS EC2.

- Managed networking, security groups, and IAM roles with Terraform.

**Security & IAM**

- Configured AWS Security Groups for subnet-level access control.

- Created IAM roles and policies to enforce least-privilege access.

- Used AWS Shield for DDoS protection.

- Secured SSH access and sensitive credentials following best practices.

**Backup & Recovery**

- Used AWS EBS volumes for persistent data storage.

- Configured multi-AZ backups for high availability.

- Automated backup schedules and disaster recovery strategies.

**Monitoring & Logging**

- Integrated AWS CloudWatch for metrics and logs.

- Set up email alerts (e.g., Gmail) for critical events.

- Created dashboards to monitor system health and performance.
