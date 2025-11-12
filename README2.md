# Docker & Kubernetes — Days 1 to 7

This document summarizes what I learned over the first seven days of working with **Docker** and **Kubernetes**. The goal was to understand how to containerize a simple Flask application and run it consistently across different environments, then deploy it to Kubernetes for orchestration.

---

## 🗓️ Day 1 — Setting Up and Virtual Environments

- Learned how to create and activate a **Python virtual environment** using `venv`.
- Understood why virtual environments are important — they isolate project dependencies.
- Installed required packages using a `requirements.txt` file.
- Learned about PowerShell's **execution policy** issue and how to fix it by adjusting permissions.
- Practiced basic terminal commands to navigate directories, activate environments, and install dependencies.

---

## 🐳 Day 2 — Understanding Docker Basics

- Learned what **Docker** is and how it allows apps to run in isolated, consistent environments.
- Understood the difference between:
  - **Images** → Blueprints that define what a container includes.
  - **Containers** → Running instances of those images.
- Wrote a basic **Dockerfile** to containerize a Flask app.
- Learned and practiced key Docker commands:
  - `docker build` → Builds an image from a Dockerfile.
  - `docker run` → Runs a container from an image.
  - `docker ps` → Lists running containers.
  - `docker exec` → Opens a shell inside a running container.
- Learned about `requirements.txt` and how to generate it using `pip freeze` from a virtual environment.

---

## ⚙️ Day 3 — Docker Compose and Multi-Service Setup

- Discovered **Docker Compose**, a tool for managing multiple containers at once.
- Learned how to define services, ports, and environment variables in a `docker-compose.yml` file.
- Understood key sections of a Compose file:
  - `build` → Points to where the Dockerfile is located.
  - `ports` → Maps container ports to host machine ports.
  - `volumes` → Syncs local code with the container for live updates.
  - `environment` → Sets configuration variables inside containers.
- Ran multiple services together using a single command:
```bash
  docker-compose up
```
- Learned how containers can communicate using their service names defined in the Compose file.

---

## 🧩 Day 4 — Debugging and Testing the Flask API

- Learned how to access a running container using:
```bash
  docker exec -it  bash
```
- Practiced checking active processes with `ps aux` and installed missing utilities when needed.
- Debugged a **404 Not Found** error and realized the Flask app was running correctly, but no route was defined for `/`.
- Confirmed that the Flask application was now fully running **inside a container**, not directly on the host machine.
- Strengthened understanding of what it means to **dockerize** an application — isolating it, packaging it, and running it anywhere consistently.

---

## 📦 Day 5 — GitHub Setup and Version Control

- Initialized a **Git repository** in the project directory.
- Learned essential Git commands:
  - `git init` → Initialize a new repository.
  - `git add .` → Stage all changes for commit.
  - `git commit -m "message"` → Save changes with a descriptive message.
  - `git remote add origin <url>` → Connect local repo to GitHub.
  - `git push -u origin main` → Push code to GitHub.
- Created a **GitHub repository** to host the project remotely.
- Pushed the Dockerized Flask application, including:
  - Backend code (`app.py`)
  - `Dockerfile`
  - `docker-compose.yml`
  - `requirements.txt`
  - Initial `README.md`
- Understood the importance of **version control** for tracking changes, collaboration, and portfolio building.
- Learned best practices for commit messages (clear, concise, descriptive).

---

## ☸️ Day 6 — Introduction to Kubernetes

- Installed and set up **Kubernetes** using **Docker Desktop Kubernetes**.
- Verified Kubernetes installation with:
```bash
  kubectl cluster-info
  kubectl get nodes
```
- Learned fundamental Kubernetes concepts:
  - **Pods** → The smallest deployable unit; wraps one or more containers.
  - **Nodes** → Physical or virtual machines that run pods.
  - **Cluster** → A set of nodes managed by Kubernetes.
  - **kubectl** → Command-line tool for interacting with Kubernetes.
- Ran a test pod to understand basic Kubernetes operations:
```bash
  kubectl run test-pod --image=nginx
  kubectl get pods
  kubectl describe pod test-pod
  kubectl delete pod test-pod
```
- Understood the difference between **Docker** (container runtime) and **Kubernetes** (container orchestration).
- Learned why Kubernetes is used:
  - Automatic scaling
  - Self-healing (automatic pod restart)
  - Load balancing
  - Rolling updates with zero downtime

---

## 🚀 Day 7 — Creating a Kubernetes Deployment

### Morning Session: Learning Kubernetes Deployment Concepts

- **What is a Deployment?**
  - A Kubernetes controller that manages **ReplicaSets** and ensures the desired number of pods are always running.
  - Provides automatic recovery, scaling, and rolling updates.
  
- **Deployments vs Running Pods Directly:**
  - Direct pods have no self-healing; if they crash, they stay dead.
  - Deployments automatically recreate crashed pods and enable zero-downtime updates.

- **Understanding Replicas:**
  - **Replicas** are identical copies of your application running simultaneously.
  - Benefits:
    - **High availability** → If one pod crashes, others continue serving requests.
    - **Load balancing** → Traffic is distributed across multiple pods.
    - **Zero-downtime updates** → New versions are rolled out gradually.
    - **Scalability** → Easily increase/decrease replicas based on demand.

- **Labels and Selectors:**
  - **Labels** are key-value tags attached to Kubernetes objects (e.g., `app=flask-api`).
  - **Selectors** are queries that find objects with specific labels.
  - Deployments use selectors to identify and manage their pods.
  - Services use selectors to route traffic to the correct pods.

### Afternoon Session: Building the Kubernetes Deployment

- Created a `k8s/` directory to organize Kubernetes configuration files.
- Wrote a **deployment.yaml** file:
```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: flask-api-deployment
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: flask-api
    template:
      metadata:
        labels:
          app: flask-api
      spec:
        containers:
        - name: flask-api
          image: flask-api:latest
          imagePullPolicy: Never
          ports:
          - containerPort: 5000
```
- Applied the deployment to Kubernetes:
```bash
  kubectl apply -f k8s/deployment.yaml
```
- Verified pods were created and running:
```bash
  kubectl get pods
  kubectl get deployments
  kubectl describe deployment flask-api-deployment
```
- Learned key kubectl commands:
  - `kubectl get pods -o wide` → Shows detailed pod information including node placement.
  - `kubectl logs <pod-name>` → Views logs from a specific pod.
  - `kubectl describe pod <pod-name>` → Shows detailed pod configuration and events.
  - `kubectl port-forward <pod-name> 5000:5000` → Forwards local traffic to a pod for testing.

- **Tested the Flask API** running inside Kubernetes pods using port forwarding.
- Understood that pods are ephemeral and the deployment maintains the desired state automatically.
- Observed Kubernetes' **self-healing** behavior by deleting a pod and watching it automatically recreate.

### Key Achievements:
✅ Flask API successfully running as 2 replicas in Kubernetes  
✅ Understanding of how Deployments manage pods using ReplicaSets  
✅ Hands-on experience with kubectl commands  
✅ Verified automatic pod recovery (self-healing)  

### Challenges & Solutions:
- **Challenge:** Pods stuck in `ImagePullBackOff` status.
  - **Solution:** Added `imagePullPolicy: Never` since the Docker image is local, not in a registry.
- **Challenge:** Couldn't access Flask API initially.
  - **Solution:** Used `kubectl port-forward` for testing (Service creation is planned for Day 8).

---

## 💡 Reflection

By the end of Day 7, I had successfully transitioned from running a containerized Flask application in Docker to orchestrating it with Kubernetes. I now understand:

- How **Deployments** provide production-grade reliability through automatic scaling and self-healing.
- Why **multiple replicas** are essential for high availability and load balancing.
- How **labels and selectors** enable Kubernetes to manage complex applications.
- The difference between working with individual containers (Docker) vs. orchestrating many containers (Kubernetes).

The Flask API is now running in a resilient, scalable environment managed by Kubernetes. Next steps include exposing the application through a Kubernetes Service and testing external access.

---

**Next Steps:**
- **Day 8:** Create a Kubernetes Service to expose the Flask API using NodePort.
- **Day 9:** Explore scaling and resilience by manually scaling deployments and observing pod recreation.
- **Day 10:** Complete documentation with screenshots and polish the README.

---

**Author:** Rehan  
**Project:** KreptKon Flask API  
**Duration:** Days 1–7 of Docker & Kubernetes Learning Journey
