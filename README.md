# KreptKon - Docker & Kubernetes Learning Project

Learning Docker and Kubernetes by building and deploying a Flask API. This project follows a 14-day roadmap to go from basic Flask to a fully orchestrated Kubernetes deployment.

## What Is It?

A simple Flask API that I've containerised with Docker and deployed to Kubernetes (using Minikube). The app runs across multiple pods with load balancing, and I've added ConfigMaps and Secrets for configuration management.

**Stack:**
- Python 3.11 + Flask
- Docker
- Kubernetes (Minikube)
- ConfigMaps & Secrets

---

## Quick Start

### Prerequisites
- Python 3.11+
- Docker Desktop or Minikube
- kubectl CLI

## Running Locally

```bash
git clone <your-repo-url>
cd KreptKon/backend

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install and run
pip3 install -r requirements.txt
python3 app.py
```

Access at http://localhost:5000

## Running with Docker

```bash
cd backend
docker build -t flask-api:latest .
docker run -p 5000:5000 flask-api:latest
```

## Running on Kubernetes

```bash
# Start Minikube
minikube start

# Build image in Minikube
eval $(minikube docker-env)
cd backend
docker build -t flask-api:latest .

# Deploy everything
cd ..
kubectl apply -f k8s/flask-configmap.yaml
kubectl apply -f k8s/flask-secret.yaml
kubectl apply -f k8s/flask-api-deployment-updated.yml
kubectl apply -f k8s/flask-api-service.yml

# Get the URL
minikube service flask-api-service --url
```

## API Endpoints

- `/hello` - Basic greeting with pod info
- `/status` - API status and config
- `/config` - Shows all configuration values
- `/data` - Sample user data
- `/user/<id>` - Get specific user

## What I Did/Learned

**Day 1-2: Project Setup**
- Created Flask API with multiple endpoints
- Set up Python virtual environment
- Installed dependencies and created requirements.txt

**Day 3-4: Dockerisation**
- Wrote Dockerfile to containerise the Flask app
- Built and ran Docker containers
- Debugged containerised application
- Learned Docker commands: `build`, `run`, `ps`, `exec`

**Day 5: Version Control**
- Initialised Git repository
- Created GitHub repository and pushed code
- Learned Git workflow: `init`, `add`, `commit`, `push`

---



**Day 6: Kubernetes Introduction**
- Installed Minikube
- Learned core concepts: Pods, Nodes, Clusters
- Ran test pods to understand basic operations
- Understood why Kubernetes is needed: scaling, self-healing, load balancing

**Day 7: Deployments**
- Created Kubernetes Deployment with 2 replicas
- Learned about ReplicaSets and pod management
- Understood labels and selectors
- Experienced automatic pod recovery (self-healing)

**Day 8: Services & Networking**
- Created NodePort Service to expose the API
- Understood Kubernetes networking and load balancing
- Added pod identification to API responses (pod name and IP)
- Verified traffic distribution across multiple pods
- Learned about NAT in Kubernetes networking

**Day 9: Scaling & Resilience**
- Scaled deployment from 2 to 4 replicas
- Deleted pods to test self-healing
- Confirmed zero-downtime during pod failures

![Scaling Demo](img/k8s_day9.png)

---

**Day 10: Documentation**
Cleaned up the README and added screenshots.

**Day 11: Configuration Management**
This is where it got interesting. Instead of hardcoding values in the app, I:
- Created a ConfigMap for things like API version, environment, log level
- Created a Secret for sensitive stuff (database passwords, API keys)
- Updated the Flask app to read from environment variables
- Modified the Kubernetes deployment to inject these values

The cool part: I can now change configuration values without rebuilding the Docker image. Just edit the ConfigMap, restart the pods, and the new values are loaded.

**ConfigMap and Secret in Kubernetes:**

![ConfigMap and Secret Resources](img/k8s_day11_resources.png)

**All Pods Running with Config:**

![Running Pods](img/k8s_day11_pods.png)

**Configuration Endpoint Response:**

![Config Endpoint](img/k8s_day11_config_endpoint.png)

**Load Balancing Across Different Pods:**

![Load Balancing](img/k8s_day11_loadbalancing.png)

## ConfigMap Example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-api-configmap
data:
  API_VERSION: "v1.0"
  ENVIRONMENT: "development"
  LOG_LEVEL: "INFO"
```

Update it live:
```bash
kubectl edit configmap flask-api-configmap
# Change values
kubectl rollout restart deployment flask-api-deployment
```

## Project Structure

```
KREPTKON/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── venv/
├── k8s/
│   ├── flask-api-deployment-updated.yml
│   ├── flask-api-service.yml
│   ├── flask-configmap.yaml
│   └── flask-secret.yaml (not committed)
├── img/
└── README.md
```

## Troubleshooting Notes

**Pods not starting?**
```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

**Image not found in Minikube?**
Make sure you built it in Minikube's Docker daemon:
```bash
eval $(minikube docker-env)
docker build -t flask-api:latest .
```

**Service not accessible?**
```bash
minikube service flask-api-service --url
```

## Useful Commands

```bash
# Check everything
kubectl get all

# Scale deployment
kubectl scale deployment flask-api-deployment --replicas=5

# View logs
kubectl logs -l app=flask-api --tail=20

# Restart pods
kubectl rollout restart deployment flask-api-deployment

# Access Minikube dashboard
minikube dashboard
```

## Things I Found Tricky

1. **Minikube image caching** - Had to make sure I was building in Minikube's Docker daemon, not my local one
2. **ConfigMap indentation** - YAML is very picky about spaces
3. **Port 5000 conflict on Mac** - Had to disable AirPlay Receiver
4. **Understanding when pods pick up new config** - They don't automatically reload, need to restart them

## Next Steps

Planning to add:
- Database integration (PostgreSQL)
- Health checks
- Maybe a simple frontend
- Try deploying to a cloud provider

## Notes

The secret files (flask-secret.yaml) aren't committed to Git for security reasons. If you clone this repo, you'll need to create your own secrets:

```bash
kubectl create secret generic flask-api-secret \
  --from-literal=DATABASE_PASSWORD=yourpassword \
  --from-literal=API_KEY=yourapikey \
  --from-literal=JWT_SECRET=yourjwtsecret
```