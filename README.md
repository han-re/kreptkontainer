# KreptKon – Docker & Kubernetes Learning Project

KreptKon is a hands-on learning project where I'm building a Flask API and progressively containerizing and deploying it using Docker and Kubernetes. The project follows a structured day-by-day roadmap, moving from a basic local Flask app to a production-ready deployment on AWS EKS with RDS PostgreSQL.

The focus is on **understanding real-world backend infrastructure concepts**, not just getting something running.

---

## What Is It?

A Flask-based REST API that:
- Runs locally, in Docker, and in Kubernetes (Minikube → AWS EKS)
- Scales across multiple pods with load balancing
- Uses PostgreSQL for persistent data storage (local → AWS RDS)
- Uses Kubernetes ConfigMaps and Secrets for configuration management
- Deploys to AWS with ECR, EKS, and RDS
- Survives pod restarts without data loss

This project is designed as a **learning reference** and a **portfolio piece** demonstrating backend, containerization, orchestration, and cloud infrastructure fundamentals.

---

## Tech Stack

- **Python 3.11**
- **Flask + SQLAlchemy**
- **PostgreSQL 15**
- **Docker & Docker Compose**
- **Kubernetes (Minikube → AWS EKS)**
- **AWS Services (ECR, EKS, RDS)**
- **ConfigMaps & Secrets**
- **Persistent Volumes (PVC)**

---

## Project Structure
```
KREPTKON/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── venv/
├── k8s (kubernetes)/
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── flask-api-deployment.yaml
│   ├── flask-api-service.yaml
│   ├── secrets-aws.yaml (in-development)
│   ├── configmap-aws.yaml (in-development)
│   ├── flask-api-deployment-aws.yaml (in-development)
│   └── flask-api-service-aws.yaml (in-development)
├── docker-compose.yml
├── eks-cluster-config.yaml (in-development)
├── img/
└── README.md
```

> ⚠️ Secret files containing real credentials are **not committed**. Example files are provided instead.

---

## Running Locally (No Docker)
```bash
git clone <your-repo-url>
cd KreptKon/backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Access at: http://localhost:5000

---

## Running Locally with Docker Compose

This setup runs Flask + PostgreSQL locally using Docker Compose.
```bash
docker-compose up --build
```

Test endpoints:
```bash
curl http://localhost:5000/hello
curl http://localhost:5000/users

curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com"}'
```

---

## Running on Kubernetes (Minikube)

### Prerequisites

- Docker
- Minikube
- kubectl

### Deploy to Minikube
```bash
# Start Minikube and build image
minikube start
eval $(minikube docker-env)

cd backend
docker build -t flask-api:latest .
cd ..

# Deploy Kubernetes resources
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
kubectl apply -f kubernetes/flask-api-deployment.yaml
kubectl apply -f kubernetes/flask-api-service.yaml

# Access the API
minikube service flask-api-service --url
```

---

## In-Development
## Running on AWS EKS

### Prerequisites

- AWS CLI configured
- eksctl installed
- kubectl installed

### Deploy to EKS
```bash
# Create EKS cluster
eksctl create cluster -f eks-cluster-config.yaml

# Deploy to EKS
kubectl apply -f kubernetes/secrets-aws.yaml
kubectl apply -f kubernetes/configmap-aws.yaml
kubectl apply -f kubernetes/flask-api-deployment-aws.yaml
kubectl apply -f kubernetes/flask-api-service-aws.yaml

# Get LoadBalancer URL
kubectl get svc flask-api-service
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /hello | Basic greeting with pod info |
| GET | /status | API status and database connection |
| GET | /users | List all users |
| POST | /users | Create a new user |
| GET | /users/<id> | Get user by ID |
| DELETE | /users/<id> | Delete a user |

---

## Learning Roadmap

### Days 1–11: Foundations (Phase 1)

**What I built:**
- Flask API with multiple endpoints
- Docker containerization with Dockerfile
- Kubernetes deployments on Minikube
- ConfigMaps and Secrets for configuration
- Scaling and self-healing demonstrations

**Key learning points:**
- Docker fundamentals: build, run, exec, ps
- Kubernetes core concepts: Pods, Deployments, Services, ReplicaSets
- Load balancing across multiple pods
- Zero-downtime deployments and auto-recovery
- Configuration management without rebuilding images

**Outcome:**
- Flask app running in Kubernetes with 2-4 replicas
- NodePort service exposing the API
- Dynamic scaling working (2→4→2 replicas)
- Pod self-healing verified

**Day 9: Scaling & Resilience**
- Scaled deployment from 2 to 4 replicas
- Deleted pods to test self-healing
- Confirmed zero-downtime during pod failures

![Scaling Demo](img/k8s_day9.png)

**Day 11: Configuration Management**

**ConfigMap and Secret in Kubernetes:**

![ConfigMap and Secret Resources](img/k8s_day11_resources.png)

**All Pods Running with Config:**

![Running Pods](img/k8s_day11_pods.png)

**Configuration Endpoint Response:**

![Config Endpoint](img/k8s_day11_config_endpoint.png)

**Load Balancing Across Different Pods:**

![Load Balancing](img/k8s_day11_loadbalancing.png)

---

### Day 12 – PostgreSQL Integration (Local)

**Goal:** Add PostgreSQL to the Flask app and run everything locally using Docker Compose.

**What I implemented:**
- SQLAlchemy models for database entities
- Database configuration via environment variables
- CRUD API endpoints for user management
- Docker Compose setup with Flask + PostgreSQL services
- Volume mounting for database persistence

**Key learning points:**
- SQLAlchemy ORM basics: models, sessions, queries
- Flask-SQLAlchemy integration patterns
- Docker Compose networking and service dependencies
- Environment variable injection in containers
- Database connection string formats

**Outcome:**
- Flask successfully connected to PostgreSQL
- Full CRUD operations working locally
- Data persisted across container restarts
- Multi-container orchestration with Docker Compose

---

### Day 13 – Kubernetes PostgreSQL + Persistence (Phase 2 – Day 2)

**Goal:** Run PostgreSQL inside Kubernetes and connect multiple Flask pods to it with persistent storage.

**What I implemented:**
- PostgreSQL Deployment (single replica)
- PostgreSQL ClusterIP Service for internal networking
- PersistentVolumeClaim for database storage
- ConfigMap for non-sensitive database configuration
- Secrets for credentials and connection strings
- Updated Flask Deployment to consume Kubernetes config
- Verified data persistence after pod restarts

**Key learning points:**
- Why databases need persistent storage in Kubernetes
- PersistentVolume vs PersistentVolumeClaim lifecycle
- StatefulSets vs Deployments for stateful applications
- Kubernetes DNS and service discovery (using service names)
- Debugging CrashLoopBackOff and volume mount issues
- Separation of ConfigMaps (public config) vs Secrets (sensitive data)

**Outcome:**
- PostgreSQL running in Kubernetes with persistent storage
- Multiple Flask pods successfully connecting to single PostgreSQL instance
- CRUD operations working through Kubernetes service
- Data survives pod deletions and restarts
- No data loss during scaling operations

---

### Next Steps: AWS Deployment (Days 14-18)

Planning to complete:
- **Day 14:** Set up AWS account, create ECR repository, and push Docker images to AWS
- **Day 15:** Create EKS cluster with eksctl for production Kubernetes environment
- **Day 16:** Deploy RDS PostgreSQL instance for managed database with automated backups
- **Day 17:** Configure security groups and VPC networking for EKS-RDS communication, deploy Flask app to EKS with LoadBalancer
- **Day 18:** Add CloudWatch monitoring and logging, create architecture diagrams, finalize documentation

---

## Common Kubernetes Commands
```bash
# View all resources
kubectl get all

# View pods with details
kubectl get pods -o wide

# Check persistent volume claims
kubectl get pvc

# View application logs
kubectl logs -l app=flask-api
kubectl logs -l app=postgres

# Restart deployment
kubectl rollout restart deployment flask-api-deployment

# Scale deployment
kubectl scale deployment flask-api-deployment --replicas=4

# Access Minikube dashboard
minikube dashboard
```

---

## ConfigMap & Secrets Example

### ConfigMap (Non-sensitive configuration)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-config
data:
  FLASK_ENV: "production"
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  DATABASE_NAME: "kreptkon"
```

Update live:
```bash
kubectl edit configmap flask-config
kubectl rollout restart deployment flask-api-deployment
```

### Secrets (Sensitive data)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secrets
type: Opaque
stringData:
  POSTGRES_USER: user
  POSTGRES_PASSWORD: password
  DATABASE_URL: postgresql://user:password@postgres-service:5432/kreptkon
```

---

## Troubleshooting

### Pods not starting?
```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Image not found in Minikube?

Make sure you built it in Minikube's Docker daemon:
```bash
eval $(minikube docker-env)
docker build -t flask-api:latest .
```

### Service not accessible?
```bash
minikube service flask-api-service --url
```

### Database connection issues?
```bash
# Check PostgreSQL pod logs
kubectl logs -l app=postgres

# Verify secrets are loaded
kubectl get secret postgres-secrets -o yaml

# Test connection from Flask pod
kubectl exec -it <flask-pod-name> -- sh
# Inside pod:
# python
# from models import db
# db.session.execute('SELECT 1')
```

### PersistentVolumeClaim issues?
```bash
# Check PVC status
kubectl get pvc

# Describe PVC for events
kubectl describe pvc postgres-pvc

# If corrupted, delete and recreate
kubectl delete pvc postgres-pvc
kubectl apply -f kubernetes/postgres-pvc.yaml
```

---

## Things I Found Tricky

1. **Minikube image caching** - Had to make sure I was building in Minikube's Docker daemon, not my local one
2. **ConfigMap indentation** - YAML is very picky about spaces
3. **Port 5000 conflict on Mac** - Had to disable AirPlay Receiver in System Preferences
4. **Understanding when pods pick up new config** - They don't automatically reload, need to restart them
5. **PostgreSQL persistent storage** - Took time to understand PersistentVolumes vs PersistentVolumeClaims and reclaim policies
6. **Database connection strings** - Service names in Kubernetes act as DNS, learned to use `postgres-service` instead of `localhost`
7. **PostgreSQL crashing due to corrupted PVC data** - Had to delete and recreate PVC when data got corrupted
8. **PVC deletion and finalizers** - Understanding why PVCs sometimes get stuck in "Terminating" state

---

## Security Notes

Secret files are ignored via `.gitignore` and not committed to the repository.

### For local Kubernetes development:
```bash
kubectl create secret generic postgres-secrets \
  --from-literal=POSTGRES_USER=user \
  --from-literal=POSTGRES_PASSWORD=yourpassword \
  --from-literal=DATABASE_URL=postgresql://user:yourpassword@postgres-service:5432/kreptkon
```

### For AWS deployment:

AWS credentials and sensitive configuration stored in `.env` file (also gitignored).

---

**Note:** This is a learning project demonstrating containerization, orchestration, and cloud deployment patterns. Not production-ready without additional security hardening, monitoring, CI/CD pipelines, and proper secret management solutions like AWS Secrets Manager or HashiCorp Vault.