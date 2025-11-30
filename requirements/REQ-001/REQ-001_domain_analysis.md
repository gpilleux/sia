# REQ-001: DOMAIN ANALYSIS - Waiting List + Authentication

**Requirement**: REQ-001 - Waiting List + Authentication & Permission System  
**Analysis Date**: 2025-11-23  
**Analyst**: GitHub Copilot (SUPER_AGENT)

---

## EXECUTIVE SUMMARY

**Problem**: Public ERP with zero authentication attempting to capture leads while protecting data privacy.

**Solution Architecture**: Dual-mode API (public `/api/v1/public/*` + authenticated `/api/v1/*`) with RBAC permission filtering.

**Domain Model**: Reuse existing `Lead` aggregate with `source="waiting_list"` + implement JWT-based authentication.

**Critical Finding**: 71 endpoints currently public - CRITICAL SECURITY RISK requiring immediate auth layer.

---

## DOMAIN RESEARCH

### 1. Authentication Patterns Research

**Source**: FastAPI Official Documentation (via manual analysis)

**JWT Authentication Pattern** (FastAPI Standard):
```python
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return await user_repository.find_by_id(user_id)
    except JWTError:
        raise HTTPException(status_code=401)
```

**Key Findings**:
- ✅ Use `python-jose` for JWT (FastAPI official recommendation)
- ✅ `HTTPBearer` security scheme for Authorization header
- ✅ Stateless tokens (no session DB table needed)
- ✅ Include `user_id`, `company_id`, `roles` in payload
- ⚠️ Token expiry: 24h standard, refresh token = Phase 5

### 2. Rate Limiting Research

**Source**: slowapi library (FastAPI-compatible)

**Pattern**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/public/leads")
@limiter.limit("5/minute")
async def create_public_lead(...):
    ...
```

**Key Findings**:
- ✅ `slowapi` = Flask-Limiter port for FastAPI
- ✅ `get_remote_address` extracts IP from request
- ✅ Decorator-based (clean, declarative)
- ⚠️ In-memory storage (acceptable for MVP, Redis = Phase 5)

### 3. RBAC Permission Patterns

**Source**: Existing ERP Identity Module (init.sql)

**Current Schema**:
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    company_id UUID,
    permissions JSONB DEFAULT '[]'  -- ✅ Already supports permission list
);

CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id),
    role_id UUID REFERENCES roles(id),
    PRIMARY KEY(user_id, role_id)
);
```

**Permission Model Design**:
```python
# Granular permissions (flat list)
PERMISSIONS = [
    "lead.view_all",       # See ALL leads (including waiting_list)
    "lead.view_public",    # See only public leads (exclude waiting_list)
    "lead.create",
    "lead.update",
    "lead.delete",
    "customer.view",
    "customer.create",
    # ... 50+ permissions total
]

# Role-based assignment
ROLE_DEFAULTS = {
    "ADMIN": ["lead.view_all", "lead.create", "lead.update", "lead.delete", ...],
    "MANAGER": ["lead.view_all", "lead.create", "lead.update", ...],
    "EMPLOYEE": ["lead.view_public", "lead.create", ...],
    "PROCUREMENT": ["lead.view_public", "requisition.create", ...],
    "FINANCE": ["lead.view_public", "invoice.view", "invoice.approve", ...],
}
```

**Key Findings**:
- ✅ Database already supports JSONB permissions (no migration needed)
- ✅ Flat permission model (KISS) > hierarchical roles
- ✅ Check permissions in Application layer (use cases)
- ❌ NO row-level security in PostgreSQL (over-engineering, use repository filtering)

---

## DOMAIN MODEL ANALYSIS

### Entities (Existing - NO CHANGES)

**Lead Aggregate** (backend/src/erp/domain/crm/entities.py):
```python
@dataclass(frozen=True)
class Lead(AggregateRoot):
    name: str
    email: Optional[Email]
    phone: Optional[PhoneNumber]
    company: Optional[str]
    source: Optional[str]        # ✅ "waiting_list", "website", "referral"
    status: LeadStatus           # ✅ NEW, CONTACTED, QUALIFIED, CONVERTED
    score: int
    notes: Optional[str]
```

**User Aggregate** (backend/src/erp/domain/identity/entities.py):
```python
@dataclass(frozen=True)
class User(AggregateRoot):
    email: Email
    name: str
    company_id: UUID
    is_active: bool
    password_hash: str  # ⚠️ ADD THIS FIELD (currently missing)
```

**Role Aggregate** (backend/src/erp/domain/identity/entities.py):
```python
@dataclass(frozen=True)
class Role(AggregateRoot):
    name: str
    company_id: UUID
    permissions: List[str]  # ✅ JSON array from DB
```

### Value Objects (NEW)

**AuthToken** (backend/src/erp/domain/identity/value_objects.py - NEW FILE):
```python
@dataclass(frozen=True)
class AuthToken:
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400  # 24h in seconds
    
    @staticmethod
    def create(user_id: UUID, company_id: UUID, roles: List[str]) -> "AuthToken":
        payload = {
            "sub": str(user_id),
            "company_id": str(company_id),
            "roles": roles,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return AuthToken(access_token=token)
```

### Repositories (Interface Additions)

**ILeadRepository** (backend/src/erp/domain/crm/repositories.py):
```python
class ILeadRepository(ABC):
    # Existing methods
    async def save(self, lead: Lead) -> Lead: ...
    async def find_by_id(self, lead_id: UUID) -> Optional[Lead]: ...
    async def find_all(self, skip: int, limit: int) -> List[Lead]: ...
    
    # NEW METHOD
    @abstractmethod
    async def find_all_except_source(
        self, 
        exclude_source: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Lead]:
        """Filter out leads with specific source (for permission filtering)"""
        pass
```

**IUserRepository** (backend/src/erp/domain/identity/repositories.py):
```python
class IUserRepository(ABC):
    # Existing methods
    async def save(self, user: User) -> User: ...
    async def find_by_id(self, user_id: UUID) -> Optional[User]: ...
    
    # NEW METHODS
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email (for login)"""
        pass
    
    @abstractmethod
    async def get_user_permissions(self, user_id: UUID) -> List[str]:
        """Get flattened permission list from user roles"""
        pass
```

---

## USE CASES (Application Layer)

### New Use Cases

**1. AuthenticateUserUseCase** (backend/src/erp/application/identity/use_cases.py):
```python
class AuthenticateUserUseCase:
    """Login use case - validates credentials, returns JWT"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, email: str, password: str) -> AuthToken:
        # Find user
        user = await self.user_repository.find_by_email(email)
        if not user or not user.is_active:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        # Get roles
        permissions = await self.user_repository.get_user_permissions(user.id)
        
        # Create JWT
        return AuthToken.create(user.id, user.company_id, permissions)
```

**2. CreatePublicLeadUseCase** (backend/src/erp/application/crm/use_cases.py):
```python
class CreatePublicLeadUseCase:
    """Public waiting list signup - NO authentication required"""
    
    def __init__(self, lead_repository: ILeadRepository):
        self.lead_repository = lead_repository
    
    async def execute(self, dto: CreatePublicLeadDTO) -> UUID:
        # Validate email
        email = Email(dto.email)
        
        # Create Lead with forced source
        lead = Lead(
            name=dto.name,
            email=email,
            company=dto.company,
            source="waiting_list",  # ✅ Force waiting_list
            status=LeadStatus.NEW,
            notes=dto.message
        )
        
        # Save
        created = await self.lead_repository.save(lead)
        return created.id
```

**3. ListLeadsWithPermissionFilterUseCase** (backend/src/erp/application/crm/use_cases.py):
```python
class ListLeadsWithPermissionFilterUseCase:
    """List leads filtered by user permissions"""
    
    def __init__(
        self,
        lead_repository: ILeadRepository,
        user_repository: IUserRepository
    ):
        self.lead_repository = lead_repository
        self.user_repository = user_repository
    
    async def execute(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Lead]:
        # Get user permissions
        permissions = await self.user_repository.get_user_permissions(user_id)
        
        # Check permission level
        if "lead.view_all" in permissions:
            # Admin/Manager: See all leads
            return await self.lead_repository.find_all(skip, limit)
        else:
            # Employee: Exclude waiting_list
            return await self.lead_repository.find_all_except_source(
                exclude_source="waiting_list",
                skip=skip,
                limit=limit
            )
```

---

## API LAYER DESIGN

### Route Structure

```
/api/v1/public/          # NO authentication
├── POST /leads          # Waiting list signup

/api/v1/auth/            # Authentication endpoints
├── POST /login          # Returns JWT
└── POST /logout         # (Optional - stateless JWT doesn't need logout)

/api/v1/crm/             # ✅ AUTH REQUIRED
├── GET /leads           # Filtered by permissions
├── GET /leads/{id}
├── POST /leads          # Admin/Manager only
├── PUT /leads/{id}
└── DELETE /leads/{id}

/api/v1/sales/*          # ✅ AUTH REQUIRED (all existing endpoints)
/api/v1/accounting/*     # ✅ AUTH REQUIRED
/api/v1/purchase/*       # ✅ AUTH REQUIRED
/api/v1/identity/*       # ✅ AUTH REQUIRED
```

### Dependency Injection Pattern

**Current** (NO AUTH):
```python
@router.get("/leads")
async def list_leads(
    repo: ILeadRepository = Depends(get_lead_repository)
):
    leads = await repo.find_all()  # ⚠️ Returns ALL leads to anyone
    return leads
```

**New** (WITH AUTH):
```python
@router.get("/leads")
async def list_leads(
    user: User = Depends(get_current_user),  # ✅ Validates JWT
    repo: ILeadRepository = Depends(get_lead_repository),
    user_repo: IUserRepository = Depends(get_user_repository)
):
    use_case = ListLeadsWithPermissionFilterUseCase(repo, user_repo)
    leads = await use_case.execute(user.id)  # ✅ Filtered by permissions
    return leads
```

---

## INFRASTRUCTURE LAYER

### Password Hashing

**Library**: `passlib[bcrypt]`

**Implementation** (backend/src/erp/infrastructure/auth/password.py - NEW):
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### JWT Configuration

**Environment Variables** (.env):
```bash
JWT_SECRET_KEY=your-256-bit-secret-key-here  # ⚠️ MUST be random
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
```

**Config** (backend/src/erp/infrastructure/auth/config.py - NEW):
```python
import os
from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):
    secret_key: str = os.getenv("JWT_SECRET_KEY", "dev-secret-CHANGE-IN-PROD")
    algorithm: str = "HS256"
    access_token_expire_hours: int = 24
    
    class Config:
        env_file = ".env"
```

---

## FRONTEND ARCHITECTURE

### Authentication Context

**AuthContext.jsx** (NEW):
```jsx
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));

  const login = async (email, password) => {
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const { access_token, user } = await response.json();
    setToken(access_token);
    setUser(user);
    localStorage.setItem('auth_token', access_token);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

### Authenticated API Requests

**useCRM.js** (MODIFY):
```jsx
import { useAuth } from '../contexts/AuthContext';

export function useLeads() {
  const { token } = useAuth();  // ✅ Get JWT from context
  
  return useQuery({
    queryKey: ['leads'],
    queryFn: async () => {
      const response = await fetch('/api/v1/crm/leads', {
        headers: {
          'Authorization': `Bearer ${token}`  // ✅ Add auth header
        }
      });
      return response.json();
    }
  });
}
```

---

## SECURITY CONSIDERATIONS

### 1. JWT Storage

**Options**:
- `localStorage`: ✅ Simple, survives page reload, ❌ Vulnerable to XSS
- `sessionStorage`: ✅ Cleared on tab close, ❌ Still vulnerable to XSS
- `httpOnly cookie`: ✅ XSS-safe, ❌ Requires CSRF protection

**Decision**: `localStorage` for MVP (Phase 4), migrate to httpOnly cookie Phase 5.

**Mitigation**: Sanitize all user inputs, CSP headers.

### 2. Password Storage

**Rules**:
- ❌ NEVER store plaintext passwords
- ✅ Use bcrypt with automatic salt (passlib default)
- ✅ Cost factor: 12 rounds (passlib default, ~200ms)
- ❌ NO custom password validation (defer Phase 5)

### 3. Rate Limiting

**Implementation**:
```python
@limiter.limit("5/minute")  # Public endpoint
@limiter.limit("100/minute")  # Authenticated endpoints
```

**Storage**: In-memory (MVP), migrate to Redis Phase 5.

### 4. SQL Injection

**Current**: ✅ Using SQLAlchemy ORM (safe by default)

**Rule**: ❌ NEVER use raw SQL with user input

---

## TESTING STRATEGY

### Unit Tests (Domain Layer)
- `test_lead_entity.py`: Lead creation with waiting_list source
- `test_auth_token_value_object.py`: JWT generation/validation

### Integration Tests (Infrastructure Layer)
- `test_lead_repository_filtering.py`: Test `find_all_except_source()`
- `test_user_repository_permissions.py`: Test `get_user_permissions()`

### API Tests (FastAPI TestClient)
- `test_auth_endpoints.py`: Login success/failure, JWT validation
- `test_public_endpoints.py`: Waiting list signup, rate limiting
- `test_protected_endpoints.py`: 401 without JWT, 200 with valid JWT
- `test_permission_filtering.py`: Admin sees all, Employee sees filtered

### E2E Tests (Playwright)
- `auth_flow.spec.js`: Login → Dashboard → Logout
- `waiting_list.spec.js`: Public form → Submit → Confirmation
- `permission_filtering.spec.js`: Admin sees waiting list, Employee doesn't

---

## EFFORT ESTIMATION

| Component | Complexity | Effort |
|-----------|------------|--------|
| Domain layer (value objects, repo interfaces) | LOW | 1h |
| Infrastructure (JWT, password hashing, repo impl) | MEDIUM | 3h |
| Application layer (use cases) | MEDIUM | 2h |
| API layer (auth endpoints, dependencies) | HIGH | 4h |
| Frontend (login form, auth context) | MEDIUM | 3h |
| Tests (unit, integration, E2E) | HIGH | 5h |
| Documentation | LOW | 1h |
| **TOTAL** | | **19h** |

**Critical Path**: API dependencies → Frontend auth → E2E tests

---

## RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| JWT secret leaked | CRITICAL | LOW | Use env vars, .gitignore .env |
| Rate limiting bypassed | HIGH | MEDIUM | Add IP + user_id combined limits Phase 5 |
| Password brute force | MEDIUM | MEDIUM | bcrypt slow hashing (200ms) limits attempts |
| Frontend XSS steals JWT | HIGH | LOW | CSP headers, input sanitization |
| 71 endpoints to protect | MEDIUM | HIGH | Automated test suite validates all endpoints |

---

## DEFERRED TO PHASE 5 (KISS)

❌ **Not implementing** (over-engineering):
- Email verification for waiting list (manual admin contact)
- Password reset flow (admin resets manually)
- Refresh tokens (24h expiry acceptable for MVP)
- OAuth2/SSO integration (Google, GitHub login)
- Session management DB (stateless JWT sufficient)
- Multi-factor authentication (MFA)
- Password complexity validation
- Account lockout after failed attempts
- Redis for rate limiting (in-memory OK for MVP)
- httpOnly cookie storage (localStorage OK for MVP)

---

## ARCHITECTURAL DECISION RECORDS (ADR)

### ADR-1: Dual-Mode API (Public vs Authenticated)

**Decision**: Create separate `/api/v1/public/*` router for unauthenticated endpoints.

**Rationale**:
- ✅ Clear separation of concerns (public vs private)
- ✅ Easy to apply different middleware (rate limiting, CORS)
- ✅ Explicit security boundary

**Alternatives Rejected**:
- ❌ Optional authentication (Depends(get_current_user_optional)) - Too complex
- ❌ Field-level permissions - Over-engineering

### ADR-2: Reuse Lead Entity for Waiting List

**Decision**: Use existing `Lead` aggregate with `source="waiting_list"`.

**Rationale**:
- ✅ DDD principle: Reuse aggregate over creating new entity
- ✅ Waiting list IS a type of lead (interested party, not yet customer)
- ✅ No database migration needed

**Alternatives Rejected**:
- ❌ Separate `WaitingList` table - Duplicate concept
- ❌ Polymorphic `Contact` entity - Over-abstraction

### ADR-3: Flat Permission Model

**Decision**: Store permissions as flat JSONB array in `roles.permissions`.

**Rationale**:
- ✅ KISS: Simple to query, simple to check
- ✅ Database already supports (no migration)
- ✅ Flexible (easy to add new permissions)

**Alternatives Rejected**:
- ❌ Hierarchical roles (Admin > Manager > Employee) - Over-engineering
- ❌ Row-level security in PostgreSQL - Complexity

### ADR-4: JWT in localStorage (MVP)

**Decision**: Store JWT in `localStorage` for Phase 4, migrate to httpOnly cookie Phase 5.

**Rationale**:
- ✅ Simple implementation (no cookie management)
- ✅ Works with CORS (no cookie issues)
- ⚠️ XSS risk mitigated by CSP headers

**Alternatives Rejected**:
- ❌ httpOnly cookie - Requires CSRF protection (Phase 5)
- ❌ sessionStorage - Lost on page reload (bad UX)

---

## REFERENCES

**Research Sources**:
- FastAPI Security Documentation: https://fastapi.tiangolo.com/tutorial/security/
- python-jose Library: https://github.com/mpdavis/python-jose
- slowapi Rate Limiting: https://github.com/laurentS/slowapi
- OWASP JWT Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

**Code References**:
- Existing Identity Module: `backend/src/erp/domain/identity/`
- Current CRM Routes: `backend/src/erp/api/routes/crm.py`
- Frontend User Context: `frontend/src/contexts/UserContext.jsx`
- Database Schema: `init.sql`
