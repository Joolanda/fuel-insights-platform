# **Fuel Insights Platform**  
*A cloud‑native platform for monitoring heating oil, diesel, and gasoline consumption with IAM, DevOps, and observability.*

## **Overview**
The Fuel Insights Platform is a compact but production‑style project designed to demonstrate modern DevOps, CloudOps, and IAM practices.  
It integrates:

- A secure API protected by **Keycloak IAM**
- Deployment on **Kubernetes** (local + AWS)
- **GitOps** workflows using ArgoCD
- Full **observability** with Prometheus, Grafana, and Loki
- Real fuel‑consumption data (heating oil, diesel, gasoline)
- Optional external price integration

## **Intended Use**
This project is built for **private household fuel analysis**.  
It helps consumers monitor heating oil, diesel, or gasoline usage and understand their own consumption patterns.

The architecture is intentionally flexible and can be extended later to support additional use cases, such as **agricultural fuel storage** or small‑scale diesel tank monitoring.

---

## **Features**
- 🔐 **Identity & Access Management** with Keycloak  
- 🧪 **FastAPI service** with JWT‑protected endpoints  
- 📊 **Monitoring & Logging** via Prometheus, Grafana, Loki  
- 🚀 **Kubernetes deployment** (local + AWS)  
- 🔄 **GitOps** with ArgoCD  
- ☁️ **AWS‑ready** (EC2, S3, CloudWatch)  
- ⛽ **Multi‑fuel analytics** (heating oil, diesel, gasoline)

---

## **Architecture**
The platform consists of:

- **API Service**  
  FastAPI application exposing fuel history, consumption, and price endpoints.

- **Keycloak IAM**  
  Realm, clients, and roles for secure access control.

- **Kubernetes Deployment**  
  Manifests for API, Keycloak, ingress, and monitoring stack.

- **Observability Stack**  
  Prometheus for metrics, Grafana dashboards, Loki logs.

- **GitOps**  
  ArgoCD manages deployments from this repository.

- **AWS Integration (optional)**  
  EC2 + k3s cluster, S3 storage, CloudWatch logs.

---

## **Repository Structure**
```
api/                # FastAPI application
data/               # Fuel datasets (converted from Excel)
docs/               # Architecture, IAM design, AWS deployment
keycloak/           # Realm export, clients, roles
k8s/                # Kubernetes manifests (base + overlays)
monitoring/         # Prometheus, Grafana, Loki configs
argocd/             # GitOps application definitions
```

---

## **IAM Design**
Keycloak realm: `fuel-insights`

Roles:
- `viewer` – read-only access  
- `admin` – manage fill-ups, alerts, configuration  

Clients:
- `fuel-api` (confidential)
- `fuel-frontend` (public)

Authentication:
- OIDC Authorization Code Flow (frontend)
- Bearer token (API)

---

## **Local Development**
Local environment uses:

- Docker
- kind/k3d Kubernetes cluster
- Keycloak container
- Prometheus + Grafana + Loki stack

---

## **AWS Deployment**
The platform can be deployed on AWS using:

- EC2 (Free Tier)
- k3s cluster
- S3 for data storage
- CloudWatch for logs
- IAM roles for service access

---

## **Status**
This project is under active development.

---

Als je wilt, maak ik nu ook:

- **IAM_DESIGN.md**  
- **ARCHITECTURE.md** (met diagram)  
- **LOCAL_SETUP.md**  
- **AWS_DEPLOYMENT.md**  
- of het **FastAPI skeleton** met Keycloak‑auth  

Zeg maar welke stap je nu wilt zetten — we bouwen dit platform strak verder.