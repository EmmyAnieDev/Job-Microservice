# Flask Job Listing Service

A Flask-based microservice that handles CRUD operations for job listings in the Job Microservice Application ecosystem.

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

The Flask Job Listing Service is part of a microservice architecture that manages all job listing operations for the Job Portal application. It works in conjunction with:
- **Laravel Service**: User authentication and authorization
- **FastAPI Service**: Job application processing

This service provides comprehensive CRUD (Create, Read, Update, Delete) operations for job listings.

## Features

- ✅ Complete CRUD Operations for Job Listings
- ✅ RESTful API Design
- ✅ Database Migrations with Alembic
- ✅ Input Validation & Sanitization
- ✅ CORS Support for Microservice Communication
- ✅ Comprehensive Error Handling
- ✅ Docker Support

## Project Structure

```
job-listing-service/
├── .venv/                      # Virtual environment (created after setup)
├── app/                       # Main application package
│   ├── api/                   # API layer
│   │   ├── db/               # Database utilities
│   │   ├── utils/            # Utility functions
│   │   └── v1/               # API version 1
│   │       ├── models/       # Database models
│   │       ├── routes/       # API route handlers
│   │       ├── schemas/      # Pydantic schemas/marshmallow
│   │       ├── services/     # Business logic layer
│   │       ├── __init__.py
│   │       └── __init__.py
│   ├── __init__.py
│   └── __init__.py
├── migrations/                 # Additional migration files
├── tests/                     # Test files
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_jobs.py          # Job-related tests
│   └── test_api.py           # API endpoint tests
├── .dockerignore              # Docker ignore file
├── .env                       # Environment variables (created from .env.sample)
├── .env.sample               # Environment variables template
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration file
├── config.py                 # Application configuration
├── Dockerfile                # Docker container configuration
├── Jenkinsfile              # Jenkins CI/CD pipeline
├── main.py                  # Application entry point
└── requirements.txt         # Python dependencies
```

### Key Directories Explained

- **`app/`**: Core application code
    - **`api/v1/`**: Version 1 of the API
        - **`models/`**: SQLAlchemy database models
        - **`routes/`**: Flask route definitions and handlers
        - **`schemas/`**: Input/output validation schemas
        - **`services/`**: Business logic and service layer
- **`tests/`**: Unit and integration tests
- **`migrations/`**: database migration scripts

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
    cd Job-Microservice/job-listing-service
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
DATABASE_URL=postgresql://username:password@localhost:5432/job_listings_db
# Alternative for MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/job_listings_db
# Alternative for SQLite
# DATABASE_URL=sqlite:///./job_listings.db

# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

## Database Setup

### 1. Create Database

Create a new database for the job listing service:

```sql
-- For PostgreSQL
CREATE DATABASE job_listings_db;

-- For MySQL
CREATE DATABASE job_listings_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
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

Start the Flask development server:

```bash
    python main.py
```

The job listing service will be available at: `http://localhost:5000`

### Alternative Run Methods

```bash
    # Using Flask CLI
    flask run --host=0.0.0.0 --port=5000
    
    # Using Gunicorn (Production)
    gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Production Deployment

For production deployment with Gunicorn:

```bash
    # Install Gunicorn
    pip install gunicorn
    
    # Run with Gunicorn
    gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 main:app
```

## API Endpoints

### Job Listing Routes

| Method | Endpoint                | Description                  | Authentication |
|--------|-------------------------|------------------------------|----------------|
| GET | `/api`                  | Api status check             | No |
| GET | `/api/v1/jobs`          | Get all jobs with pagination | No             |
| GET | `/api/v1/jobs/{job_id}` | Get specific job by ID       | No             |
| POST | `/api/v1/jobs`          | Create new job listing       | No             |
| PUT | `/api/v1/jobs/{job_id}` | Update existing job          | No             |
| DELETE | `/api/v1/jobs/{job_id}` | Delete job listing           | No             |


## Testing

### Run Tests

Execute the test suite:

```bash
    # Run all tests
    python -m pytest
    
    # Run with coverage
    python -m pytest --cov=app
    
    # Run specific test file
    python -m pytest tests/test_jobs.py
    
    # Run with verbose output
    python -m pytest -v
```

## Docker Support

### Build and Run with Docker

```bash
    # Build the image
    docker build -t job-listing-service .
    
    # Run the container
    docker run -p 5000:5000 --env-file .env job-listing-service
```

### Docker Compose

In the main Job-Microservice directory, add to `docker-compose.yml`:

Run with Docker Compose:

```bash
    docker-compose up -d --build
```

**Note**: This is the job listing service for the Job Microservice Application. Make sure to also set up the Laravel (authentication) and FastAPI (job applications) services for the complete application to function properly.