# Hackathon Management System Backend

A complete FastAPI backend for managing hackathons, teams, tasks, and submissions with advanced JWT authentication and role-based access control.

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLModel** - SQL database ORM with Pydantic integration
- **PostgreSQL** - Production relational database
- **Alembic** - Database migrations
- **JWT (python-jose)** - Authentication tokens
- **Passlib + bcrypt** - Password hashing and verification

## Project Structure

```
app/
├── core/                    # Configuration and security
│   ├── config.py           # Settings management
│   └── security.py         # JWT, hashing, authentication
├── models/                 # SQLModel domain models
│   ├── user.py
│   ├── hackathon.py
│   ├── team.py
│   ├── task.py
│   ├── submission.py
│   └── evaluation.py
├── schemas/                # Pydantic request/response models
│   ├── auth.py
│   ├── user.py
│   ├── hackathon.py
│   ├── team.py
│   ├── task.py
│   ├── submission.py
│   ├── evaluation.py
│   └── token.py
├── services/               # Business logic layer
│   ├── user_service.py
│   ├── hackathon_service.py
│   ├── team_service.py
│   ├── task_service.py
│   ├── submission_service.py
│   └── evaluation_service.py
├── routers/                # API endpoint handlers
│   ├── auth.py            # Authentication (register, login, me)
│   ├── users.py           # User management
│   ├── hackathons.py      # Hackathon CRUD
│   ├── teams.py           # Team CRUD + join
│   ├── tasks.py           # Task CRUD
│   ├── submissions.py     # Submission CRUD
│   └── evaluations.py     # Evaluation CRUD
├── migrations/            # Alembic database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── database.py            # Database connection and session
└── main.py               # FastAPI application entry point
```

## Domain Models & Relationships

### User
- **Fields**: id, email (unique), name, password_hash, role
- **Roles**: participant, organizer, judge
- **Relations**: Has many TeamMember (bidirectional), Has many Evaluation as judge

### Hackathon
- **Fields**: id, title, description, start_date, end_date
- **Relations**: Has many Team, Has many Task

### Team
- **Fields**: id, name, hackathon_id
- **Relations**: Has many TeamMember (participants), Has many Submission, Belongs to Hackathon

### TeamMember (Associative Entity)
- **Fields**: user_id (PK), team_id (PK), role_in_team (extra field)
- **Purpose**: Many-to-many relationship between User and Team with role context

### Task
- **Fields**: id, title, description, hackathon_id
- **Relations**: Belongs to Hackathon, Has many Submission

### Submission
- **Fields**: id, team_id, task_id, github_url, created_at
- **Relations**: Belongs to Team, Belongs to Task, Has many Evaluation

### Evaluation
- **Fields**: id, submission_id, judge_id, score, comment
- **Relations**: Belongs to Submission, Belongs to User (as judge)

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current authenticated user
- `POST /auth/change-password` - Change user password

### Users
- `GET /users/` - List all users (organizers only)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user profile

### Hackathons
- `GET /hackathons/` - List all hackathons
- `POST /hackathons/` - Create hackathon (organizers only)
- `GET /hackathons/{hackathon_id}` - Get hackathon with teams and tasks
- `PUT /hackathons/{hackathon_id}` - Update hackathon (organizers only)
- `DELETE /hackathons/{hackathon_id}` - Delete hackathon (organizers only)

### Teams
- `GET /teams/` - List all teams
- `POST /teams/` - Create team
- `GET /teams/{team_id}` - Get team with members
- `POST /teams/{team_id}/join` - Join team as member
- `PUT /teams/{team_id}` - Update team (organizers only)
- `DELETE /teams/{team_id}` - Delete team (organizers only)

### Tasks
- `GET /tasks/` - List all tasks
- `POST /tasks/` - Create task (organizers only)
- `GET /tasks/{task_id}` - Get task details
- `PUT /tasks/{task_id}` - Update task (organizers only)
- `DELETE /tasks/{task_id}` - Delete task (organizers only)

### Submissions
- `GET /submissions/` - List all submissions
- `POST /submissions/` - Create submission
- `GET /submissions/{submission_id}` - Get submission
- `PUT /submissions/{submission_id}` - Update submission
- `DELETE /submissions/{submission_id}` - Delete submission

### Evaluations
- `GET /evaluations/` - List all evaluations
- `POST /evaluations/` - Create evaluation (judges only)
- `GET /evaluations/{evaluation_id}` - Get evaluation
- `PUT /evaluations/{evaluation_id}` - Update evaluation (judges only)
- `DELETE /evaluations/{evaluation_id}` - Delete evaluation (judges/organizers only)

## Security Features

- **Password Hashing**: bcrypt with passlib
- **JWT Authentication**: OAuth2PasswordBearer with HS256
- **Role-Based Access Control**: participant, organizer, judge roles
- **Dependency Injection**: Database session & user authentication
- **No Password Exposure**: password_hash never returned in API responses

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database URL and JWT secret
```

### 3. Initialize Database

```bash
# Create tables (if CREATE_TABLES_ON_STARTUP=True)
# OR run migrations with Alembic:
alembic upgrade head
```

### 4. Run Application

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Database Migrations (Alembic)

### Create Migration
```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

## Example Usage

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "secure_password",
    "role": "participant"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secure_password"
```

### Create Hackathon (Organizer)
```bash
curl -X POST http://localhost:8000/hackathons/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "TechHack 2025",
    "description": "Annual tech hackathon",
    "start_date": "2025-04-15",
    "end_date": "2025-04-17"
  }'
```

## Architecture Highlights

- **Clean Separation**: Models, schemas, services, and routers in separate modules
- **Dependency Injection**: FastAPI dependencies for DB session and user auth
- **Type Safety**: Full type hints throughout the codebase
- **Proper Error Handling**: HTTP exceptions with appropriate status codes
- **Nested Responses**: Hackathons include teams and tasks, teams include members
- **Eager Loading**: selectinload for preventing N+1 query problems
- **Production Ready**: Docker support, environment configuration, migrations

## Requirements

See [requirements.txt](requirements.txt) for all dependencies.
