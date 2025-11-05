# Docker & Kubernetes — Days 1 to 4

This document summarizes what I learned over the first four days of working with **Docker** and **Kubernetes**. The goal was to understand how to containerize a simple Flask application and run it consistently across different environments.

---

## 🗓️ Day 1 — Setting Up and Virtual Environments

- Learned how to create and activate a **Python virtual environment** using `venv`.
- Understood why virtual environments are important — they isolate project dependencies.
- Installed required packages using a `requirements.txt` file.
- Learned about PowerShell’s **execution policy** issue and how to fix it by adjusting permissions.
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
  docker exec -it <container_name> bash
  ```
- Practiced checking active processes with `ps aux` and installed missing utilities when needed.
- Debugged a **404 Not Found** error and realized the Flask app was running correctly, but no route was defined for `/`.
- Confirmed that the Flask application was now fully running **inside a container**, not directly on the host machine.
- Strengthened understanding of what it means to **dockerize** an application — isolating it, packaging it, and running it anywhere consistently.

---

## 💡 Reflection

By the end of Day 4, I understood how Docker makes development environments reproducible and portable.  
I learned how to:
- Build and run Docker images and containers.
- Manage multi-service environments with Docker Compose.
- Debug and interact with containers directly.
- Identify and resolve basic app and environment issues.

Next steps: connect the Flask API to a database container and start learning **Kubernetes** for container orchestration.

---

**Author:** Rehan  
**Project:** KreptKon Flask API  
**Duration:** Days 1–4 of Docker & Kubernetes Learning Journey
