# Traefik API Gateway - Job Application Microservices

A comprehensive Kubernetes-based microservices application using Traefik as an API Gateway with advanced routing, authentication, and monitoring capabilities.

## 🏗️ Architecture Overview

This project implements a microservices architecture with:

- **API Gateway**: Traefik v3.0 with advanced middleware
- **Authentication Service**: JWT-based authentication (Port 9000)
- **Jobs Listing Service**: Job management endpoints (Port 5000)
- **Applications Service**: Job application management (Port 8000)
- **Redis**: Storing of revoked JTI
- **PostgreSQL**: Primary database storage

## 🚀 Features

### API Gateway Capabilities
- **Intelligent Routing**: Path-based routing to microservices
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Configurable request throttling (100 burst, 1min period)
- **Circuit Breaker**: Automatic failure detection and recovery
- **CORS Support**: Cross-origin resource sharing
- **Request/Response Transformation**: Header manipulation
- **Compression**: Automatic response compression
- **Retry Logic**: Automatic request retries (3 attempts)
- **Health Checks**: Built-in service monitoring
- **Metrics**: Prometheus integration for monitoring

### Security Features
- JWT token validation middleware
- Protected and public route separation
- IP-based rate limiting
- Circuit breaker for resilience
- Secure header management

## 📁 Project Structure

```
job-microservice-app/
├── auth-service/
├── eks-deployment-setup/
│   ├── auth/
│   ├── jobs-applications/
│   ├── jobs-listing/
│   ├── traefik/
│   ├── apply-db-migrations.sh
│   ├── apply-k8s-configs.sh
│   ├── apply-traefik.sh
│   ├── delete-traefik.sh
│   ├── eks-cluster.yaml
│   ├── namespace.yaml
│   ├── redis-deployment.yaml
│   └── redis-service.yaml
├── job-apply-service/
├── job-listing-service/
├── .env
├── .env.sample
├── .gitignore
├── docker-compose.yaml
└── README.md
```

## 🛣️ API Routes

### Public Routes (No Authentication Required)
- `GET /api` - API status
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/validate-token` - Token validation

### Protected Routes (JWT Required)
- `GET /api/v1/me` - User profile
- `POST /api/v1/auth/refresh` - Token refresh
- `POST /api/v1/auth/logout` - User logout
- `GET|POST|PUT|DELETE /api/v1/jobs/*` - Jobs management
- `GET|POST|PUT|DELETE /api/v1/applications/*` - Applications management

## ⚠️ Test Environment Disclaimer

This project is a test/demo application. All secrets, keys, and environment variables used here are for testing purposes only.

- ✅ Do NOT reuse any credentials in this Project, it has been completely deleted after testing. 
- ✅ All infrastructure (Kubernetes clusters, databases, services, secrets, etc.) has been completely deleted after testing.
- ✅ This repository is shared strictly for educational and demonstration purposes.

## 🚀 Deployment Instructions

To deploy this application, navigate to the `eks-deployment-setup` directory and run the following scripts in order:

### 1. Navigate to the eks-deployment-setup directory
```bash
    cd eks-deployment-setup
```

### 2. Create an EKS Cluster
```bash
    eksctl create cluster --name micro-eks-cluster --region eu-north-1 --node-type t3.medium
```

### 3. Create a Namespace for Your Cluster
```bash
    kubectl apply -f namespace.yaml
```

### 4. Apply Traefik as API Gateway
```bash
    ./apply-traefik.sh
```

### 5. Apply Kubernetes Configurations
```bash
    ./apply-k8s-configs.sh
```

### 6. Apply Database Migrations
```bash
    ./apply-db-migrations.sh
```

### 7. Install ArgoCD in Your Cluster
```bash
    ./apply-argo-cd.sh
```

- ⚠️ Login into ArgoCD UI `https://localhost:{PORT}`, check your terminal for username and password

### 8. Configure ArgoCD to Sync with GitOps Repository
```bash
    kubectl apply -f argo.yaml
```

### 9. Update Redis in the Cluster

#### Step 1: Exec into the debug pod
```bash
  kubectl exec -it debug-pod -n job-application-microservices -- /bin/sh
```

#### Step 2: Inside the pod - update and install redis-cli
```bash
  apt update && apt install -y redis-tools
```

#### Step 3: Test connection to Redis service
```bash
  redis-cli -h redis-service -p 6379 ping
```
**Expected Output:** `PONG`

## 🔧 Middleware Configuration

### JWT Authentication
- Validates tokens via auth service
- Forwards user context headers
- Supports authorization header passthrough

### Rate Limiting
- **Burst**: 100 requests
- **Period**: 1 minute
- **Strategy**: IP-based limiting

### Circuit Breaker
- **Network Error Threshold**: 30%
- **HTTP Error Threshold**: 25% (5xx responses)
- **Auto-recovery**: Built-in

### CORS Configuration
- **Methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS
- **Origins**: Configurable (currently set to *)
- **Credentials**: Supported
- **Max Age**: 3600 seconds

## 📊 Monitoring and Observability

### Health Checks
- **Endpoint**: `/ping` on port 8080
- **Liveness Probe**: 10s intervals
- **Readiness Probe**: 5s intervals

### Metrics
- **Prometheus Integration**: Built-in metrics export
- **Custom Buckets**: 0.1, 0.3, 1.2, 5.0 seconds
- **ServiceMonitor**: Automatic Prometheus discovery

### Logging
- **Access Logs**: Enabled
- **Log Level**: INFO
- **Structured Logging**: JSON format

## 🔐 Security Considerations

1. **Authentication**: JWT tokens required for protected routes
2. **Rate Limiting**: Prevents abuse and DDoS attacks
3. **Circuit Breaker**: Protects against cascade failures
4. **CORS**: Configurable cross-origin policies
5. **Header Security**: Custom security headers added

## 🛠️ Development and Testing

### Prerequisites
- Kubernetes cluster (EKS recommended)
- kubectl configured
- Docker for container management

### Local Development
1. Clone the repository
2. Follow deployment instructions above
3. Access Traefik dashboard at `http://localhost:8080`
4. Monitor services and routing rules

### Testing API Endpoints
```bash
    # Test public endpoint
    curl http://your-loadbalancer/api/v1/auth/login
    
    # Test protected endpoint (with JWT)
    curl -H "Authorization: Bearer your-jwt-token" http://your-loadbalancer/api/v1/jobs
```

## 📝 Configuration Files

### Core Components
- **traefik-deployment.yaml**: Main Traefik deployment with middlewares
- **ingress-configs.yaml**: Route definitions and service mappings
- **RBAC**: Cluster roles and permissions for Traefik

### Middleware Stack
1. JWT Authentication
2. CORS Headers
3. Rate Limiting
4. Circuit Breaker
5. Retry Logic
6. Compression
7. API Headers

## 🤝 Contributing

This is a demonstration project. For educational purposes:
1. Fork the repository
2. Create feature branches
3. Test thoroughly
4. Document changes
5. Submit pull requests

## 📜 License

This project is for educational and demonstration purposes only. Please ensure you understand the security implications before adapting for production use.

---

**⚠️ Remember: This is a test environment. Never use these configurations, secrets, or credentials in production systems.**