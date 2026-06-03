# 📝 2-Tier To-Do Application

A simple production-style 2-Tier To-Do Application built using **Flask** and **MySQL**. The application allows users to create, view, update, and delete tasks while demonstrating the architecture of a typical web application connected to a relational database.

---

## 🚀 Features

- Add new tasks
- View all tasks
- Delete tasks
- MySQL database integration
- Environment variable-based configuration
- Docker support
- Lightweight and easy to deploy

---

## 🏗️ Architecture

![Home Page](pics/2-tier-app.jpg)

---

This project follows a **2-Tier Architecture**:

1. Presentation & Business Logic Layer (Flask)
2. Data Layer (MySQL)

---

## 📂 Project Structure

```text
to-do-2-tier-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── index.html
└── README.md
```

## 🛠️ Tech Stack

- Python
- Flask
- MySQL
- HTML
- CSS
- Docker
- Docker Compose

---

## ⚙️ Environment Variables

Create a `.env` file or configure the following variables:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=todo_db
```

---

## 📦 Installation

### Clone Repository

```bash
git clone <repository-url>
cd to-do-2-tier-app
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Login to MySQL:

```sql
CREATE DATABASE todo_db;
```

Update your environment variables accordingly.

---

## ▶️ Run Application

```bash
python app.py
```

Application will be available at:

```text
http://localhost:5000
```
## Running the Application with Docker

### Step 1: Create a Docker Network

Create a custom Docker network so that the application container can communicate with the MySQL container.

```bash
docker network create todo-network
```

---

### Step 2: Start the MySQL Container

Run a MySQL 5.7 container with a dedicated database for the application.

```bash
docker run -d \
--name mysql \
-p 3306:3306 \
--network todo-network \
-e MYSQL_ROOT_PASSWORD=admin \
-e MYSQL_DATABASE=todo_db \
mysql:5.7
```

#### MySQL Configuration

| Parameter | Value |
|------------|--------|
| Container Name | mysql |
| Database Name | todo_db |
| Username | root |
| Password | admin |
| Port | 3306 |

---

### Step 3: Start the Todo Application Container

Run the Flask Todo application container and connect it to the same Docker network.

```bash
docker run -d \
--name todo-app \
-p 5000:5000 \
--network todo-network \
-e MYSQL_HOST=mysql \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=admin \
-e MYSQL_DB=todo_db \
todo-app:latest
```

#### Application Configuration

| Environment Variable | Value |
|---------------------|--------|
| MYSQL_HOST | mysql |
| MYSQL_USER | root |
| MYSQL_PASSWORD | admin |
| MYSQL_DB | todo_db |

---

### Step 4: Verify Running Containers

Check whether both containers are running successfully.

```bash
docker ps
```

Expected output:

```text
CONTAINER ID   IMAGE             STATUS
xxxxxxxxxxxx   mysql:5.7         Up
xxxxxxxxxxxx   todo-app:latest   Up
```

---

### Step 5: Access the Application

Open your browser and navigate to:

```text
http://localhost:5000
```

For AWS EC2:

```text
http://<EC2-PUBLIC-IP>:5000
```

Ensure that port **5000** is allowed in your EC2 Security Group.

---

### Useful Docker Commands

#### View Application Logs

```bash
docker logs todo-app
```

#### View MySQL Logs

```bash
docker logs mysql
```

#### Stop Containers

```bash
docker stop todo-app mysql
```

#### Remove Containers

```bash
docker rm -f todo-app mysql
```

#### Remove Network

```bash
docker network rm todo-network
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t todo-app .
```

### Run Container

```bash
docker run -p 5000:5000 todo-app
```

---

## 🐳 Docker Compose

Start application and database:

```bash
docker-compose up -d
```

Stop containers:

```bash
docker-compose down
```

## 🎯 Learning Objectives

This project demonstrates:

- Flask Web Development
- MySQL Integration
- CRUD Operations
- Environment Variable Management
- Docker Containerization
- 2-Tier Application Architecture

---

## 👨‍💻 Author

**Siddhesh Masurkar**

Data Scientist | Machine Learning Engineer | Python Developer
