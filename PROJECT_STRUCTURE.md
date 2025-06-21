# 📁 FastAPI Starter Project - Structure Documentation

## 📋 Overview

This FastAPI starter project follows a well-organized, modular architecture designed for scalability and maintainability. The project implements a modern Python web API using FastAPI, with PostgreSQL for data persistence, Redis for caching, and Docker for containerization.

---

## 🏗️ Root Directory Structure

```
fastapi-starter-project/
├── 📁 app/                    # Main application code
├── 📁 alembic/               # Database migration management
├── 📁 tests/                 # Test suite
├── 📁 .git/                  # Git version control
├── 📁 .mypy_cache/           # MyPy type checker cache
├── 📁 .ruff_cache/           # Ruff linter cache
├── 📁 .venv/                 # Python virtual environment
├── 📄 pyproject.toml         # Project configuration and dependencies
├── 📄 README.md              # Setup and workflow documentation
├── 📄 docker-compose.yml     # Multi-container Docker application
├── 📄 Dockerfile             # Docker image build instructions
├── 📄 alembic.ini            # Alembic migration configuration
├── 📄 requirements.txt       # Python dependencies (legacy format)
├── 📄 uv.lock                # UV dependency lock file
├── 📄 .env                   # Environment variables
├── 📄 .gitignore             # Git ignore patterns
├── 📄 .dockerignore          # Docker ignore patterns
├── 📄 .pre-commit-config.yaml # Pre-commit hooks configuration
└── 📄 .python-version        # Python version specification
```

---

## 📂 Detailed Directory Descriptions

### 🚀 `/app` - Main Application Directory

The heart of the FastAPI application containing all business logic and API implementation.

```
app/
├── 📄 __init__.py           # Package initialization
├── 📄 main.py               # FastAPI application entry point
├── 📄 config.py             # Application configuration and settings
├── 📄 database.py           # Database connection and session management
├── 📄 cache.py              # Redis cache configuration and utilities
├── 📄 oauth2.py             # OAuth2 authentication logic (placeholder)
├── 📄 roles.py              # User roles and permissions (placeholder)
├── 📄 utils.py              # Common utility functions (placeholder)
├── 📁 controllers/          # Business logic controllers
├── 📁 dependencies/         # FastAPI dependency injection
├── 📁 exceptions/           # Custom exception classes
├── 📁 middlewares/          # Custom middleware components
├── 📁 models/               # SQLAlchemy database models
├── 📁 routers/              # FastAPI route handlers
└── 📁 schemas/              # Pydantic data validation schemas
```

#### 📄 Core Application Files

- **`main.py`**: The FastAPI application instance and root endpoint. Configures logging and custom OpenAPI documentation.
- **`config.py`**: Centralized configuration management using Pydantic settings for environment variables and app configuration.
- **`database.py`**: SQLAlchemy database engine, session factory, and connection management.
- **`cache.py`**: Redis connection setup and caching utilities for performance optimization.

#### 📁 Application Modules

- **`controllers/`**: Contains business logic separated from route handlers. Implements the controller layer of the MVC pattern.
- **`dependencies/`**: FastAPI dependency injection functions for authentication, database sessions, and shared logic.
- **`exceptions/`**: Custom exception classes for specific error handling and API error responses.
- **`middlewares/`**: Custom middleware for cross-cutting concerns like CORS, authentication, logging, and request processing.
- **`models/`**: SQLAlchemy ORM models defining database table structures and relationships.
- **`routers/`**: FastAPI router modules organizing API endpoints by feature or domain.
- **`schemas/`**: Pydantic models for request/response validation, serialization, and API documentation.

### 🗃️ `/alembic` - Database Migration Management

Handles database schema versioning and migrations using Alembic.

```
alembic/
├── 📄 env.py                # Alembic environment configuration
├── 📄 script.py.mako        # Migration script template
├── 📄 README                # Alembic usage information
└── 📁 versions/             # Migration version files
    └── 📄 6717d9a15f4a_initial.py  # Initial database migration
```

- **`env.py`**: Configures Alembic environment, database connection, and migration context.
- **`script.py.mako`**: Template for generating new migration scripts.
- **`versions/`**: Contains chronologically ordered migration files that modify database schema.

### 🧪 `/tests` - Test Suite

Contains all automated tests for the application.

```
tests/
└── 📄 test_main.py          # Basic application tests
```

Currently contains basic tests for the main application. This directory should be expanded with:
- Unit tests for individual components
- Integration tests for API endpoints
- Database tests for model operations
- Authentication and authorization tests

### 🐳 **Containerization Files**

#### 📄 `Dockerfile`
Defines the Docker image build process:
- Sets up Python 3.12 environment
- Installs system dependencies
- Copies application code
- Configures the container runtime

#### 📄 `docker-compose.yml`
Orchestrates multi-container application with services:
- **`db`**: PostgreSQL 15 database with health checks
- **`redis`**: Redis 7 cache server with password authentication
- **`alembic`**: Database migration runner with conditional logic
- **`app`**: Main FastAPI application server

#### 📄 `.dockerignore`
Excludes unnecessary files from Docker build context for faster builds and smaller images.

---

## 🐳 How Docker Works in This Project

This section explains the complete Docker implementation and workflow for this FastAPI starter project.

### 🏗️ **Docker Architecture Overview**

The project uses a **multi-container architecture** with four interconnected services:

```
┌─────────────────────────────────────────────────────┐
│                Docker Network                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │   App    │  │ Alembic  │  │PostgreSQL│  │Redis │ │
│  │Container │  │Container │  │Container │  │Cache │ │
│  │:5000     │  │          │  │:5432     │  │:6379 │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────┘ │
└─────────────────────────────────────────────────────┘
```

### 📋 **Dockerfile Breakdown**

The `Dockerfile` creates an optimized Python container:

```dockerfile
FROM python:3.12-slim                    # Lightweight Python base image
ENV PYTHONDONTWRITEBYTECODE=1            # Prevents .pyc file generation
    PYTHONUNBUFFERED=1                   # Ensures stdout/stderr are unbuffered
    PYTHONFAULTHANDLER=1                 # Enables fault handler for debugging

WORKDIR /app                             # Sets working directory

# Install UV package manager for faster dependency resolution
COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /uvx /bin/

# Copy dependency files first (Docker layer caching optimization)
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-cache          # Install dependencies

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code (separate layer for better caching)
COPY . .

# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--port", "5000", "--host", "0.0.0.0"]
```

#### 🎯 **Key Dockerfile Optimizations**

1. **Layer Caching**: Dependencies are installed before copying application code
2. **UV Package Manager**: Faster dependency resolution than pip
3. **Slim Base Image**: Reduces container size and attack surface
4. **Environment Variables**: Optimizes Python runtime behavior
5. **Virtual Environment**: Isolated dependency management

### 🔄 **Docker Compose Service Orchestration**

#### 🗄️ **PostgreSQL Database Service (`db`)**
```yaml
db:
  image: postgres:15                     # Official PostgreSQL image
  restart: on-failure                    # Auto-restart on crashes
  ports: ['5432:5432']                   # Port mapping
  environment:                           # Database configuration
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
    POSTGRES_DB: ${POSTGRES_DB:-fastapi}
  volumes:
    - postgres-db:/var/lib/postgresql/data  # Persistent data storage
  healthcheck:                           # Health monitoring
    test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
    interval: 10s
    timeout: 5s
    retries: 5
```

#### 🚀 **Redis Cache Service (`redis`)**
```yaml
redis:
  image: redis:7                         # Official Redis image
  restart: on-failure
  ports: ['6379:6379']
  command: bash -c 'redis-server --requirepass ${REDIS_PASSWORD:-password}'
  environment:
    REDIS_PASSWORD: ${REDIS_PASSWORD:-password}
  volumes:
    - cache:/data                        # Persistent cache storage
```

#### 🔄 **Alembic Migration Service (`alembic`)**
```yaml
alembic:
  build: .                               # Uses project Dockerfile
  depends_on:
    db:
      condition: service_healthy         # Waits for database health check
  environment:                           # Migration configuration
    MAKE_MIGRATIONS: ${MAKE_MIGRATIONS:-false}
    MAKE_MIGRATION_DOWNGRADE: ${MAKE_MIGRATION_DOWNGRADE:-false}
  command: >                             # Conditional migration logic
    sh -c "[ "$MAKE_MIGRATIONS" = "true" ] && alembic revision --autogenerate;
           [ "$MAKE_MIGRATION_DOWNGRADE" = "true" ] && alembic downgrade;
           [ "$MAKE_MIGRATION_DOWNGRADE" != "true" ] && alembic upgrade head"
```

#### 🌐 **FastAPI Application Service (`app`)**
```yaml
app:
  build: .                               # Uses project Dockerfile
  restart: on-failure
  container_name: fastapi_app
  ports: ["5001:5000"]                   # Maps host:5001 to container:5000
  depends_on: [redis, db, alembic]       # Service dependencies
  environment:                           # Application configuration
    - Database and Redis connection variables
```

### 🔗 **Service Communication & Networking**

#### 🌐 **Docker Network**
- **Network Name**: `app_network` (bridge driver)
- **Internal DNS**: Services communicate using service names (`db`, `redis`, `app`)
- **Port Isolation**: Internal container ports are isolated from host

#### 📡 **Service Discovery**
```python
# In application code, services are referenced by name:
DATABASE_URL = "postgresql://user:pass@db:5432/fastapi"
REDIS_URL = "redis://:password@redis:6379"
```

### 💾 **Data Persistence**

#### 📊 **Named Volumes**
- **`postgres-db`**: Persists PostgreSQL database files
- **`cache`**: Persists Redis cache data across container restarts

#### 🔄 **Volume Mounting**
- **Alembic files**: `./alembic:/app/alembic` (for migration development)
- **Configuration**: `./alembic.ini:/app/alembic.ini`

### 🚀 **Docker Workflow Commands**

#### 🏃 **Development Workflow**
```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Build and start (after code changes)
docker compose up --build

# View logs
docker compose logs -f app

# Stop all services
docker compose down

# Stop and remove volumes (complete reset)
docker compose down -v
```

#### 🔧 **Database Migration Workflow**
```bash
# Create new migration
MAKE_MIGRATIONS=true docker compose up alembic

# Apply migrations
docker compose up alembic

# Rollback migration
MAKE_MIGRATION_DOWNGRADE=true MIGRATION_DOWNGRADE_TARGET=<revision> docker compose up alembic
```

#### 🐛 **Debugging & Maintenance**
```bash
# Execute commands in running container
docker compose exec app bash

# View container status
docker compose ps

# Restart specific service
docker compose restart app

# View resource usage
docker stats
```

### 🔒 **Environment Configuration**

#### 📝 **Environment Variables**
The `.env` file configures all services:
```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=fastapi
POSTGRES_HOST=db
DATABASE_PORT=5432

# Redis Configuration
REDIS_PASSWORD=password
REDIS_HOST=redis
REDIS_PORT=6379

# Migration Control
MAKE_MIGRATIONS=false
MAKE_MIGRATION_DOWNGRADE=false
```

### 🎯 **Benefits of This Docker Setup**

#### ✅ **Development Benefits**
- **Consistent Environment**: Same setup across all developer machines
- **Quick Setup**: Single command to start entire stack
- **Isolation**: No conflicts with local installations
- **Easy Reset**: Quick environment cleanup and rebuild

#### 🚀 **Production Benefits**
- **Scalability**: Easy horizontal scaling of services
- **Reliability**: Health checks and auto-restart policies
- **Security**: Isolated network and controlled access
- **Portability**: Runs identically across different environments

#### 🔧 **Operational Benefits**
- **Monitoring**: Built-in health checks and logging
- **Backup**: Persistent volumes for data safety
- **Updates**: Rolling updates with zero downtime
- **Debugging**: Easy access to container internals

### 🎛️ **Advanced Docker Features Used**

#### 🏥 **Health Checks**
- PostgreSQL health check ensures database readiness
- Prevents application startup before database is available
- Automatic service restart on health check failures

#### 🔄 **Dependency Management**
- Service startup order controlled by `depends_on`
- Conditional logic in Alembic service for flexible migrations
- Environment-based configuration for different deployment scenarios

#### 📦 **Multi-stage Optimization**
- UV package manager for faster builds
- Layer caching optimization in Dockerfile
- Minimal base image for security and performance

This Docker setup provides a robust, scalable foundation for both development and production deployments of the FastAPI application.

---

## 🔧 How Docker Compose Works in This Project

This section provides an in-depth explanation of the Docker Compose orchestration specifically used in this FastAPI starter project.

### 📋 **Docker Compose File Structure**

The `docker-compose.yml` file defines a complete multi-service application stack:

```yaml
# docker-compose.yml structure overview
services:          # Defines all application services
  db:             # PostgreSQL database service
  redis:          # Redis cache service
  alembic:        # Database migration service
  app:            # FastAPI application service

volumes:          # Persistent data storage
  postgres-db:    # Database files
  cache:          # Redis cache data

networks:         # Service communication
  app_network:    # Custom bridge network
```

### 🔄 **Service Orchestration Flow**

Docker Compose manages the startup sequence and dependencies:

```
1. Network Creation: app_network (bridge)
   ↓
2. Volume Creation: postgres-db, cache
   ↓
3. Database Startup: PostgreSQL container
   ↓
4. Health Check: Wait for database readiness
   ↓
5. Redis Startup: Cache service initialization
   ↓
6. Migration Service: Alembic runs database migrations
   ↓
7. Application Startup: FastAPI server starts
```

### 🗄️ **Database Service Deep Dive**

The PostgreSQL service configuration:

```yaml
db:
  image: postgres:15                    # Uses official PostgreSQL 15 image
  restart: on-failure                   # Restart policy for resilience
  ports:
    - '5432:5432'                      # Host:Container port mapping
  environment: &db-variables            # Environment variables with YAML anchor
    POSTGRES_USER: ${POSTGRES_USER:-postgres}      # Default fallback values
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
    POSTGRES_DB: ${POSTGRES_DB:-fastapi}
    POSTGRES_HOST: ${POSTGRES_HOST:-db}
    DATABASE_PORT: ${DATABASE_PORT:-5432}
  volumes:
    - postgres-db:/var/lib/postgresql/data  # Named volume for data persistence
  networks:
    - app_network                      # Connects to custom network
  healthcheck:                         # Health monitoring configuration
    test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
    interval: 10s                      # Check every 10 seconds
    timeout: 5s                        # 5 second timeout per check
    retries: 5                         # 5 failed attempts before unhealthy
```

#### 🎯 **Database Service Features**
- **Environment Variables**: Uses YAML anchors (`&db-variables`) for reusability
- **Default Values**: `${VAR:-default}` syntax provides fallback values
- **Health Checks**: `pg_isready` command ensures database is accepting connections
- **Data Persistence**: Named volume survives container recreation
- **Network Isolation**: Only accessible within the Docker network

### 🚀 **Redis Cache Service Analysis**

```yaml
redis:
  image: redis:7                        # Official Redis 7 image
  restart: on-failure
  ports:
    - '6379:6379'                      # Standard Redis port
  command: bash -c 'redis-server --requirepass ${REDIS_PASSWORD:-password}'
  environment: &redis-variables         # Another YAML anchor for reuse
    REDIS_PASSWORD: ${REDIS_PASSWORD:-password}
    REDIS_HOST: ${REDIS_HOST:-redis}
    REDIS_PORT: ${REDIS_PORT:-6379}
  volumes:
    - cache:/data                      # Persistent cache storage
  networks:
    - app_network
```

#### 🔑 **Redis Service Features**
- **Password Authentication**: Custom command with `--requirepass` flag
- **Data Persistence**: RDB snapshots saved to named volume
- **Configuration Override**: Custom command replaces default Redis startup
- **Environment Reuse**: YAML anchor allows sharing variables with other services

### 🔄 **Alembic Migration Service Breakdown**

The most complex service with conditional logic:

```yaml
alembic:
  build:
    context: .                         # Build from current directory
    dockerfile: Dockerfile             # Uses same Dockerfile as app
  depends_on:
    db:
      condition: service_healthy       # Waits for database health check to pass
  environment:                         # Inherits both database and Redis variables
    <<:                               # YAML merge operator
      - *db-variables                 # Merges database environment
      - *redis-variables              # Merges Redis environment
    MAKE_MIGRATIONS: ${MAKE_MIGRATIONS:-false}
    MAKE_MIGRATION_DOWNGRADE: ${MAKE_MIGRATION_DOWNGRADE:-false}
    MIGRATION_DOWNGRADE_TARGET: ${MIGRATION_DOWNGRADE_TARGET:-63017c98c3da}
  command: >                          # Multi-line command with conditional logic
    sh -c "[ \"$MAKE_MIGRATIONS\" = \"true\" ] && alembic revision --autogenerate -m 'auto detect changes';
           [ \"$MAKE_MIGRATION_DOWNGRADE\" = \"true\" ] && alembic downgrade \"$MIGRATION_DOWNGRADE_TARGET\";
           [ \"$MAKE_MIGRATION_DOWNGRADE\" != \"true\" ] && alembic upgrade head"
  volumes:
    - ./alembic:/app/alembic            # Mount local alembic directory
    - ./alembic.ini:/app/alembic.ini    # Mount configuration file
  networks:
    - app_network
```

#### 🎛️ **Alembic Service Logic**
The command uses shell conditional statements:
1. **If** `MAKE_MIGRATIONS=true`: Creates new migration files
2. **Else If** `MAKE_MIGRATION_DOWNGRADE=true`: Rolls back to specific revision
3. **Else**: Applies all pending migrations (default behavior)

#### 📁 **Volume Mounting Strategy**
- **Development**: Local `alembic/` folder is mounted for live editing
- **Configuration**: `alembic.ini` is mounted for consistent settings
- **Persistence**: Migration files created in container appear locally

### 🌐 **FastAPI Application Service**

```yaml
app:
  build:
    context: .                         # Build from project root
    dockerfile: Dockerfile
  restart: on-failure
  container_name: fastapi_app          # Fixed container name for easy reference
  ports:
    - "5001:5000"                     # Maps host port 5001 to container port 5000
  environment:                        # Inherits all environment variables
    <<:
      - *db-variables
      - *redis-variables
  depends_on:                         # Service dependencies
    - redis                           # Requires Redis to be running
    - db                              # Requires database to be running
    - alembic                         # Requires migrations to be complete
  networks:
    - app_network
```

#### 🔗 **Application Dependencies**
- **Database**: Must be healthy before app starts
- **Redis**: Cache service must be available
- **Alembic**: Migrations must complete successfully
- **Network**: All services communicate via `app_network`

### 🌐 **Network Configuration**

```yaml
networks:
  app_network:
    driver: bridge                     # Bridge network type
```

#### 📡 **Network Features**
- **Service Discovery**: Services can reach each other by name (`db`, `redis`, `app`)
- **Isolation**: Network traffic is isolated from host and other Docker networks
- **DNS Resolution**: Docker provides automatic DNS for service names
- **Port Security**: Internal ports are not exposed unless explicitly mapped

### 💾 **Volume Management**

```yaml
volumes:
  postgres-db:                        # Named volume for database
  cache:                              # Named volume for Redis
    driver: local                     # Local storage driver
```

#### 📊 **Volume Benefits**
- **Data Persistence**: Survives container recreation and updates
- **Performance**: Better I/O performance than bind mounts
- **Portability**: Can be backed up and restored easily
- **Isolation**: Separate from host filesystem

### 🔄 **YAML Advanced Features Used**

#### 🏷️ **YAML Anchors and Aliases**
```yaml
environment: &db-variables            # Anchor definition
  POSTGRES_USER: postgres
  # ... other variables

# Later reused with alias
environment:
  <<: *db-variables                   # Merge all anchor variables
```

#### 🔀 **YAML Merge Operator**
```yaml
environment:
  <<:                                 # Merge operator
    - *db-variables                   # Merge database variables
    - *redis-variables                # Merge Redis variables
  CUSTOM_VAR: value                   # Add additional variables
```

### 🚀 **Docker Compose Command Workflows**

#### 🏃 **Development Commands**
```bash
# Start all services with logs
docker compose up

# Start specific service
docker compose up db redis

# Start in detached mode (background)
docker compose up -d

# Force rebuild and start
docker compose up --build

# Scale specific service
docker compose up --scale app=3
```

#### 🔧 **Migration Workflows**
```bash
# Run standard migrations
docker compose up alembic

# Create new migration
MAKE_MIGRATIONS=true docker compose up alembic

# Rollback to specific revision
MAKE_MIGRATION_DOWNGRADE=true MIGRATION_DOWNGRADE_TARGET=abc123 docker compose up alembic

# Run migration in isolation
docker compose run --rm alembic alembic upgrade head
```

#### 🐛 **Debugging and Maintenance**
```bash
# View service status
docker compose ps

# Follow logs for specific service
docker compose logs -f app

# Execute command in running container
docker compose exec app bash

# Run one-off command
docker compose run --rm app python -c "print('Hello')"

# Restart specific service
docker compose restart app

# View resource usage
docker compose top
```

#### 🧹 **Cleanup Commands**
```bash
# Stop all services
docker compose down

# Stop and remove volumes (data loss!)
docker compose down -v

# Stop and remove images
docker compose down --rmi all

# Complete cleanup
docker compose down -v --rmi all --remove-orphans
```

### 🔒 **Environment Variable Management**

#### 📝 **Variable Sources (Priority Order)**
1. **Shell Environment**: `export POSTGRES_USER=myuser`
2. **`.env` File**: `POSTGRES_USER=myuser`
3. **Docker Compose File**: `POSTGRES_USER: myuser`
4. **Default Values**: `${POSTGRES_USER:-postgres}`

#### 🎯 **Best Practices**
- **Sensitive Data**: Use `.env` file (excluded from Git)
- **Default Values**: Always provide sensible defaults
- **Documentation**: Comment environment variables in compose file
- **Validation**: Check required variables at startup

### 🎛️ **Advanced Docker Compose Features**

#### 🏥 **Health Check Integration**
```yaml
depends_on:
  db:
    condition: service_healthy         # Waits for health check to pass
```

#### 🔄 **Conditional Service Logic**
The Alembic service demonstrates advanced conditional execution:
- Uses shell scripting within Docker Compose
- Environment-driven behavior modification
- Multiple execution paths in single service

#### 📦 **Build Context Management**
```yaml
build:
  context: .                          # Build context (project root)
  dockerfile: Dockerfile              # Custom Dockerfile location
  args:                               # Build-time arguments
    BUILD_ENV: development
```

### 🎯 **Benefits of This Docker Compose Setup**

#### ✅ **Development Benefits**
- **Single Command Setup**: `docker compose up` starts entire stack
- **Environment Consistency**: Same setup across all machines
- **Service Isolation**: Each service runs in isolated container
- **Easy Testing**: Can start/stop individual services for testing

#### 🚀 **Production Benefits**
- **Scalability**: Easy to scale individual services
- **Monitoring**: Built-in health checks and restart policies
- **Configuration Management**: Environment-based configuration
- **Deployment Consistency**: Same compose file for different environments

#### 🔧 **Operational Benefits**
- **Log Aggregation**: Centralized logging with `docker compose logs`
- **Service Discovery**: Automatic DNS resolution between services
- **Volume Management**: Persistent data with named volumes
- **Network Security**: Isolated network with controlled access

### 🚨 **Common Docker Compose Pitfalls and Solutions**

#### ⚠️ **Service Startup Order**
**Problem**: App starts before database is ready
**Solution**: Use health checks and `depends_on` with conditions

#### ⚠️ **Environment Variable Conflicts**
**Problem**: Variables not loading correctly
**Solution**: Check precedence order and use explicit defaults

#### ⚠️ **Volume Permissions**
**Problem**: Permission denied errors with mounted volumes
**Solution**: Match user IDs or use named volumes instead of bind mounts

#### ⚠️ **Network Connectivity**
**Problem**: Services can't communicate
**Solution**: Ensure all services are on same network and use service names

This Docker Compose configuration provides a robust, scalable foundation for both development and production deployments, with careful attention to service orchestration, data persistence, and operational requirements.

---

## 🗃️ How Alembic Works in This Project

This section provides a comprehensive explanation of how Alembic database migration system is implemented and integrated into this FastAPI starter project.

### 📋 **Alembic Overview**

Alembic is SQLAlchemy's database migration tool that provides:
- **Version Control**: Track database schema changes over time
- **Automated Migrations**: Generate migration scripts from model changes
- **Rollback Support**: Ability to downgrade to previous schema versions
- **Environment Management**: Support for different deployment environments

### 🏗️ **Alembic Architecture in This Project**

```
┌─────────────────────────────────────────────────────┐
│                Alembic Workflow                      │
│                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │   Models    │───▶│  Migration  │───▶│Database │ │
│  │(app/models) │    │   Scripts   │    │ Schema  │ │
│  │             │    │(versions/)  │    │         │ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
│         │                   │                │     │
│         │                   │                │     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │ alembic.ini │    │   env.py    │    │Revision │ │
│  │(Config)     │    │(Environment)│    │ Table   │ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
└─────────────────────────────────────────────────────┘
```

### 📄 **Alembic Configuration Files**

#### 🔧 **`alembic.ini` - Main Configuration**

```ini
[alembic]
script_location = alembic                    # Location of migration scripts
prepend_sys_path = .                        # Add current directory to Python path

# Database connection URL with environment variables
sqlalchemy.url = postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${DATABASE_PORT}/${POSTGRES_DB}

# File naming and versioning
version_path_separator = os                 # Use OS path separator
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

[loggers]
keys = root,sqlalchemy,alembic             # Logging configuration

[logger_alembic]
level = INFO                               # Alembic log level
handlers =
qualname = alembic
```

#### 🎯 **Key Configuration Features**
- **Environment Variables**: Database URL uses Docker environment variables
- **Script Location**: Migration files stored in `alembic/` directory
- **Logging**: Configured for INFO level Alembic logging
- **Path Management**: Current directory added to Python path for imports

#### 🌐 **`alembic/env.py` - Environment Setup**

```python
from logging.config import fileConfig
from alembic import context
from app.database import SQLALCHEMY_DATABASE_URL  # Import database URL
from app.models import Base                       # Import SQLAlchemy Base
from sqlalchemy import engine_from_config, pool

# Alembic Config object
config = context.config

# Override database URL from application configuration
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

# Configure logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (SQL script generation)."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (direct database execution)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,  # No connection pooling for migrations
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine execution mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

#### 🔑 **Environment Configuration Features**
- **Dynamic Database URL**: Imports from application configuration
- **Metadata Integration**: Uses SQLAlchemy Base metadata for autogenerate
- **Dual Mode Support**: Online (direct DB) and offline (SQL script) execution
- **Connection Management**: Proper connection handling with NullPool

### 📁 **Migration Files Structure**

#### 🗂️ **`alembic/versions/` Directory**
```
alembic/versions/
└── 6717d9a15f4a_initial.py              # Initial migration file
```

#### 📄 **Migration File Anatomy**
```python
"""initial                                # Migration description

Revision ID: 6717d9a15f4a                # Unique revision identifier
Revises:                                 # Previous revision (None for initial)
Create Date: 2025-04-03 16:22:27.659679  # Creation timestamp
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers used by Alembic
revision: str = '6717d9a15f4a'           # Current revision ID
down_revision: Union[str, None] = None    # Previous revision ID
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Apply forward migration changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('users',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('email', sa.String(), nullable=False),
    #     sa.PrimaryKeyConstraint('id')
    # )
    pass
    # ### end Alembic commands ###

def downgrade() -> None:
    """Apply reverse migration changes."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('users')
    pass
    # ### end Alembic commands ###
```

### 🔄 **Alembic Integration with Docker Compose**

#### 🐳 **Alembic Service Configuration**
```yaml
alembic:
  build: .                               # Uses project Dockerfile
  depends_on:
    db:
      condition: service_healthy         # Waits for database readiness
  environment:
    <<:                                 # Inherits environment variables
      - *db-variables                   # Database connection details
      - *redis-variables                # Redis configuration
    MAKE_MIGRATIONS: ${MAKE_MIGRATIONS:-false}
    MAKE_MIGRATION_DOWNGRADE: ${MAKE_MIGRATION_DOWNGRADE:-false}
    MIGRATION_DOWNGRADE_TARGET: ${MIGRATION_DOWNGRADE_TARGET:-63017c98c3da}
  command: >                            # Conditional migration logic
    sh -c "[ \"$MAKE_MIGRATIONS\" = \"true\" ] && alembic revision --autogenerate -m 'auto detect changes';
           [ \"$MAKE_MIGRATION_DOWNGRADE\" = \"true\" ] && alembic downgrade \"$MIGRATION_DOWNGRADE_TARGET\";
           [ \"$MAKE_MIGRATION_DOWNGRADE\" != \"true\" ] && alembic upgrade head"
  volumes:
    - ./alembic:/app/alembic            # Mount local alembic directory
    - ./alembic.ini:/app/alembic.ini    # Mount configuration file
```

#### 🎛️ **Conditional Migration Logic**

The Docker Compose service implements three migration modes:

1. **Standard Migration (Default)**:
   ```bash
   alembic upgrade head
   ```
   - Applies all pending migrations to the latest revision
   - Default behavior when no special flags are set

2. **Create New Migration**:
   ```bash
   MAKE_MIGRATIONS=true docker compose up alembic
   # Executes: alembic revision --autogenerate -m 'auto detect changes'
   ```
   - Compares current models with database schema
   - Generates new migration file with detected changes

3. **Rollback Migration**:
   ```bash
   MAKE_MIGRATION_DOWNGRADE=true MIGRATION_DOWNGRADE_TARGET=abc123 docker compose up alembic
   # Executes: alembic downgrade abc123
   ```
   - Rolls back database to specified revision
   - Useful for undoing problematic migrations

### 🚀 **Alembic Workflow Commands**

#### 🏃 **Development Workflow**

##### 📝 **Creating New Migrations**
```bash
# Method 1: Using Docker Compose
MAKE_MIGRATIONS=true docker compose up alembic

# Method 2: Direct command in container
docker compose run --rm alembic alembic revision --autogenerate -m "add user table"

# Method 3: Local development (if running locally)
alembic revision --autogenerate -m "add user table"
```

##### ⬆️ **Applying Migrations**
```bash
# Apply all pending migrations
docker compose up alembic

# Apply to specific revision
docker compose run --rm alembic alembic upgrade abc123

# Apply one migration at a time
docker compose run --rm alembic alembic upgrade +1
```

##### ⬇️ **Rolling Back Migrations**
```bash
# Rollback to specific revision
MAKE_MIGRATION_DOWNGRADE=true MIGRATION_DOWNGRADE_TARGET=abc123 docker compose up alembic

# Rollback one migration
docker compose run --rm alembic alembic downgrade -1

# Rollback to base (empty database)
docker compose run --rm alembic alembic downgrade base
```

#### 🔍 **Migration Information Commands**
```bash
# View current revision
docker compose run --rm alembic alembic current

# View migration history
docker compose run --rm alembic alembic history

# View pending migrations
docker compose run --rm alembic alembic heads

# Show specific migration details
docker compose run --rm alembic alembic show abc123
```

#### 🧪 **Testing and Validation**
```bash
# Test migration without applying (offline mode)
docker compose run --rm alembic alembic upgrade head --sql

# Validate current database state
docker compose run --rm alembic alembic current --verbose

# Check for branches in migration history
docker compose run --rm alembic alembic branches
```

### 🔄 **Alembic Migration Lifecycle**

#### 1️⃣ **Model Changes**
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.models import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)  # New field added
```

#### 2️⃣ **Generate Migration**
```bash
MAKE_MIGRATIONS=true docker compose up alembic
```

Generated migration file:
```python
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
```

#### 3️⃣ **Review and Edit**
```python
def upgrade() -> None:
    # Add the column as nullable first
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))

    # Set default values for existing records
    op.execute("UPDATE users SET name = 'Unknown' WHERE name IS NULL")

    # Make the column non-nullable
    op.alter_column('users', 'name', nullable=False)

def downgrade() -> None:
    op.drop_column('users', 'name')
```

#### 4️⃣ **Apply Migration**
```bash
docker compose up alembic
```

### 🎯 **Alembic Best Practices in This Project**

#### ✅ **Migration Safety**
- **Review Generated Migrations**: Always review auto-generated migrations
- **Test Rollbacks**: Ensure downgrade functions work correctly
- **Data Migration**: Handle existing data when changing schema
- **Backup Before Major Changes**: Create database backups before complex migrations

#### 🔧 **Development Workflow**
- **Incremental Changes**: Create small, focused migrations
- **Descriptive Names**: Use meaningful migration descriptions
- **Version Control**: Commit migration files with code changes
- **Team Coordination**: Communicate schema changes to team members

#### 🛡️ **Production Considerations**
- **Staging Tests**: Test migrations in staging environment first
- **Rollback Plans**: Always have a rollback strategy
- **Downtime Planning**: Plan for potential downtime during migrations
- **Monitoring**: Monitor database performance after migrations

### 🎛️ **Advanced Alembic Features**

#### 🔀 **Branching and Merging**
```bash
# Create branch for feature development
docker compose run --rm alembic alembic revision --branch-label feature_branch -m "feature migration"

# Merge branches
docker compose run --rm alembic alembic merge -m "merge feature branch" head1 head2
```

#### 📊 **Custom Migration Operations**
```python
def upgrade() -> None:
    # Custom SQL execution
    op.execute("CREATE INDEX CONCURRENTLY idx_users_email ON users(email)")

    # Bulk data operations
    connection = op.get_bind()
    connection.execute(
        text("UPDATE users SET status = 'active' WHERE created_at > :date"),
        {"date": datetime.now() - timedelta(days=30)}
    )

    # Custom Python logic
    from app.models import User
    session = Session(bind=connection)
    users = session.query(User).filter(User.email.is_(None)).all()
    for user in users:
        user.email = f"user_{user.id}@example.com"
    session.commit()
```

#### 🌍 **Environment-Specific Migrations**
```python
def upgrade() -> None:
    # Check environment and apply different logic
    import os
    if os.getenv('ENVIRONMENT') == 'production':
        # Production-specific migration
        op.create_index('idx_users_email', 'users', ['email'], unique=True)
    else:
        # Development-specific migration
        op.create_index('idx_users_email', 'users', ['email'])
```

### 🚨 **Common Alembic Issues and Solutions**

#### ⚠️ **Migration Conflicts**
**Problem**: Multiple developers create migrations simultaneously
**Solution**:
```bash
# Merge conflicting heads
docker compose run --rm alembic alembic merge -m "merge conflict resolution" head1 head2
```

#### ⚠️ **Model Import Errors**
**Problem**: Cannot import models in migration
**Solution**: Use direct SQL or table reflection
```python
def upgrade() -> None:
    # Instead of importing models, use table reflection
    from sqlalchemy import MetaData, Table
    metadata = MetaData()
    users_table = Table('users', metadata, autoload_with=op.get_bind())
```

#### ⚠️ **Database State Mismatch**
**Problem**: Database schema doesn't match migration history
**Solution**:
```bash
# Stamp database with current revision without applying migrations
docker compose run --rm alembic alembic stamp head

# Or reset and reapply all migrations
docker compose run --rm alembic alembic downgrade base
docker compose run --rm alembic alembic upgrade head
```

#### ⚠️ **Large Table Migrations**
**Problem**: Migration takes too long on large tables
**Solution**: Use online schema change tools or break into smaller steps
```python
def upgrade() -> None:
    # Add column as nullable first
    op.add_column('large_table', sa.Column('new_field', sa.String(), nullable=True))

    # Update in batches (implement in separate migration)
    # Make non-nullable in another migration after data population
```

### 📈 **Alembic Monitoring and Maintenance**

#### 📊 **Migration Tracking**
- **Revision Table**: Alembic maintains `alembic_version` table
- **History Tracking**: All applied migrations are recorded
- **State Verification**: Current database state can be verified

#### 🔧 **Regular Maintenance Tasks**
- **Clean Old Migrations**: Archive old migration files periodically
- **Performance Review**: Monitor migration execution times
- **Schema Validation**: Regularly validate database schema consistency
- **Backup Strategy**: Maintain migration-aware backup procedures

This comprehensive Alembic integration provides robust database schema management with version control, automated migration generation, and flexible deployment options through Docker Compose orchestration.

---

## 🛡️ How Pre-commit Works in This Project

This section provides a comprehensive explanation of how pre-commit hooks are implemented and integrated into this FastAPI starter project for automated code quality assurance.

### 📋 **Pre-commit Overview**

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks that:
- **Automated Quality Checks**: Runs code quality tools before each commit
- **Consistent Code Style**: Enforces consistent formatting and style across the team
- **Early Error Detection**: Catches issues before they reach the repository
- **Multi-language Support**: Works with various programming languages and tools

### 🏗️ **Pre-commit Architecture in This Project**

```
┌─────────────────────────────────────────────────────┐
│                Pre-commit Workflow                   │
│                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │    Git      │───▶│ Pre-commit  │───▶│ Quality │ │
│  │   Commit    │    │    Hooks    │    │  Tools  │ │
│  │             │    │             │    │         │ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
│         │                   │                │     │
│         │                   │                │     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │   Stage     │    │.pre-commit- │    │ Commit  │ │
│  │   Files     │    │ config.yaml │    │Success/ │ │
│  │             │    │             │    │ Failure │ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
└─────────────────────────────────────────────────────┘
```

### 📄 **Pre-commit Configuration File**

#### 🔧 **`.pre-commit-config.yaml` - Main Configuration**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-case-conflict          # Check for case conflicts
      - id: check-illegal-windows-names  # Check for Windows-illegal filenames
      - id: check-json                   # Validate JSON syntax
      - id: pretty-format-json           # Format JSON files
        args:
          - '--autofix'                  # Auto-fix formatting issues
          - '--indent=2'                 # Use 2-space indentation
          - '--no-sort-keys'             # Don't sort JSON keys
      - id: check-toml                   # Validate TOML syntax
      - id: check-yaml                   # Validate YAML syntax
      - id: check-merge-conflict         # Check for merge conflict markers
      - id: mixed-line-ending            # Fix mixed line endings
        args: ['--fix=lf']               # Use Unix line endings
      - id: name-tests-test              # Ensure test files follow naming convention
        args: ['--pytest-test-first']    # pytest naming convention
        exclude: '^app/tests/fixtures/'  # Exclude fixtures directory
      - id: end-of-file-fixer           # Ensure files end with newline
      - id: trailing-whitespace         # Remove trailing whitespace

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.13
    hooks:
      - id: ruff                        # Python linting
        args: [--fix]                   # Auto-fix issues when possible
      - id: ruff-format                 # Python code formatting

  - repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.401
    hooks:
      - id: pyright                     # Static type checking
```

### 🔍 **Hook Categories and Functions**

#### 🧹 **File Quality Hooks (`pre-commit-hooks`)**

##### 📁 **File System Checks**
- **`check-case-conflict`**: Prevents case-sensitive filename conflicts
  ```bash
  # Prevents issues like having both:
  # MyFile.py and myfile.py
  ```

- **`check-illegal-windows-names`**: Ensures cross-platform compatibility
  ```bash
  # Prevents Windows-reserved names like:
  # CON, PRN, AUX, NUL, COM1-9, LPT1-9
  ```

##### 📝 **File Format Validation**
- **`check-json`**: Validates JSON file syntax
  ```bash
  # Checks files like:
  # package.json, .vscode/settings.json
  ```

- **`pretty-format-json`**: Formats JSON files consistently
  ```json
  // Before:
  {"name":"value","nested":{"key":"value"}}

  // After:
  {
    "name": "value",
    "nested": {
      "key": "value"
    }
  }
  ```

- **`check-toml`**: Validates TOML syntax (pyproject.toml)
- **`check-yaml`**: Validates YAML syntax (docker-compose.yml, .pre-commit-config.yaml)

##### 🔀 **Git-specific Checks**
- **`check-merge-conflict`**: Detects unresolved merge conflicts
  ```bash
  # Finds patterns like:
  # <<<<<<< HEAD
  # =======
  # >>>>>>> branch
  ```

##### 📐 **Text Formatting**
- **`mixed-line-ending`**: Ensures consistent line endings (Unix LF)
- **`end-of-file-fixer`**: Adds newline at end of files
- **`trailing-whitespace`**: Removes trailing spaces and tabs

##### 🧪 **Test File Naming**
- **`name-tests-test`**: Enforces pytest naming conventions
  ```bash
  # Valid test files:
  # test_user.py, test_api.py
  # user_test.py, api_test.py

  # Invalid:
  # usertest.py, apitest.py
  ```

#### 🐍 **Python Code Quality Hooks**

##### 🔧 **Ruff - Linting and Formatting**
- **`ruff`**: Fast Python linter (replaces flake8, isort, and more)
  ```bash
  # Checks for:
  # - Import sorting
  # - Code style violations
  # - Unused imports/variables
  # - Security issues
  # - Performance anti-patterns
  ```

- **`ruff-format`**: Python code formatter (replaces Black)
  ```python
  # Before:
  def function(x,y,z):
      return x+y+z

  # After:
  def function(x, y, z):
      return x + y + z
  ```

##### 🔍 **Pyright - Type Checking**
- **`pyright`**: Static type analysis for Python
  ```python
  # Catches type errors like:
  def add_numbers(a: int, b: int) -> int:
      return a + b

  result = add_numbers("hello", "world")  # Type error caught
  ```

### 🚀 **Pre-commit Installation and Setup**

#### 📦 **Installation Process**
```bash
# 1. Install pre-commit (included in dev dependencies)
uv sync --all-extras

# 2. Install git hooks
pre-commit install

# 3. Verify installation
pre-commit --version
```

#### 🔧 **Git Hook Integration**
After installation, pre-commit creates a `.git/hooks/pre-commit` script that:
1. Runs automatically before each `git commit`
2. Stages files are checked by configured hooks
3. Blocks commit if any hook fails
4. Allows commit to proceed if all hooks pass

### 🔄 **Pre-commit Workflow**

#### 📝 **Typical Development Workflow**
```bash
# 1. Make code changes
echo "print('hello world')" > test_file.py

# 2. Stage files for commit
git add test_file.py

# 3. Attempt to commit (triggers pre-commit)
git commit -m "Add test file"

# Pre-commit runs automatically:
# - Ruff checks and fixes code style
# - Pyright checks types
# - File format hooks run
# - If all pass: commit succeeds
# - If any fail: commit blocked
```

#### 🔄 **Hook Execution Flow**
```
git commit
    ↓
Pre-commit activated
    ↓
┌─────────────────────┐
│ File Quality Hooks  │
│ - check-json        │
│ - check-yaml        │
│ - trailing-whitespace│
│ - end-of-file-fixer │
└─────────────────────┘
    ↓ (if pass)
┌─────────────────────┐
│ Python Hooks        │
│ - ruff (lint)       │
│ - ruff-format       │
│ - pyright (types)   │
└─────────────────────┘
    ↓ (if all pass)
Commit succeeds
```

### 🛠️ **Pre-commit Commands**

#### 🏃 **Manual Execution**
```bash
# Run hooks on all files
pre-commit run --all-files

# Run hooks on staged files only
pre-commit run

# Run specific hook
pre-commit run ruff

# Run specific hook on all files
pre-commit run trailing-whitespace --all-files

# Run hooks on specific files
pre-commit run --files app/main.py app/config.py
```

#### 🔄 **Hook Management**
```bash
# Update hooks to latest versions
pre-commit autoupdate

# Install hooks without running them
pre-commit install --install-hooks

# Uninstall pre-commit hooks
pre-commit uninstall

# Clean hook cache
pre-commit clean
```

#### 🐛 **Debugging and Troubleshooting**
```bash
# Run with verbose output
pre-commit run --verbose --all-files

# Show hook configuration
pre-commit run --show-diff-on-failure

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "Skip pre-commit hooks"

# Test hook configuration
pre-commit try-repo . --all-files
```

### 🎯 **Hook Configuration Details**

#### 🔧 **Ruff Configuration Integration**
Pre-commit uses Ruff settings from `pyproject.toml`:
```toml
[tool.ruff]
line-length = 120
src = ["app", "test", "scripts"]

[tool.ruff.lint]
extend-select = [
    "I",    # isort
    "T201", # print
    "T203", # pprint
]

[tool.ruff.format]
quote-style = "single"
```

#### 🔍 **Pyright Configuration Integration**
Pre-commit uses Pyright settings from `pyproject.toml`:
```toml
[tool.pyright]
include = ["app", "scripts"]
exclude = ["**/__pycache__"]
pythonVersion = "3.12"
reportAttributeAccessIssue = "warning"
```

### 📊 **Hook Execution Results**

#### ✅ **Successful Hook Run**
```bash
$ git commit -m "Add new feature"

check case conflict..............................................Passed
check for illegal windows names.................................Passed
check json.......................................................Passed
pretty format JSON...............................................Passed
check toml.......................................................Passed
check yaml.......................................................Passed
check for merge conflicts.......................................Passed
mixed line ending................................................Passed
tests should end in _test.py.....................................Passed
fix end of files.................................................Passed
trim trailing whitespace.........................................Passed
ruff.............................................................Passed
ruff-format......................................................Passed
pyright..........................................................Passed

[main abc1234] Add new feature
 2 files changed, 15 insertions(+)
```

#### ❌ **Failed Hook Run**
```bash
$ git commit -m "Add buggy code"

ruff.............................................................Failed
- hook id: ruff
- exit code: 1

app/main.py:15:1: F401 [*] `os` imported but unused
app/main.py:23:5: T201 `print` found
Found 2 errors (1 fixed, 1 remaining).

pyright..........................................................Failed
- hook id: pyright
- exit code: 1

app/main.py:45:12 - error: Argument of type "str" cannot be assigned to parameter of type "int"
```

### 🎛️ **Advanced Pre-commit Features**

#### 🔀 **Conditional Hook Execution**
```yaml
# Run only on specific file types
- id: ruff
  files: \.py$

# Exclude specific directories
- id: pyright
  exclude: ^tests/fixtures/

# Run only on specific stages
- id: ruff
  stages: [commit, push]
```

#### 🌍 **Environment-specific Configuration**
```yaml
# Different configurations for different environments
- id: ruff
  args: [--config, pyproject.toml]
  additional_dependencies: [ruff==0.11.13]
```

#### 📦 **Custom Hooks**
```yaml
# Local custom hooks
- repo: local
  hooks:
    - id: custom-security-check
      name: Custom Security Check
      entry: python scripts/security_check.py
      language: python
      files: \.py$
```

### 🔧 **Integration with Development Workflow**

#### 🐳 **Docker Integration**
```bash
# Run pre-commit in Docker container
docker compose run --rm app pre-commit run --all-files

# Install pre-commit in Docker
docker compose run --rm app pre-commit install
```

#### 🔄 **CI/CD Integration**
```yaml
# GitHub Actions example
- name: Run pre-commit
  uses: pre-commit/action@v3.0.0
  with:
    extra_args: --all-files
```

#### 📝 **IDE Integration**
```json
// VS Code settings.json
{
  "python.linting.enabled": true,
  "python.formatting.provider": "none",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### 🎯 **Benefits of This Pre-commit Setup**

#### ✅ **Code Quality Benefits**
- **Consistent Formatting**: Automatic code formatting with Ruff
- **Early Error Detection**: Type checking with Pyright
- **Import Organization**: Automatic import sorting
- **Style Enforcement**: Consistent code style across team

#### 🚀 **Development Benefits**
- **Fast Feedback**: Immediate feedback on code quality
- **Automated Fixes**: Many issues fixed automatically
- **Reduced Review Time**: Less time spent on style issues in code review
- **Cross-platform Consistency**: Same checks across all environments

#### 🔧 **Team Benefits**
- **Onboarding**: New team members get consistent setup
- **Knowledge Sharing**: Shared code quality standards
- **Reduced Conflicts**: Fewer merge conflicts due to formatting
- **Documentation**: Self-documenting code quality requirements

### 🚨 **Common Pre-commit Issues and Solutions**

#### ⚠️ **Hook Installation Issues**
**Problem**: Hooks not running after installation
**Solution**:
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Verify installation
ls -la .git/hooks/pre-commit
```

#### ⚠️ **Performance Issues**
**Problem**: Hooks taking too long to run
**Solution**:
```bash
# Run only on changed files
pre-commit run

# Skip slow hooks temporarily
SKIP=pyright git commit -m "Quick fix"

# Update to faster hook versions
pre-commit autoupdate
```

#### ⚠️ **Configuration Conflicts**
**Problem**: Tool configurations conflicting
**Solution**:
```toml
# Ensure consistent configuration in pyproject.toml
[tool.ruff]
line-length = 120

[tool.pyright]
# Compatible with Ruff settings
```

#### ⚠️ **False Positives**
**Problem**: Hooks flagging valid code
**Solution**:
```python
# Use specific ignores
def function():
    import os  # noqa: F401 - Used in dynamic import

# Or exclude files
# In .pre-commit-config.yaml:
# exclude: ^legacy/
```

### 📈 **Pre-commit Monitoring and Maintenance**

#### 📊 **Hook Performance Tracking**
```bash
# Time hook execution
time pre-commit run --all-files

# Profile specific hooks
pre-commit run ruff --verbose
```

#### 🔧 **Regular Maintenance Tasks**
- **Update Hook Versions**: Run `pre-commit autoupdate` monthly
- **Review Configuration**: Ensure hooks align with project needs
- **Performance Monitoring**: Check hook execution times
- **Team Training**: Ensure team understands hook requirements

#### 📋 **Hook Effectiveness Metrics**
- **Commit Success Rate**: Percentage of commits passing hooks
- **Auto-fix Rate**: Issues automatically resolved
- **Manual Intervention**: Issues requiring developer attention
- **Time Savings**: Reduced code review time

This comprehensive pre-commit integration provides automated code quality assurance, ensuring consistent code style, early error detection, and improved development workflow efficiency across the entire team.

---

## ⚙️ Configuration Files

### 📄 `pyproject.toml`
Modern Python project configuration file containing:
- **Project metadata**: Name, version, description, Python version requirements
- **Dependencies**: Runtime and development dependencies with pinned versions
- **Tool configurations**: Ruff linter, MyPy type checker, Pytest settings
- **Build system**: Package build requirements

### 📄 `alembic.ini`
Alembic-specific configuration:
- Database connection URL template
- Migration file locations
- Logging configuration
- Migration script formatting options

### 📄 `.env`
Environment variables for local development:
- Database connection parameters
- Redis configuration
- Migration control flags
- Sensitive configuration data

---

## 🛠️ Development Tools Configuration

### 📄 `.pre-commit-config.yaml`
Configures automated code quality checks before commits:
- Code formatting with Black and Ruff
- Import sorting
- Type checking with MyPy
- Security scanning
- Commit message formatting

### 📄 `.gitignore`
Comprehensive Git ignore patterns for:
- Python cache files and bytecode
- Virtual environments
- IDE configuration files
- Environment variables and secrets
- Build artifacts and logs
- Database files and cache directories

### 📄 `.python-version`
Specifies the exact Python version (3.12) for version managers like pyenv.

---

## 📦 Dependency Management

### 📄 `requirements.txt`
Traditional pip requirements file with pinned versions for production deployment.

### 📄 `uv.lock`
UV package manager lock file ensuring reproducible builds with exact dependency versions and checksums.

---

## 🏛️ Architecture Patterns

This project implements several architectural patterns:

### 🔄 **Layered Architecture**
- **Presentation Layer**: FastAPI routers and schemas
- **Business Logic Layer**: Controllers and services
- **Data Access Layer**: Models and database operations

### 🎯 **Dependency Injection**
- FastAPI's built-in dependency system
- Centralized dependency management in `/dependencies`
- Easy testing and mocking

### 🗄️ **Repository Pattern**
- Models define data structure
- Controllers handle business logic
- Clean separation of concerns

### 🛡️ **Middleware Pattern**
- Cross-cutting concerns handled by middleware
- Request/response processing pipeline
- Authentication, logging, CORS handling

---

## 🚀 Getting Started

1. **Environment Setup**: Follow the README.md for detailed setup instructions
2. **Database**: Run migrations with `alembic upgrade head`
3. **Development**: Use `uvicorn app.main:app --reload` for local development
4. **Docker**: Use `docker compose up` for containerized development
5. **Testing**: Run tests with `pytest`

---

## 📈 Scalability Considerations

The project structure supports growth through:

- **Modular organization**: Easy to add new features in separate modules
- **Dependency injection**: Facilitates testing and component swapping
- **Database migrations**: Version-controlled schema changes
- **Containerization**: Consistent deployment across environments
- **Caching layer**: Redis for performance optimization
- **Configuration management**: Environment-based settings

---

## 🔧 Maintenance

Regular maintenance tasks:
- Update dependencies in `pyproject.toml`
- Run `uv sync` to update lock file
- Create database migrations for schema changes
- Update Docker images for security patches
- Review and update pre-commit hooks
- Monitor application logs and performance metrics

This structure provides a solid foundation for building scalable FastAPI applications while maintaining code quality and development efficiency.

---

## ⚡ How UV Works in This Project

This section provides a comprehensive explanation of how UV (Ultra-fast Python package installer and resolver) is implemented and integrated into this FastAPI starter project for modern Python dependency management.

### 📋 **UV Overview**

UV is a next-generation Python package installer and resolver written in Rust that provides:
- **Ultra-fast Performance**: 10-100x faster than pip for dependency resolution and installation
- **Modern Lock Files**: Reproducible builds with comprehensive dependency locking
- **Drop-in Replacement**: Compatible with pip and existing Python workflows
- **Cross-platform Support**: Consistent behavior across different operating systems

### 🏗️ **UV Architecture in This Project**

```
┌─────────────────────────────────────────────────────┐
│                UV Dependency Management              │
│                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │pyproject.toml│───▶│     UV      │───▶│ Virtual │ │
│  │(Config)     │    │   Resolver  │    │   Env   │ │
│  │             │    │             │    │(.venv/) │ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
│         │                   │                │     │
│         │                   │                │     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │   uv.lock   │    │  Package    │    │Installed│ │
│  │(Lock File)  │    │  Registry   │    │Packages │ │
│  │             │    │ (PyPI, etc) │    │         │ │
│  └─────────────┘    └─────────────┘    └─────────┘ │
└─────────────────────────────────────────────────────┘
```

### 📄 **UV Configuration Files**

#### 🔧 **`pyproject.toml` - Project Configuration**

```toml
[project]
name = "fastapi-starter-project"
version = "0.1.0"
description = "FastAPI starter project"
readme = "README.md"
requires-python = ">=3.12"                    # Python version constraint
dependencies = [                              # Runtime dependencies
    "aioredis==2.0.1",                       # Redis async client
    "alembic==1.14.1",                       # Database migrations
    "annotated-types==0.7.0",                # Type annotations
    "anyio==4.8.0",                          # Async I/O library
    "async-timeout==5.0.1",                  # Timeout utilities
    "bcrypt==4.2.1",                         # Password hashing
    "dnspython==2.7.0",                      # DNS resolution for email validation
    "email-validator==2.2.0",                # Email validation
    "fastapi==0.115.8",                      # Web framework
    "h11==0.14.0",                           # HTTP/1.1 implementation
    "idna==3.10",                            # Internationalized domain names
    "mako==1.3.9",                           # Template engine (Alembic)
    "markupsafe==3.0.0",                     # Safe string handling
    "psycopg2-binary==2.9.10",               # PostgreSQL adapter
    "pydantic==2.10.6",                      # Data validation
    "pydantic-core==2.27.2",                 # Pydantic core library
    "pydantic-settings==2.7.1",              # Settings management
    "python-dotenv==1.0.1",                  # Environment variable loading
    "sniffio==1.3.1",                        # Async library detection
    "sqlalchemy==2.0.38",                    # ORM and database toolkit
    "starlette==0.45.3",                     # ASGI framework (FastAPI dependency)
    "typing-extensions==4.12.2",             # Extended type hints
    "uvicorn==0.34.0",                       # ASGI server
]

[project.optional-dependencies]              # Development dependencies
dev = [
    "black==25.1.0",                         # Code formatter
    "mypy==1.15.0",                          # Static type checker
    "mypy-extensions==1.0.0",                # MyPy extensions
    "pre-commit==4.2.0",                     # Pre-commit hooks
    "ruff==0.11.2",                          # Fast Python linter
]
```

#### 🎯 **Key Configuration Features**
- **Pinned Dependencies**: All dependencies have exact version specifications
- **Python Version Constraint**: Requires Python 3.12 or higher
- **Optional Dependencies**: Development tools separated from runtime dependencies
- **Comprehensive Metadata**: Project name, version, and description for packaging

#### 🔒 **`uv.lock` - Lock File Structure**

```toml
version = 1                                   # Lock file format version
revision = 1                                  # Lock file revision
requires-python = ">=3.12"                   # Python version requirement

[[package]]                                   # Package definition
name = "fastapi"
version = "0.115.8"
source = { registry = "https://pypi.org/simple" }
dependencies = [                              # Package dependencies
    { name = "pydantic" },
    { name = "starlette" },
    { name = "typing-extensions" },
]
sdist = {                                     # Source distribution info
    url = "https://files.pythonhosted.org/packages/.../fastapi-0.115.8.tar.gz",
    hash = "sha256:0ce9111231720190473e222cdf0f07f7206ad7e53ea02beb1d2dc36e2f0741e9",
    size = 295403
}
wheels = [                                    # Wheel distribution info
    {
        url = "https://files.pythonhosted.org/packages/.../fastapi-0.115.8-py3-none-any.whl",
        hash = "sha256:753a96dd7e036b34eeef8babdfcfe3f28ff79648f86551eb36bfc1b0bf4a8cbf",
        size = 94814
    },
]
```

#### 🔑 **Lock File Features**
- **Exact Versions**: Every package locked to specific version
- **Cryptographic Hashes**: SHA256 hashes for security verification
- **Multiple Formats**: Both source distributions (sdist) and wheels
- **Dependency Tree**: Complete dependency resolution graph
- **Platform Specific**: Different wheels for different platforms/architectures

### 🚀 **UV Installation and Setup**

#### 📦 **Local Development Setup**
```bash
# 1. Install UV (multiple methods available)
# Method 1: Using pip
pip install uv

# Method 2: Using curl (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Method 3: Using brew (macOS)
brew install uv

# 2. Verify installation
uv --version

# 3. Create virtual environment and install dependencies
uv sync

# 4. Activate virtual environment (optional, uv manages this)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

#### 🐳 **Docker Integration**
The Dockerfile shows UV integration in containerized environments:

```dockerfile
FROM python:3.12-slim

# Environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app

# Install UV from official container image
COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /uvx /bin/

# Copy dependency files first (Docker layer caching)
COPY uv.lock pyproject.toml ./

# Install dependencies using UV
RUN uv sync --frozen --no-cache

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY . .

# Start application
CMD ["uvicorn", "app.main:app", "--port", "5000", "--host", "0.0.0.0"]
```

### 🔄 **UV Workflow and Commands**

#### 🏃 **Development Workflow**

##### 📦 **Dependency Management**
```bash
# Install all dependencies (runtime + dev)
uv sync

# Install only runtime dependencies
uv sync --no-dev

# Install with all optional dependencies
uv sync --all-extras

# Install specific extra group
uv sync --extra dev

# Update lock file with latest compatible versions
uv lock

# Add new dependency
uv add fastapi-users

# Add development dependency
uv add --dev pytest

# Remove dependency
uv remove requests

# Upgrade specific package
uv add fastapi@latest
```

##### 🔧 **Virtual Environment Management**
```bash
# Create virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.12

# Activate virtual environment
source .venv/bin/activate

# Run command in virtual environment
uv run python app/main.py

# Run with specific Python version
uv run --python 3.12 python app/main.py

# Install package in development mode
uv pip install -e .
```

##### 📊 **Project Information**
```bash
# Show dependency tree
uv tree

# Show outdated packages
uv pip list --outdated

# Show package information
uv pip show fastapi

# Verify lock file integrity
uv lock --check

# Export requirements.txt format
uv export --format requirements-txt > requirements.txt
```

### 🎯 **UV Performance Benefits**

#### ⚡ **Speed Comparisons**
```bash
# Traditional pip workflow (slow)
pip install -r requirements.txt  # ~30-60 seconds

# UV workflow (fast)
uv sync                          # ~3-5 seconds

# Dependency resolution comparison
pip-tools compile pyproject.toml # ~15-30 seconds
uv lock                         # ~1-2 seconds
```

#### 🔧 **Performance Optimizations**
- **Parallel Downloads**: Downloads packages concurrently
- **Cached Resolution**: Reuses previous dependency resolution results
- **Binary Wheels**: Prefers pre-compiled wheels over source distributions
- **Incremental Updates**: Only updates changed dependencies

### 🔒 **UV Security Features**

#### 🛡️ **Hash Verification**
```bash
# UV automatically verifies package hashes
uv sync  # Verifies SHA256 hashes from uv.lock

# Manual hash verification
uv pip install fastapi --require-hashes
```

#### 🔐 **Dependency Auditing**
```bash
# Check for known vulnerabilities
uv pip audit

# Generate security report
uv pip audit --format json > security-report.json
```

### 🎛️ **Advanced UV Features**

#### 🔀 **Multiple Python Versions**
```bash
# Install with specific Python version
uv sync --python 3.12

# Create environment with different Python
uv venv --python 3.11 .venv-py311

# Run with specific Python version
uv run --python 3.12 pytest
```

#### 🌍 **Environment-specific Dependencies**
```toml
[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]
test = ["pytest", "pytest-cov", "httpx"]
docs = ["mkdocs", "mkdocs-material"]
prod = ["gunicorn", "uvicorn[standard]"]
```

```bash
# Install specific environment
uv sync --extra test
uv sync --extra prod
uv sync --extra dev,docs
```

#### 📦 **Custom Package Sources**
```toml
# In pyproject.toml
[tool.uv]
index-url = "https://pypi.org/simple"
extra-index-url = [
    "https://private-pypi.company.com/simple"
]
```

### 🔧 **UV Integration with Development Tools**

#### 🐳 **Docker Compose Integration**
```yaml
# docker-compose.yml
services:
  app:
    build: .
    environment:
      - UV_CACHE_DIR=/tmp/uv-cache  # Custom cache directory
    volumes:
      - uv-cache:/tmp/uv-cache      # Persistent UV cache

volumes:
  uv-cache:                         # UV cache volume
```

#### 🔄 **CI/CD Integration**
```yaml
# GitHub Actions example
- name: Setup UV
  uses: astral-sh/setup-uv@v1
  with:
    version: "0.6.10"

- name: Install dependencies
  run: uv sync --frozen

- name: Run tests
  run: uv run pytest
```

#### 📝 **IDE Integration**
```json
// VS Code settings.json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.venvPath": ".venv"
}
```

### 🎯 **Benefits of UV in This Project**

#### ✅ **Development Benefits**
- **Fast Setup**: New developers can get started in seconds
- **Reproducible Builds**: Exact same dependencies across all environments
- **Simple Commands**: Familiar pip-like interface with enhanced features
- **Integrated Workflow**: Single tool for all dependency management needs

#### 🚀 **Production Benefits**
- **Faster Deployments**: Significantly reduced Docker build times
- **Security**: Built-in hash verification and vulnerability scanning
- **Reliability**: Deterministic dependency resolution
- **Efficiency**: Reduced bandwidth usage with intelligent caching

#### 🔧 **Operational Benefits**
- **Consistency**: Same tool works across development, testing, and production
- **Debugging**: Clear error messages and dependency resolution information
- **Maintenance**: Easy dependency updates and security patching
- **Integration**: Works seamlessly with existing Python tooling

### 🔄 **UV Migration from Pip**

#### 📝 **Migration Steps**
```bash
# 1. Generate pyproject.toml from requirements.txt
uv init --lib  # or --app for applications

# 2. Import existing requirements
uv add -r requirements.txt

# 3. Generate lock file
uv lock

# 4. Verify installation
uv sync --frozen

# 5. Update CI/CD pipelines to use UV
# Replace: pip install -r requirements.txt
# With: uv sync --frozen
```

#### ✅ **Migration Checklist**
- [ ] Convert requirements.txt to pyproject.toml dependencies
- [ ] Generate and commit uv.lock file
- [ ] Update Dockerfile to use UV
- [ ] Update CI/CD pipelines
- [ ] Update documentation and README
- [ ] Train team on UV commands
- [ ] Test in staging environment
- [ ] Monitor performance improvements

This comprehensive UV integration provides ultra-fast dependency management, reproducible builds, and modern Python packaging workflows that significantly improve development velocity and deployment reliability.
