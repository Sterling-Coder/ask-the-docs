# AWS EC2 Deployment Guide for "Ask the Docs"

This guide outlines the steps to deploy your Dockerized Streamlit application to an AWS EC2 instance (Free Tier).

## Prerequisites
- An AWS Account.
- Your OpenAI API Key.

## Step 1: Launch an EC2 Instance

1.  **Login** to the AWS Management Console.
2.  Navigate to **EC2** Dashboard.
3.  Click **Launch Instances**.
4.  **Name**: "AskTheDocs-Server".
5.  **AMI (OS)**: Select **Ubuntu Server 24.04 LTS** (Free tier eligible).
6.  **Instance Type**: Select **t2.micro** or **t3.micro** (Free tier eligible).
7.  **Key Pair**:
    - Click **Create new key pair**.
    - Name: `ask-the-docs-key`.
    - Type: `RSA`.
    - Format: `.pem`.
    - **Download** the file and keep it safe (e.g., in `~/.ssh/`).
8.  **Network Settings (Security Group)**:
    - Method: "Create security group".
    - Allow SSH traffic from "Anywhere" (0.0.0.0/0) or "My IP".
    - **IMPORTANT**: Click "Edit" (or "Add security group rule") to open the Streamlit port:
        - Type: **Custom TCP**
        - Port range: **8501**
        - Source: **Anywhere** (0.0.0.0/0)
    - (Optional) Allow HTTP (80) and HTTPS (443) if you plan to set up a domain later.
9.  Click **Launch Instance**.

## Step 2: Connect to the Instance

1.  Open your local terminal.
2.  Locate your downloaded key (e.g., `~/Downloads/ask-the-docs-key.pem`).
3.  Change permission:
    ```bash
    chmod 400 ~/Downloads/ask-the-docs-key.pem
    ```
4.  **Connect via SSH**:
    *Replace `<PUBLIC-IP>` with your EC2 IP (e.g., `51.21.161.9`).*

    **If using Amazon Linux (Default):**
    ```bash
    ssh -i ~/Downloads/ask-the-docs-key.pem ec2-user@<PUBLIC-IP>
    ```

    **If using Ubuntu:**
    ```bash
    ssh -i ~/Downloads/ask-the-docs-key.pem ubuntu@<PUBLIC-IP>
    ```

## Step 3: Set up the Server

Once connected, run the commands for your OS:

### Option A: Amazon Linux (Likely what you have)
```bash
# 1. Update system
sudo yum update -y

# 2. Install Docker
sudo yum install docker -y

# 3. Start Docker
sudo service docker start

# 4. Add user to docker group (fixes permission issues)
sudo usermod -a -G docker ec2-user
```
*After Step 4, type `exit` to disconnect, then SSH back in to apply changes.*

### Option B: Ubuntu
```bash
# 1. Update
sudo apt-get update

# 2. Install Docker
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# 3. Permissions
sudo usermod -aG docker $USER
```
*After Step 3, type `exit`, then SSH back in.*

## Step 4: Deploy the Application

1.  **Clone your code** (or copy it):
    *Option A: Git Clone (Easiest if your code is on GitHub)*
    ```bash
    git clone https://github.com/Sterling-Coder/ask-the-docs.git
    cd ask-the-docs
    ```
    *Option B: SCP (Copy local files if not using Git)*
    *(Run this from your **LOCAL** machine, not the server)*
    ```bash
    scp -i ~/Downloads/ask-the-docs-key.pem -r /path/to/local/project ubuntu@<PUBLIC-IP>:~/ask-the-docs
    ```

2.  **Create the Environment File**:
    Inside the project folder on the server:
    ```bash
    nano .env
    ```
    Paste your API key:
    ```
    OPENAI_API_KEY=sk-proj-...
    ```
    Press `Ctrl+O`, `Enter` to save, and `Ctrl+X` to exit.

3.  **Build the Docker Image**:
    ```bash
    docker build -t ask-the-docs .
    ```

4.  **Run the Container**:
    Run in "detached" mode (`-d`) so it keeps running after you disconnect.
    ```bash
    docker run -d -p 8501:8501 --env-file .env --restart always --name rag-app ask-the-docs
    ```

## Step 5: Access the App

1.  Open your browser.
2.  Visit: `http://<EC2-PUBLIC-IP>:8501`
3.  You should see your "Ask the Docs" app running!

http://51.21.161.9:8501

## Troubleshooting

- **Site can't be reached?**
  - Check your AWS **Security Group** settings to ensure Port **8501** is open to 0.0.0.0/0.
- **App crashes?**
  - Check logs: `docker logs rag-app`
