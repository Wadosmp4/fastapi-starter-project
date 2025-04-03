# 📌 Project Setup Requirements (needed to be installed)

### 🔹 Python 3.12

### 🔹 Docker and docker compose

<br>

# 🚀 Python Project Setup Workflow

## 🏗️ Step-by-Step Guide

### 1️⃣ Set Up Virtual Environment

```
python3 -m venv .venv      # Creates the virtual environment
source .venv/bin/activate  # Activate the virtual environment (Linux/macOS)
.venv\Scripts\activate     # Activate the virtual environment (Windows)
```

<br>

### 2️⃣ Install Dependencies

We use `uv` for faster dependency management. Install it first:

```bash
# Install uv
pip install uv
```

Run this command to install packages and dependencies:

```bash
# Install all dependencies including dev tools
uv sync --all-extras
```

If you installed additional packages, add them to pyproject.toml:

```bash
# Add a runtime dependency
uv pip add package_name --sync

# Add a development dependency
uv pip add package_name --sync --dev
```

> [!TIP]
> This way we ensure tracking of all packages in pyproject.toml with proper versioning

<br>

### 3️⃣ Set Up Linters and Pre-commit Hooks

This command will make linters run before each commit and help you to refactor code and keep everything clean:

```bash
pre-commit install
```

> [!TIP]
> Run it only once and all needed dependencies will be installed

<br>

This command will help you when you want to run linters, but do not want to create a commit:

```bash
pre-commit run --all-files
```

> [!TIP]
> Can be run multiple times to ensure code quality

<br>

### 4️⃣ Create .env file

Example content of file for a successful build and start:

```
DATABASE_PORT=5432
POSTGRES_PASSWORD=password
POSTGRES_USER=postgres
POSTGRES_DB=fastapi
POSTGRES_HOST=db

REDIS_PASSWORD=password
REDIS_HOST=redis
REDIS_PORT=6379

MAKE_MIGRATIONS=false
MAKE_MIGRATION_DOWNGRADE=false
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

<br>

---

# 📌 Code Quality Tools

We use the following tools to maintain code quality:

### 🔹 Ruff

> [!NOTE]
> Ruff is an extremely fast Python linter and formatter, written in Rust. It handles both linting (code quality checks) and formatting (code style) in one tool, replacing both Flake8 and isort.

### 🔹 Black

> [!NOTE]
> Black is the uncompromising Python code formatter. It formats your code in a consistent style with little configuration needed.

### 🔹 MyPy

> [!NOTE]
> MyPy is a static type checker for Python. It helps catch type errors before runtime, making your code more reliable.

### 🔹 Pre-commit

> [!NOTE]
> Pre-commit manages git hooks to ensure code quality checks run before each commit, preventing problematic code from being committed.

<br>

To ignore specific Ruff warnings in your code, you can use comments:

```python
# For a specific line:
some_code = "example"  # noqa: E501

# For multiple specific warnings:
unused_variable = "something"  # noqa: F841, E501

# For an entire file (add at the top):
# ruff: noqa: E501, F841
```

<br>

---

# 🚀 Docker and Docker Compose: Overview & Standard workflow

### 🔹 What is Docker?

> [!NOTE]
> Docker is a platform that helps developers create, deploy, and run applications in isolated environments called containers. <br> Containers bundle everything an application needs, ensuring it works the same way across different systems.

### 🔹 Why Use Docker?

✅ Portability: Runs the same way in any environment. <br>
✅ Scalability: Easy to scale applications. <br>
✅ Efficiency: Uses fewer resources than traditional VMs. <br>
✅ Isolation: Prevents conflicts between applications. <br>

### 📦 Simplifying Dependencies with Containers

> [!NOTE]
> Containers package all required dependencies, eliminating the need for local installations.
> For example, instead of manually installing and configuring a database on your local machine,
> you can run it inside a container, ensuring a consistent and hassle-free setup.

### 🔹 What is Docker Compose?

> [!NOTE]
> Docker Compose is a tool that allows you to manage multi-container applications.
> Instead of running separate docker run commands, you can define everything in a docker-compose.yml file
> and start all services with a single command.

### 🔹 Why Use Docker Compose?

✅ Simplifies multi-container setup. <br>
✅ Allows defining environments in a single file. <br>
✅ Supports easy service scaling. <br>
✅ Reduces manual setup effort. <br>

<br>

---

# 📌 Standard Workflow with Docker Compose

## 🏗️ Step-by-Step Guide

### 1️⃣ Install Docker and Docker Compose

Ensure you have Docker and Docker Compose installed. You can verify their installation with:

```bash
docker --version
docker compose --version
```

<br>

### 2️⃣ Build and Start Services

Run the following command to build images (if needed) and start the services:

```bash
docker compose up --build
```

After application build and start it will be available by this url http://localhost:5001/

<br>

### 3️⃣ Stop Services

When you're done, shut everything down (in the same terminal where everything was started):

```bash
CTRL+C command
```

Or run this command in a separate terminal window to stop and remove containers:

```bash
docker compose down
```

<br>

---

# 📌 Alembic: Database Migrations Guide

### 🔹 What is Alembic?

> Alembic is a database migration tool for SQLAlchemy.
> It helps track schema changes and apply them across different environments.

<br>

## 📌 Standard Alembic Workflow For Local Usage

### 🔹 Automatically Detect And Apply Schema Changes

Configure variables in your `.env` file like this:

```
MAKE_MIGRATIONS=true
MAKE_MIGRATION_DOWNGRADE=false
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

Migrations will be enabled for the project, and on the startup, they will be automatically created and applied to the database:

```
docker compose up --build
```

✅ Alembic inspects SQLAlchemy models and generates migration code(script) automatically.

> [!TIP]
> It is obligatory to import our models so alembic will see them <br>
> You can check a guide in `app/models/__init__.py` file

> [!IMPORTANT]
> We should keep track of all migration scripts so we will be able to upgrade or downgrade correctly our production database <br>
>
> For instance, during the implementation of a feature, we created five additional migration files as part of local testing. <br>
> However, to deploy the changes to production, it would be better to delete these five latest migration files
> and create a new, single migration that consolidates the changes from all of them.
> This ensures a cleaner, more efficient migration process for production.

<br>

### 🔹 Downgrade Version After Development of Feature

Let's Assume that we created some number of migrations during implementation of feature and `63017c98c3da` is the migration from which we started adding changes

Configure variables in your `.env` file like this:

```
MAKE_MIGRATIONS=false
MAKE_MIGRATION_DOWNGRADE=true
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

Run command to start a project:

```
docker compose up --build
```

Then delete all new migration files that were created during implementation and change `.env` to making migrations again:

```
MAKE_MIGRATIONS=true
MAKE_MIGRATION_DOWNGRADE=false
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

Run command to start a project:

```
docker compose up --build
```

✅ Now you have one migration script that includes all the changes for implemented feature <br>
This way you will have clean history of migrations

<br>

### 🔹 Manual Migrations Generation

To be able to run migrations command change `POSTGRES_HOST` in `.env` file and start database:

```
POSTGRES_HOST=localhost
```

We need to do this because we want to access database from outside of the container

To start database separately use following command:

```
docker compose up db
```

Commands to migrate and apply database migrations:

```
alembic revision --autogenerate -m "your name of migration"
alembic upgrade head
```

<br>

---

# That is all you need to have for fully configured project 🎉

## 📌 Below you can find useful commands that may come in handy during development

<br>

---

# 🚀 Useful Docker and Docker Compose Commands

## 📌 Docker Commands

### 🏗️ Container Management

- List all running containers

  ```
  docker ps
  ```

  _Shows currently running containers._
- List all containers (including stopped ones)

  ```
  docker ps -a
  ```

  _Shows all containers, including those that are stopped._
- Start a container

  ```
  docker start <container_id>
  ```

  _Starts a stopped container._
- Stop a container

  ```
  docker stop <container_id>
  ```

  _Stops a running container._
- Restart a container

  ```
  docker restart <container_id>
  ```

  _Restarts a container._
- Remove a container

  ```
  docker rm <container_id>
  ```

  _Deletes a stopped container._
- Remove all stopped containers

  ```
  docker container prune
  ```

  _Deletes all containers that are not running._

### 🏗️ Image Management

- List all images

  ```
  docker images
  ```

  _Displays all Docker images stored locally._
- Remove an image

  ```
  docker rmi <image_id>
  ```

  _Deletes a specific Docker image._
- Remove all unused images

  ```
  docker image prune -a
  ```

  _Deletes all dangling and unused images._

### 🏗️ Building and Running Containers

- Build an image from a Dockerfile

  ```
  docker build -t <image_name> .
  ```

  _Builds an image from the Dockerfile in the current directory._
- Run a container from an image

  ```
  docker run -d -p 80:80 --name <container_name> <image_name>
  ```

  _Runs a container in detached mode, mapping port 80 of the container to port 80 on the host._
- Run an interactive container

  ```
  docker run -it <image_name> /bin/bash
  ```

  _Starts a container and opens an interactive bash shell._

### 📂 Volumes and Logs

- List all volumes

  ```
  docker volume ls
  ```

  _Displays all Docker volumes._
- Remove unused volumes

  ```
  docker volume prune
  ```

  _Deletes all unused volumes._
- View logs of a container

  ```
  docker logs <container_id>
  ```

  _Displays logs for a specific container._
- Follow logs in real-time

  ```
  docker logs -f <container_id>
  ```

  _Streams logs from a container._

### 🏗️ Network Management

- List networks

  ```
  docker network ls
  ```

  _Displays all Docker networks._
- Create a new network

  ```
  docker network create <network_name>
  ```

  _Creates a new Docker network._
- Connect a container to a network

  ```
  docker network connect <network_name> <container_name>
  ```

  _Attaches a container to a specific network._

## 📌 Useful Docker Compose Commands

### 🏗️ Managing Services

- Start services defined in docker-compose.yml

  ```
  docker compose up -d
  ```

  _Starts all services in detached mode._
- Stop services

  ```
  docker compose down
  ```

  _Stops and removes all running services._
- Restart services

  ```
  docker compose restart
  ```

  _Restarts all running services._
- Rebuild services (force re-build of images)

  ```
  docker compose up --build
  ```

  _Rebuilds services and runs them._

### 🏗️ Service Management

- List all running services

  ```
  docker-compose ps
  ```

  _Shows all running services._
- View logs for a service

  ```
  docker compose logs -f <service_name>
  ```

  _Streams logs from a specific service._
- Run a command inside a running service

  ```
  docker compose exec <service_name> <command>
  ```

  _Runs a command inside a running container (e.g., /bin/bash)._

### 📂 Volumes and Cleanup

- Remove all stopped services and volumes

  ```
  docker compose down -v
  ```

  _Stops and removes all containers, networks, and volumes._
- Prune unused resources

  ```
  docker system prune -a
  ```

  _Removes all unused containers, images, networks, and caches._

<br>

# 📌 Useful Alembic commands

### 🔹 Create a New Migration <br>

```
alembic revision -m "add users table"
```

✅ This generates a new migration script in alembic/versions/.

💡 But it does not create a migration code, so we should manually add it in a created template

<br>

### 🔹 Automatically Detect Schema Changes

```
alembic revision --autogenerate -m "auto detect changes"
```

✅ Alembic inspects SQLAlchemy models and generates migration code automatically.

💡 Ensure models are imported in env.py for autogeneration to work!

<br>

### 🔹 Apply Migrations to the Database

```
alembic upgrade head
```

✅ This applies all pending migrations up to the latest version.

Use `alembic upgrade <version_id>` to apply migrations up to a specific point.

<br>

### 🔹 Revert to a Previous State (Downgrade)

```
alembic downgrade -1
```

✅ This rolls back the last migration.

Use `alembic downgrade <version_id>` to revert to a specific version.

<br>

## 📌 Managing Migration History

### 🔹 View Current Migration State

```
alembic current
```

✅ Displays the currently applied migration version.

<br>

### 🔹 Check History of Migrations

```
alembic history
```

✅ Lists all past migrations in order.

<br>

### 🔹 Show Pending Migrations

```
alembic heads
```

✅ Displays the latest (unapplied) migration version(s).

<br>

### 🔹 Manually Stamp Database with a Version

```
alembic stamp head
```

✅ Marks the database as up-to-date without applying migrations.

<br>

## 📌 Common Debugging Commands

### 🔹 Verify Your Migration Script

```
alembic check
```

✅ Checks for issues in migration scripts before applying them.

<br>

### 🔹 Generate SQL Instead of Applying Migration

```
alembic upgrade head --sql
```

✅ Shows SQL statements without running them, useful for debugging.

<br>

# Complete Migration Reset Process for Local Development

Here's a step-by-step guide to reset your migrations while preserving your database structure:

## 1. Configure Database Connection

First, ensure your database is running and your connection settings are configured:

```bash
# In your .env file
POSTGRES_HOST=localhost  # Change to localhost if using direct connection
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=fastapi
```

## 2. Start the Database

Make sure your database is running:

```bash
# Start just the database container
docker compose up db
```

## 3. Verify Database Connection

Test your connection to ensure everything is working:

```bash
# Test connection using psql
psql -U postgres -h localhost -d fastapi -c "SELECT 'Connection successful';"
```

## 4. Create a Backup (Optional but Recommended)

Before making changes, back up your existing migrations and database:

```bash
# Backup migrations
mkdir -p alembic/versions_backup
cp -r alembic/versions/* alembic/versions_backup/

# Backup database (optional)
pg_dump -U postgres -h localhost -d fastapi > db_backup.sql
```

## 5. Reset Alembic Version Tracking

Remove migration tracking from the database:

```bash
# Reset Alembic migration state
alembic stamp base
```

## 6. Verify Reset

Check that the version tracking has been reset:

```bash
# Should show no current revision
alembic current
```

## 7. Remove Migration Files

Now you can safely delete the migration files:

```bash
# Remove all migrations
rm -rf alembic/versions/*.py
```

## 8. Create a Fresh Migration

Generate a new migration that captures the current state of your database:

```bash
# Create new migration capturing current schema
alembic revision --autogenerate -m "fresh_start"
```

## 9. Mark the Migration as Applied

Tell Alembic that this new migration has already been applied:

```bash
# Mark as applied
alembic stamp head
```

## 10. Verify Success

Confirm everything worked correctly:

```bash
# Should show your new migration id
alembic current

# Check migration history - should just show your new migration
alembic history
```

> [!NOTE]
> This approach is perfect for local development as it gives you a clean migration history while preserving your database structure and data. It's especially useful when you've accumulated many incremental migrations during development that you don't need to preserve for production.

### 🔹 Python 3.12

### 🔹 Docker and docker compose

<br>

# 🚀 Python Project Setup Workflow

## 🏗️ Step-by-Step Guide

### 1️⃣ Set Up Virtual Environment

```
python3 -m venv .venv      # Creates the virtual environment
source .venv/bin/activate  # Activate the virtual environment (Linux/macOS)
.venv\Scripts\activate     # Activate the virtual environment (Windows)
```

<br>

### 2️⃣ Install Dependencies

We use `uv` for faster dependency management. Install it first:

```bash
# Install uv
pip install uv
```

Run this command to install packages and dependencies:

```bash
# Install all dependencies including dev tools
uv sync --all-extras
```

If you installed additional packages, add them to pyproject.toml:

```bash
# Add a runtime dependency
uv pip add package_name --sync

# Add a development dependency
uv pip add package_name --sync --dev
```

> [!TIP]
> This way we ensure tracking of all packages in pyproject.toml with proper versioning

<br>

### 3️⃣ Set Up Linters and Pre-commit Hooks

This command will make linters run before each commit and help you to refactor code and keep everything clean:

```bash
pre-commit install
```

> [!TIP]
> Run it only once and all needed dependencies will be installed

<br>

This command will help you when you want to run linters, but do not want to create a commit:

```bash
pre-commit run --all-files
```

> [!TIP]
> Can be run multiple times to ensure code quality

<br>

### 4️⃣ Create .env file

Example content of file for a successful build and start

```
DATABASE_PORT=5432
POSTGRES_PASSWORD=password
POSTGRES_USER=postgres
POSTGRES_DB=fastapi
POSTGRES_HOST=db

REDIS_PASSWORD=password
REDIS_HOST=redis
REDIS_PORT=6379

MAKE_MIGRATIONS=false
MAKE_MIGRATION_DOWNGRADE=false
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

<br>

---

# 🚀 Docker and Docker Compose: Overview & Standard workflow

### 🔹 What is Docker?

> [!NOTE]
> Docker is a platform that helps developers create, deploy, and run applications in isolated environments called containers. <br> Containers bundle everything an application needs, ensuring it works the same way across different systems.

### 🔹 Why Use Docker?

✅ Portability: Runs the same way in any environment. <br>
✅ Scalability: Easy to scale applications. <br>
✅ Efficiency: Uses fewer resources than traditional VMs. <br>
✅ Isolation: Prevents conflicts between applications. <br>

### 📦 Simplifying Dependencies with Containers

> [!NOTE]
> Containers package all required dependencies, eliminating the need for local installations.
> For example, instead of manually installing and configuring a database on your local machine,
> you can run it inside a container, ensuring a consistent and hassle-free setup.

### 🔹 What is Docker Compose?

> [!NOTE]
> Docker Compose is a tool that allows you to manage multi-container applications.
> Instead of running separate docker run commands, you can define everything in a docker-compose.yml file
> and start all services with a single command.

### 🔹 Why Use Docker Compose?

✅ Simplifies multi-container setup. <br>
✅ Allows defining environments in a single file. <br>
✅ Supports easy service scaling. <br>
✅ Reduces manual setup effort. <br>

<br>

---

# 📌 Standard Workflow with Docker Compose

## 🏗️ Step-by-Step Guide

### 1️⃣ Install Docker and Docker Compose

Ensure you have Docker and Docker Compose installed. You can verify their installation with:

docker --version
docker compose --version
<br>

### 2️⃣ Build and Start Services Run

The following command to build images (if needed) and start the services:

docker compose up --build
After application build and start it will be available by this url http://localhost:5001/

<br>

### 3️⃣ Stop Services

When you're done, shut everything down (in the same terminal where everything was started):

CTRL+C command
Or run this command in a separate terminal window to stop and remove containers:

docker compose down
<br>

---

# 📌 Alembic: Database Migrations Guide

### 🔹 What is Alembic?

> Alembic is a database migration tool for SQLAlchemy.
> It helps track schema changes and apply them across different environments.

<br>

## 📌 Standard Alembic Workflow For Local Usage

### 🔹 Automatically Detect And Apply Schema Changes

Configure variables in your ``.env`` file like this

```
MAKE_MIGRATIONS=true
MAKE_MIGRATION_DOWNGRADE=false
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

Migrations will be enabled for the project, and on the startup, they will be automatically created and applied to the database

```
docker compose up --build
```

✅ Alembic inspects SQLAlchemy models and generates migration code(script) automatically.

> [!TIP]
> It is obligatory to import our models so alembic will see them <br>
> You can check a guide in ``app/models/__init__.py`` file

> [!IMPORTANT]
> We should keep track of all migration scripts so we will be able to upgrade or downgrade correctly our production database <br>
>
> For instance, during the implementation of a feature, we created five additional migration files as part of local testing. <br>
> However, to deploy the changes to production, it would be better to delete these five latest migration files
> and create a new, single migration that consolidates the changes from all of them.
> This ensures a cleaner, more efficient migration process for production.

<br>

### 🔹 Downgrade Version After Development of Feature

Let's Assume that we created some number of migrations during implementation of feature and ``63017c98c3da`` is the migration from which we started adding changes

Configure variables in your ``.env`` file like this

```
MAKE_MIGRATIONS=false
MAKE_MIGRATION_DOWNGRADE=true
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

Run command to start a project

```
docker compose up --build
```

Then delete all new migration files that were created during implementation and change ``.env`` to making migrations again

```
MAKE_MIGRATIONS=true
MAKE_MIGRATION_DOWNGRADE=false
MIGRATION_DOWNGRADE_TARGET=63017c98c3da
```

Run command to start a project

```
docker compose up --build
```

✅ Now you have one migration script that includes all the changes for implemented feature <br>
This way you will have clean history of migrations

<br>

### 🔹 Manual Migrations Generation

To be able to run migrations command change ``POSTGRES_HOST`` in ``.env`` file and start database

```
POSTGRES_HOST=localhost
```

We need to do this because we want to access database from outside of the container

To start database separately use following command

```
docker compose up db
```

Commands to migrate and apply database migrations

```
alembic revision --autogenerate -m "your name of migration"
alembic upgrade head
```

<br>

---

# That is all you need to have for fully configured project 🎉

## 📌 Below you can find useful commands that may come in handy during development

<br>

---

# 🚀 Useful Docker and Docker Compose Commands

## 📌 Docker Commands

### 🏗️ Container Management

- List all running containers

  ```
  docker ps
  ```

  _Shows currently running containers._
- List all containers (including stopped ones)

  ```
  docker ps -a
  ```

  _Shows all containers, including those that are stopped._
- Start a container

  ```
  docker start <container_id>
  ```

  _Starts a stopped container._
- Stop a container

  ```
  docker stop <container_id>
  ```

  _Stops a running container._
- Restart a container

  ```
  docker restart <container_id>
  ```

  _Restarts a container._
- Remove a container

  ```
  docker rm <container_id>
  ```

  _Deletes a stopped container._
- Remove all stopped containers

  ```
  docker container prune
  ```

  _Deletes all containers that are not running._

### 🏗️ Image Management

- List all images

  ```
  docker images
  ```

  _Displays all Docker images stored locally._
- Remove an image

  ```
  docker rmi <image_id>
  ```

  _Deletes a specific Docker image._
- Remove all unused images

  ```
  docker image prune -a
  ```

  _Deletes all dangling and unused images._

### 🏗️ Building and Running Containers

- Build an image from a Dockerfile

  ```
  docker build -t <image_name> .
  ```

  _Builds an image from the Dockerfile in the current directory._
- Run a container from an image

  ```
  docker run -d -p 80:80 --name <container_name> <image_name>
  ```

  _Runs a container in detached mode, mapping port 80 of the container to port 80 on the host._
- Run an interactive container

  ```
  docker run -it <image_name> /bin/bash
  ```

  _Starts a container and opens an interactive bash shell._

### 📂 Volumes and Logs

- List all volumes

  ```
  docker volume ls
  ```

  _Displays all Docker volumes._
- Remove unused volumes

  ```
  docker volume prune
  ```

  _Deletes all unused volumes._
- View logs of a container

  ```
  docker logs <container_id>
  ```

  _Displays logs for a specific container._
- Follow logs in real-time

  ```
  docker logs -f <container_id>
  ```

  _Streams logs from a container._

### 🏗️ Network Management

- List networks

  ```
  docker network ls
  ```

  _Displays all Docker networks._
- Create a new network

  ```
  docker network create <network_name>
  ```

  _Creates a new Docker network._
- Connect a container to a network

  ```
  docker network connect <network_name> <container_name>
  ```

  _Attaches a container to a specific network._

## 📌 Useful Docker Compose Commands

### 🏗️ Managing Services

- Start services defined in docker-compose.yml

  ```
  docker compose up -d
  ```

  _Starts all services in detached mode._
- Stop services

  ```
  docker compose down
  ```

  _Stops and removes all running services._
- Restart services

  ```
  docker compose restart
  ```

  _Restarts all running services._
- Rebuild services (force re-build of images)

  ```
  docker compose up --build
  ```

  _Rebuilds services and runs them._

### 🏗️ Service Management

- List all running services

  ```
  docker-compose ps
  ```

  _Shows all running services._
- View logs for a service

  ```
  docker compose logs -f <service_name>
  ```

  _Streams logs from a specific service._
- Run a command inside a running service

  ```
  docker compose exec <service_name> <command>
  ```

  _Runs a command inside a running container (e.g., /bin/bash)._

### 📂 Volumes and Cleanup

- Remove all stopped services and volumes

  ```
  docker compose down -v
  ```

  _Stops and removes all containers, networks, and volumes._
- Prune unused resources

  ```
  docker system prune -a
  ```

  _Removes all unused containers, images, networks, and caches._

<br>

# 📌 Useful Alembic commands

### 🔹 Create a New Migration <br>

```
alembic revision -m "add users table"
```

✅ This generates a new migration script in alembic/versions/.

💡 But it does not create a migration code, so we should manually add it in a created template

<br>

### 🔹 Automatically Detect Schema Changes

```
alembic revision --autogenerate -m "auto detect changes"
```

✅ Alembic inspects SQLAlchemy models and generates migration code automatically.

💡 Ensure models are imported in env.py for autogeneration to work!

<br>

### 🔹 Apply Migrations to the Database

```
alembic upgrade head
```

✅ This applies all pending migrations up to the latest version.

Use ``alembic upgrade <version_id>`` to apply migrations up to a specific point.

<br>

### 🔹 Revert to a Previous State (Downgrade)

```
alembic downgrade -1
```

✅ This rolls back the last migration.

Use ``alembic downgrade <version_id>`` to revert to a specific version.

<br>

## 📌 Managing Migration History

### 🔹 View Current Migration State

```
alembic current
```

✅ Displays the currently applied migration version.

<br>

### 🔹 Check History of Migrations

```
alembic history
```

✅ Lists all past migrations in order.

<br>

### 🔹 Show Pending Migrations

```
alembic heads
```

✅ Displays the latest (unapplied) migration version(s).

<br>

### 🔹 Manually Stamp Database with a Version

```
alembic stamp head
```

✅ Marks the database as up-to-date without applying migrations.

<br>

## 📌 Common Debugging Commands

### 🔹 Verify Your Migration Script

```
alembic check
```

✅ Checks for issues in migration scripts before applying them.

<br>

### 🔹 Generate SQL Instead of Applying Migration

```
alembic upgrade head --sql
```

✅ Shows SQL statements without running them, useful for debugging.

<br>

## 📌 Cleaning Up and Resetting Migrations

 Here's a step-by-step guide to reset your migrations while preserving your database structure:

## 1. Configure Database Connection

First, ensure your database is running and your connection settings are configured:

```bash
# In your .env file
POSTGRES_HOST=localhost  # Change to localhost if using direct connection
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=fastapi
```

## 2. Start the Database

Make sure your database is running:

```bash
# Start just the database container
docker compose up db
```

## 3. Verify Database Connection

Test your connection to ensure everything is working:

```bash
# Test connection using psql
psql -U postgres -h localhost -d fastapi -c "SELECT 'Connection successful';"
```

## 4. Create a Backup (Optional but Recommended)

Before making changes, back up your existing migrations and database:

```bash
# Backup migrations
mkdir -p alembic/versions_backup
cp -r alembic/versions/* alembic/versions_backup/

# Backup database (optional)
pg_dump -U postgres -h localhost -d fastapi > db_backup.sql
```

## 5. Reset Alembic Version Tracking

Remove migration tracking from the database:

```bash
# Reset Alembic migration state
alembic stamp base
```

## 6. Verify Reset

Check that the version tracking has been reset:

```bash
# Should show no current revision
alembic current
```

## 7. Remove Migration Files

Now you can safely delete the migration files:

```bash
# Remove all migrations
rm -rf alembic/versions/*.py
```

## 8. Create a Fresh Migration

Generate a new migration that captures the current state of your database:

```bash
# Create new migration capturing current schema
alembic revision --autogenerate -m "fresh_start"
```

## 9. Mark the Migration as Applied

Tell Alembic that this new migration has already been applied:

```bash
# Mark as applied
alembic stamp head
```

## 10. Verify Success

Confirm everything worked correctly:

```bash
# Should show your new migration id
alembic current

# Check migration history - should just show your new migration
alembic history
```

> [!NOTE]
> This approach is perfect for local development as it gives you a clean migration history while preserving your database structure and data. It's especially useful when you've accumulated many incremental migrations during development that you don't need to preserve for production.
>

### 🔹 Delete All Migrations and Reset

```
rm -rf alembic/versions/*
alembic revision --autogenerate -m "reset migrations"
alembic upgrade head
```

✅ Deletes old migrations and creates a fresh one based on the current models.

<br>
