# FastAPI Job Application Service

A FastAPI-based microservice that handles job application operations in the Job Microservice Application ecosystem.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Docker Support](#docker-support)

## Overview

The FastAPI Job Application Service is part of a microservice architecture that manages all job application operations for the Job Portal application. It works in conjunction with:
- **Laravel Service**: User authentication and authorization
- **Flask Service**: Job listing management

This service provides comprehensive operations for job applications including applying to jobs, and deleting applied jobs.

## Features

- ✅ Complete Job Application Operations
- ✅ RESTful API Design with FastAPI
- ✅ Database Migrations with Alembic
- ✅ Input Validation with Pydantic
- ✅ CORS Support for Microservice Communication
- ✅ Comprehensive Error Handling
- ✅ Automatic API Documentation (Swagger/OpenAPI)
- ✅ Docker Support
- ✅ Async/Await Support

## Project Structure

```
job-application-service/
├── .venv/                      # Virtual environment (created after setup)
├── app/                       # Main application package
│   ├── api/                   # API layer
│   │   ├── db/               # Database utilities
│   │   ├── utils/            # Utility functions
│   │   └── v1/               # API version 1
│   │       ├── models/       # Database models
│   │       ├── routes/       # API route handlers
│   │       ├── schemas/      # Pydantic schemas
│   │       ├── services/     # Business logic layer
│   │       ├── __init__.py
│   │       └── __init__.py  
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── migrations/                   # Alembic migration files
├── tests/                     # Test files
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_applications.py  # Application-related tests
├── .dockerignore              # Docker ignore file
├── .env                       # Environment variables (created from .env.sample)
├── .env.sample               # Environment variables template
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration file
├── Dockerfile                # Docker container configuration
├── main.py                  # Application entry point
└── requirements.txt         # Python dependencies
```

### Key Directories Explained

- **`app/`**: Core application code
    - **`api/v1/`**: Version 1 of the API
        - **`models/`**: SQLAlchemy database models
        - **`routes/`**: FastAPI route definitions and handlers
        - **`schemas/`**: Pydantic models for input/output validation
        - **`services/`**: Business logic and service layer
        - **`config.py`**: Application settings using Pydantic
        - **`database.py`**: Database connection and session management
- **`tests/`**: Unit and integration tests
- **`migrations/`**: Database migration scripts

## Requirements

- **Python**: >= 3.8
- **pip**: Latest version
- **Database**: PostgreSQL 12+ / MySQL 8.0+ / SQLite 3.8+
- **Docker**: >= 20.10 (optional)
- **Git**: Latest version

## Installation

### 1. Clone the Repository

```bash
    git clone https://github.com/EmmyAnieDev/Job-Microservice.git
    cd Job-Microservice/job-apply-service
```

### 2. Create Virtual Environment

```bash
    # Create virtual environment
    python -m venv .venv
    
    # Activate virtual environment
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
```

### 3. Install Dependencies

```bash
    pip install -r requirements.txt
```

### 4. Environment Setup

Copy the sample environment file and configure it:

```bash
    cp .env.sample .env
```

## Configuration

### Database Configuration

Edit your `.env` file with your database credentials:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/job_applications_db
# Alternative for MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/job_applications_db
# Alternative for SQLite
# DATABASE_URL=sqlite:///./job_applications.db

# Application Configuration
APP_NAME=Job Application Service
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here

# External Services
JOB_LISTING_BASE_URL=http://job-listing-service:5000
```

## Database Setup

### 1. Create Database

Create a new database for the job application service:

```sql
-- For PostgreSQL
CREATE DATABASE job_applications_db;

-- For MySQL
CREATE DATABASE job_applications_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Initialize Alembic (if not already done)

```bash
    alembic init alembic
```

### 3. Run Database Migrations

Execute the database migrations using Alembic:

```bash
    alembic upgrade head
```

## Running the Application

### Development Server

Start the FastAPI development server:

```bash
    python main.py
```

The job application service will be available at: `http://localhost:8001`

**API Documentation** will be available at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

### Alternative Run Methods

```bash
    # Using Uvicorn directly
    uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
    
    # Using Uvicorn with workers (Production)
    uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

### Production Deployment

For production deployment with Gunicorn + Uvicorn:

```bash
    # Install Gunicorn
    pip install gunicorn
    
    # Run with Gunicorn + Uvicorn workers
    gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

## API Endpoints

### Job Application Routes

| Method | Endpoint                        | Description                        | Authentication              |
|--------|---------------------------------|------------------------------------|-----------------------------|
| GET    | `/`                             | API status check                   | No                          |
| GET    | `/health`                       | Health check endpoint              | No                          |
| POST   | `/api/v1/applications`          | Apply for a job                    | Depends on JWT from Headers |
| DELETE | `/api/v1/applications/{app_id}` | Delete/withdraw application        | Depends on JWT from Headers |


## Testing

### Run Tests

Execute the test suite:

```bash
    # Run all tests
    pytest
    
    # Run with coverage
    pytest --cov=app
    
    # Run specific test file
    pytest tests/test_applications.py
    
    # Run with verbose output
    pytest -v
    
    # Run async tests
    pytest -v --asyncio-mode=auto
```

## Docker Support

### Dockerfile

### Build and Run with Docker

```bash
    # Build the image
    docker build -t job-application-service .
    
    # Run the container
    docker run -p 8001:8001 --env-file .env job-application-service
```

### Docker Compose

In the main Job-Microservice directory, cd to `docker-compose.yml`:

Run with Docker Compose:

```bash
    cd ..
    docker-compose up -d --build
```

**Note**: This is the job application service for the Job Microservice Application. Make sure to also set up the Laravel (authentication) and Flask (job listings) services for the complete application to function properly.

The service provides automatic API documentation at `/docs` and `/redoc` endpoints when running in development mode.