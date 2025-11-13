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

## ☸️ Day 8 — Exposing the Flask API with Kubernetes Services

### Morning Session: Understanding Kubernetes Services

- **What is a Kubernetes Service?**
  - A stable network endpoint that provides access to a set of pods.
  - Solves the problem of pods having dynamic, changing IP addresses.
  - Acts as a load balancer, distributing traffic across multiple pod replicas.

- **Why Services are Necessary:**
  - **Pods are ephemeral** → They can be deleted, recreated, and get new IP addresses.
  - **Services provide stability** → A single, unchanging endpoint regardless of pod changes.
  - **Built-in load balancing** → Automatically distributes requests across healthy pods.

- **Service Types:**
  - **ClusterIP** (default) → Only accessible within the cluster.
  - **NodePort** → Exposes the service on each node's IP at a static port (30000-32767).
  - **LoadBalancer** → Creates an external load balancer (requires cloud provider).

- **How Services Find Pods:**
  - Services use **selectors** to match pod labels (e.g., `app=flask-api`).
  - The selector must match the labels defined in the Deployment.
  - Services automatically update their endpoint list as pods are created/destroyed.

### Afternoon Session: Creating and Deploying the Service

- Created a **service.yaml** file in the `k8s/` directory:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-api-service
spec:
  type: NodePort
  selector:
    app: flask-api
  ports:
    - protocol: TCP
      port: 5000        # Service port (internal cluster access)
      targetPort: 5000  # Container port where Flask is listening
      # nodePort is auto-assigned (30000-32767 range)
```

- Applied the Service to Kubernetes:

```powershell
kubectl apply -f k8s/flask-api-service.yaml
```

- Verified the Service was created successfully:

```powershell
kubectl get services
kubectl describe service flask-api-service
```

### Understanding the Network Path

The complete request flow:

```
Browser/curl (http://127.0.0.1:55520)
    ↓
Minikube tunnel (port forwarding)
    ↓
Minikube VM NodePort (192.168.49.2:30817)
    ↓
Kubernetes Service (flask-api-service)
    ↓
Load balances to one of 3 pods:
    - Pod 1: 10.244.0.6:5000
    - Pod 2: 10.244.0.7:5000
    - Pod 3: 10.244.0.8:5000
    ↓
Flask application responds
```

### Accessing the Service

**On Windows/macOS with Minikube:**
- Direct access to the Minikube VM IP doesn't work because Minikube runs in a VM.
- Solution: Use Minikube's tunnel feature:

```powershell
minikube service flask-api-service
```

This command:
1. Creates a tunnel from localhost to the Minikube VM
2. Provides a localhost URL (e.g., `http://127.0.0.1:55520`)
3. Must remain running in the terminal while accessing the service

**Alternative Access Method:**

```powershell
# Port-forward directly to the service
kubectl port-forward service/flask-api-service 5000:5000

# Then access at:
curl http://localhost:5000/hello
```

### Verifying Load Balancing

- **Challenge:** Initially couldn't see which pod was handling requests.
- **Root Cause:** Flask logs showed requests coming from `10.244.0.1` (the Kubernetes node) due to Network Address Translation (NAT).

**Solution: Add Pod Identification to Flask Responses**

Modified `app.py` to include pod information:

```python
from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

def pod_data(data):
    """Helper function to add pod identification to responses"""
    return {
        **data,
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        "pod_ip": socket.gethostbyname(socket.gethostname())
    }

@app.route('/hello')
def hello():
    return jsonify({
        "message": "Hello from Flask, Yessir!",
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        "pod_ip": socket.gethostbyname(socket.gethostname())
    })

@app.route('/data')
def data():
    fake_db = {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "moderator"}
        ]
    }
    return jsonify(pod_data(fake_db))
```

### Updating the Application in Kubernetes

Learned the complete workflow for updating code in Kubernetes:

```powershell
# 1. Edit the application code (app.py)

# 2. Rebuild the Docker image
docker build -t flask-api:latest . --no-cache

# 3. Load the new image into Minikube
minikube image load flask-api:latest

# 4. Force pods to restart with the new image
kubectl delete pods -l app=flask-api

# 5. Verify pods are running with new code
kubectl get pods -w
```

### Troubleshooting: Image Caching Issues

**Problem:** After rebuilding the Docker image, pods were still running old code.

**Root Cause:** Minikube cached the old image even after loading a new one with the same tag.

**Investigation Steps:**

1. Verified local Docker image was correct by testing directly:

```powershell
docker run -d --name flask-test -p 5001:5000 flask-api:latest
curl http://localhost:5001/hello  # ✅ Showed pod info correctly
```

2. Checked what was actually running in Kubernetes pods:

```powershell
kubectl exec -it <pod-name> -- cat /app/backend/app.py
# Showed old code without pod identification
```

3. Checked image timestamp in Minikube:

```powershell
minikube ssh "docker images | grep flask-api"
# Showed "25 hours ago" instead of recent build time
```

**Solution: Force Image Cache Clearing**

```powershell
# Scale deployment to 0 to remove all pods
kubectl scale deployment flask-api-deployment --replicas=0

# Force remove the old cached image
minikube ssh "docker rmi -f flask-api:latest"

# Load the fresh image
minikube image load flask-api:latest

# Verify it's the new image (check timestamp)
minikube ssh "docker images | grep flask-api"

# Scale back up
kubectl scale deployment flask-api-deployment --replicas=3
```

### Testing Load Balancing in Action

With pod identification working, verified load balancing:

```powershell
# Make multiple requests and see different pods responding
1..10 | ForEach-Object {
    $response = (curl http://127.0.0.1:55520/hello).Content | ConvertFrom-Json
    Write-Host "Request $_ served by: $($response.pod_name)"
}
```

**Example Output:**

```
Request 1 served by: flask-api-deployment-c4b9676c9-8qw5g
Request 2 served by: flask-api-deployment-c4b9676c9-hslxp
Request 3 served by: flask-api-deployment-c4b9676c9-vgkkp
Request 4 served by: flask-api-deployment-c4b9676c9-8qw5g
...
```

This confirmed that Kubernetes was successfully distributing requests across all 3 pod replicas.

### Key Learnings: Network Address Translation (NAT)

- **IP Addresses in Kubernetes:**
  - Pod IPs (e.g., `10.244.0.6-8`) → Where containers actually run
  - Node IP (e.g., `10.244.0.1`) → Minikube node's network interface
  - Service IP (e.g., `10.96.218.213`) → Virtual IP for the service

- **Why Flask logs show `10.244.0.1`:**
  - Kubernetes performs NAT when routing through services
  - From Flask's perspective, requests appear to come from the node
  - This is normal Kubernetes behavior, not an error

- **Better way to track requests:**
  - Include pod identification in application responses
  - Use structured logging with pod metadata
  - Use `kubectl logs --prefix` to see which pod produced each log line

### Key Achievements

✅ Created and deployed a Kubernetes Service with NodePort  
✅ Successfully exposed Flask API externally via Minikube tunnel  
✅ Understood the complete network request flow in Kubernetes  
✅ Added pod identification to API responses for visibility  
✅ Verified load balancing across multiple pod replicas  
✅ Learned to troubleshoot and resolve Docker image caching issues  
✅ Mastered the workflow for updating applications in Kubernetes  

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| 404 errors when accessing service | Minikube tunnel was needed for Windows; used `minikube service` command |
| Couldn't see load balancing | Added pod name and IP to API responses using `os.environ` and `socket` |
| Updated code not appearing in pods | Cleared Minikube's image cache and forced pod recreation |
| Confusion about source IP `10.244.0.1` | Learned this is normal NAT behavior in Kubernetes networking |

### Commands Reference

**Service Management:**

```powershell
# Create service
kubectl apply -f k8s/flask-api-service.yaml

# View services
kubectl get services
kubectl get svc  # shorthand

# Detailed service info
kubectl describe service flask-api-service

# Access service (Minikube)
minikube service flask-api-service

# Port forwarding
kubectl port-forward service/flask-api-service 5000:5000
```

**Debugging:**

```powershell
# Check pod logs with pod names
kubectl logs -l app=flask-api --tail=20 --prefix

# Execute commands in pod
kubectl exec -it <pod-name> -- cat /app/backend/app.py

# Check image in Minikube
minikube ssh "docker images | grep flask-api"
```

**Updating Application:**

```powershell
# Complete update workflow
docker build -t flask-api:latest . --no-cache
minikube image load flask-api:latest
kubectl scale deployment flask-api-deployment --replicas=0
minikube ssh "docker rmi -f flask-api:latest"
minikube image load flask-api:latest
kubectl scale deployment flask-api-deployment --replicas=3
```

---

## 💡 Reflection

Day 8 was crucial for understanding how Kubernetes exposes applications to the outside world. The journey from 404 errors to successfully seeing load balancing in action taught me:

- **Services are essential** → They provide stable endpoints for dynamic pods
- **Minikube networking is different** → Requires tunnels or port-forwarding on Windows/macOS
- **Observability matters** → Adding pod identification made debugging and verification much easier
- **Image caching can be tricky** → Always verify pods are using the latest image
- **Patience in debugging pays off** → Systematic troubleshooting revealed the root cause

The Flask API is now fully accessible, load-balanced across 3 replicas, and ready for Day 9's scaling and resilience testing.

---

**Next Steps:**
- **Day 9:** Test Kubernetes' resilience by scaling deployments and killing pods
- **Day 10:** Complete documentation with screenshots and polish the README
- **Day 11:** Optional enhancements (ConfigMaps, Secrets, or frontend)

---