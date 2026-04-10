# KreptKon

A Flask REST API that I built from scratch and progressively deployed across three environments: local Docker Compose, Kubernetes on Minikube, and a production AWS stack using EKS, RDS, and ECR. The project is a hands-on demonstration of backend development, containerisation, orchestration, and cloud infrastructure.

## Tech Stack

- Python 3.11, Flask, SQLAlchemy
- PostgreSQL 15
- Docker and Docker Compose
- Kubernetes (Minikube, then AWS EKS)
- AWS (ECR, EKS, RDS, ELB, CloudWatch)
- kubectl, eksctl, AWS CLI

## Architecture

![AWS Architecture](img/kreptkon_aws_architecture.jpg)

The Flask application runs as a scalable Kubernetes Deployment inside an EKS cluster. The EKS nodes pull container images from ECR, the pods query a managed RDS PostgreSQL instance, and CloudWatch collects metrics and logs. Pods can be scaled horizontally, and Kubernetes handles automatic recovery if any pod fails.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/hello` | Health check with pod info |
| GET | `/status` | Application and database status |
| GET | `/users` | List all users |
| POST | `/users` | Create a new user |
| GET | `/users/<id>` | Get user by ID |
| DELETE | `/users/<id>` | Delete a user |

## Project Structure

```
KREPTKON/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── flask-api-configmap.yml
│   ├── flask-api-deployment-updated.yml
│   ├── flask-api-deployment-aws.yml
│   ├── flask-api-service.yml
│   ├── flask-api-service-aws.yml
│   ├── flask-api-secret.example.yml
│   ├── postgres-deployment.yml
│   ├── postgres-pvc.yml
│   ├── postgres-service.yml
│   ├── postgres-secret.example.yml
│   └── rds-secret.example.yml
├── docker-compose.yml
├── eks-cluster-config.yml
├── img/
└── README.md
```

Secret files containing real credentials are not committed. Example values are provided below.

## Running Locally with Docker Compose

```bash
git clone <your-repo-url>
cd KreptKon
docker-compose up --build
```

This starts the Flask API and a PostgreSQL container. Test with:

```bash
curl http://localhost:5000/hello
curl http://localhost:5000/users

curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com"}'
```

## Running on Kubernetes (Minikube)

```bash
minikube start
eval $(minikube docker-env)

cd backend
docker build -t flask-api:latest .
cd ..

kubectl apply -f k8s/flask-api-configmap.yml
kubectl apply -f k8s/flask-api-secret.yml
kubectl apply -f k8s/postgres-pvc.yml
kubectl apply -f k8s/postgres-deployment.yml
kubectl apply -f k8s/postgres-service.yml
kubectl apply -f k8s/flask-api-deployment-updated.yml
kubectl apply -f k8s/flask-api-service.yml

minikube service flask-api-service --url
```

Flask pods running on Minikube, each with its own cluster IP:

![Pods running on Minikube](img/k8s_day11_pods.png)

## Deploying to AWS (EKS + RDS)

### Prerequisites

AWS CLI configured, eksctl installed, kubectl installed.

### 1. Push image to ECR

```bash
aws ecr create-repository --repository-name kreptkon/flask-api --region us-east-1

aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker buildx build --platform linux/amd64 -t <ecr-uri>:latest --push backend/
```

### 2. Create EKS cluster

```bash
eksctl create cluster -f eks-cluster-config.yaml
```

The cluster config provisions two t3.small nodes with policies for ECR access, auto-scaling, CloudWatch, and EBS storage.

Two worker nodes running on EKS after cluster creation:

![EKS worker nodes](img/EKS_nodes_screenshot.png)

### 3. Create RDS PostgreSQL instance

Create the RDS instance in the same VPC as the EKS cluster, with a security group allowing inbound PostgreSQL traffic from the EKS node security group. I used a db.t3.micro instance running PostgreSQL 15 with no public access.

### 4. Deploy to EKS

Update the AWS secret and config files with your RDS endpoint and ECR URI, then apply:

```bash
kubectl apply -f k8s/flask-api-configmap.yml
kubectl apply -f k8s/flask-api-secret.yml
kubectl apply -f k8s/rds-secret.yml
kubectl apply -f k8s/flask-api-deployment-aws.yml
kubectl apply -f k8s/flask-api-service-aws.yml
```

### 5. Access the API

```bash
kubectl get svc flask-api-service
```

The LoadBalancer service exposes the API on port 80, forwarding to the Flask containers on port 5000.

## Scaling and Resilience

The deployment supports horizontal scaling. Kubernetes automatically reschedules pods if any fail.

```bash
kubectl scale deployment flask-api-deployment --replicas=4
kubectl get pods -w
```

Below: scaling up to 5 replicas, then deleting a pod to demonstrate self-healing. Kubernetes immediately spins up a replacement (`k6n27`, age 5s):

![Scaling and self-healing](img/k8s_day9.png)

Repeated requests to `/hello` show traffic being distributed across different pods, each returning its own pod name and IP:

![Load balancing across pods](img/k8s_day11_loadbalancing.png)

## Monitoring

Application logs are structured and written to stdout, picked up by CloudWatch Container Insights. Logs are visible both via kubectl and in the CloudWatch console.

```bash
kubectl logs -l app=flask-api -f
```

The Flask deployment includes liveness probes on `/hello` and readiness probes on `/status` to ensure traffic only reaches healthy pods.

## Configuration Management

Non-sensitive values (environment, database host, port) are stored in a ConfigMap. Sensitive values (credentials, connection strings) are stored in a Kubernetes Secret. Configuration can be updated without rebuilding the Docker image:

```bash
kubectl edit configmap flask-config
kubectl rollout restart deployment flask-api-deployment
```

ConfigMap and Secret resources loaded in the cluster:

![ConfigMap and Secret resources](img/k8s_day11_resources.png)

The `/config` endpoint confirms that environment variables, feature flags, and secrets are all injected correctly into the running pod:

![Config endpoint response](img/k8s_day11_config_endpoint.png)

## What I Learned

This project took me from writing a basic Flask app to deploying it on AWS with a managed database, load balancing, auto-scaling, and monitoring. The main areas I developed understanding in:

- Docker containerisation and multi-stage builds
- Kubernetes core concepts: Pods, Deployments, Services, ReplicaSets, PersistentVolumeClaims
- Kubernetes networking, DNS-based service discovery, and load balancing across pods
- AWS infrastructure: EKS cluster creation with eksctl, RDS setup, ECR image management, VPC and security group configuration
- Configuration management with ConfigMaps and Secrets
- Health checks, readiness probes, and rolling updates for zero-downtime deployments
- CloudWatch integration for centralised logging

## Troubleshooting

**Pods stuck in CrashLoopBackOff:** Check logs with `kubectl logs <pod-name>` and events with `kubectl describe pod <pod-name>`. Common causes are missing secrets or incorrect database connection strings.

**Image not found in Minikube:** Build the image inside Minikube's Docker daemon using `eval $(minikube docker-env)` before running `docker build`.

**Database connection failures on EKS:** Verify the RDS security group allows inbound traffic from the EKS cluster security group on port 5432. Test connectivity from a pod using `kubectl exec`.

**PVC stuck in Terminating state:** Usually caused by finalizers. Check `kubectl describe pvc` for details.

## Cleanup

To avoid ongoing AWS charges:

```bash
eksctl delete cluster --name kreptkon-cluster --region us-east-1

aws rds delete-db-instance \
  --db-instance-identifier kreptkon-postgres \
  --skip-final-snapshot --region us-east-1

aws ecr delete-repository \
  --repository-name kreptkon/flask-api \
  --force --region us-east-1
```

## Security Notes

Secret files are excluded via `.gitignore`. To recreate secrets for local Kubernetes development:

```bash
kubectl create secret generic postgres-secrets \
  --from-literal=POSTGRES_USER=user \
  --from-literal=POSTGRES_PASSWORD=yourpassword \
  --from-literal=DATABASE_URL=postgresql://user:yourpassword@postgres-service:5432/kreptkon
```

For AWS deployment, credentials and configuration are stored in a local `.env` file that is also gitignored. In a production setting, these would be managed through AWS Secrets Manager or a similar tool.
