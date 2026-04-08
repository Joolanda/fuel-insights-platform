# **Fuel Insights Platform — IAM Architecture**

## **1. Overview**
The Fuel Insights Platform uses **Keycloak** as its Identity & Access Management (IAM) provider.  
Authentication and authorization are implemented using:

- OpenID Connect (OIDC)  
- Client Credentials Flow  
- Role‑based access control (RBAC)  
- Service Account tokens  

This ensures a clean separation between identity, authorization, and application logic.

---

## **2. Realm Structure**
### **Realm: `fuel-insights`**
All application IAM configuration is isolated inside this realm.

The `master` realm is reserved for Keycloak administration and is not used by the application.

---

## **3. Clients**
### **Client: `fuel-api`**
This client represents the backend API.

| Setting | Value |
|--------|--------|
| Client Type | OpenID Connect |
| Access Type | confidential |
| Service Accounts Enabled | true |
| Standard Flow | false |
| Direct Access Grants | false |
| Token Endpoint | `/realms/fuel-insights/protocol/openid-connect/token` |

The client authenticates using a **client secret** and retrieves tokens via the Client Credentials Flow.

---

## **4. Authentication Flow**
### **Flow: Client Credentials**
The backend retrieves a token using:

```
client_id=fuel-api
client_secret=<secret>
grant_type=client_credentials
```

Keycloak returns a signed JWT containing:

- issuer  
- subject  
- expiration  
- service account username  
- assigned realm roles  

The token is forwarded to the API via:

```
Authorization: Bearer <token>
```

---

## **5. Authorization Model (RBAC)**

### **Realm Roles**
| Role | Purpose |
|------|---------|
| `fuel-user` | Standard API access |
| `viewer` | Read‑only access |
| `admin` | Elevated privileges |
| `offline_access` | System role |
| `uma_authorization` | System role |
| `default-roles-fuel-insights` | System composite role |

Only the first three are application‑specific.

### **Service Account Role Assignment**
The service account for `fuel-api` is assigned:

- `fuel-user`  
- `viewer`  
- `admin` (optional)  
- system roles (automatically assigned)

These roles appear in the JWT under:

```
realm_access.roles
```

---

## **6. FastAPI Integration**
FastAPI validates tokens using:

- Keycloak JWKS  
- issuer validation  
- audience validation  
- role extraction  

Example role check:

```python
if "fuel-user" not in token["realm_access"]["roles"]:
    raise HTTPException(status_code=403)
```

This ensures only authorized clients can access protected endpoints.

---

## **7. Example Successful Response**

```json
{
  "message": "Fuel history visible",
  "user": {
    "username": "service-account-fuel-api",
    "roles": [
      "viewer",
      "offline_access",
      "admin",
      "uma_authorization",
      "default-roles-fuel-insights",
      "fuel-user"
    ]
  }
}
```

This confirms:

- token is valid  
- roles are correctly assigned  
- authorization logic is functioning  

---

## **8. Security Considerations**
- Secrets are stored outside the repository.  
- Only confidential clients are used.  
- No interactive login flows are required.  
- Roles are minimal and scoped.  
- Realm is isolated from Keycloak’s master realm.

---

## **9. Extensibility**
This IAM setup supports:

- user accounts  
- frontend login flows  
- fine‑grained permissions  
- multi‑environment realms  
- multi‑client architectures  

The structure is modular and production‑ready.

---

## **10. Architecture Diagram (text‑based)**

```
+-------------------+         +----------------------+
|   Client Script   |  --->   |   Keycloak Token     |
| (get-token.sh)    |         |   Endpoint (OIDC)    |
+-------------------+         +----------------------+
           |                              |
           | Bearer Token                 |
           v                              |
+-------------------+         +----------------------+
|   FastAPI Backend | <------ |  Keycloak Realm      |
|   (fuel-api)      |         |  Roles & Policies    |
+-------------------+         +----------------------+
           |
           v
+-------------------+
| Protected Routes  |
| (/fuel/history)   |
+-------------------+
```

