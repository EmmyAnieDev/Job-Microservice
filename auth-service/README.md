# Laravel Auth Service

A Laravel-based authentication microservice that provides secure user authentication and authorization for the Job Microservice Application ecosystem.

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

The Laravel Auth Service is part of a microservice architecture that handles all authentication-related operations for the Job Portal application. It works in conjunction with:
- **Flask Service**: Job listing management
- **FastAPI Service**: Job application processing

This service provides secure user registration, login, logout, and token-based authentication using JWT.

## Features

- ✅ User Registration & Login
- ✅ JWT Token Authentication
- ✅ Token Validation for API Gateway
- ✅ CORS Support for Microservice Communication
- ✅ Comprehensive Input Validation
- ✅ Security Headers & Middleware
- ✅ API Versioning (v1)
- ✅ Docker Support
- ✅ Comprehensive Testing Suite

## Project Structure

```
auth-service/
├── app/                        # Core application code
│   ├── Facades/               # Custom Laravel facades
│   ├── Http/                  # HTTP layer
│   │   ├── Controllers/       # API controllers
│   │   ├── Middleware/        # Custom middleware
│   │   ├── Requests/          # Form request validation
│   │   └── Resources/         # API resources
│   ├── Models/                # Eloquent models
│   │   └── User.php          # User model
│   ├── Providers/             # Service providers
│   ├── Services/              # Business logic services
│   └── Traits/                # Reusable traits
├── bootstrap/                  # Application bootstrap files
├── config/                     # Configuration files
│   ├── app.php               # Main app configuration
│   ├── auth.php              # Authentication configuration
│   ├── cors.php              # CORS configuration
│   ├── database.php          # Database configuration
│   └── jwt.php               # JWT configuration
├── database/                   # Database files
│   ├── factories/            # Model factories
│   ├── migrations/           # Database migrations
│   └── seeders/              # Database seeders
├── node_modules/              # NPM dependencies (after npm install)
├── public/                    # Public web files
│   ├── index.php             # Application entry point
│   └── assets/               # Static assets
├── resources/                 # Application resources
│   ├── views/                # Blade templates
│   ├── lang/                 # Language files
│   └── js/                   # JavaScript files
├── routes/                    # Route definitions
│   ├── api.php               # API routes
│   ├── web.php               # Web routes
│   └── console.php           # Console routes
├── storage/                   # Storage files
│   ├── app/                  # Application storage
│   ├── framework/            # Framework storage
│   └── logs/                 # Application logs
├── tests/                     # Test files
│   ├── Feature/              # Feature tests
│   ├── Unit/                 # Unit tests
│   └── TestCase.php          # Base test case
├── vendor/                    # Composer dependencies
├── .dockerignore              # Docker ignore file
├── .editorconfig             # Editor configuration
├── .env                      # Environment variables (created from .env.example)
├── .env.example              # Environment template
├── .env.testing              # Testing environment
├── .gitattributes            # Git attributes
├── .gitignore                # Git ignore file
├── artisan                   # Artisan command line tool
├── composer.json             # PHP dependencies
├── composer.lock             # Locked PHP dependencies
├── Dockerfile                # Docker container configuration
├── package.json             # Node.js dependencies
├── package-lock.json        # Locked Node.js dependencies
├── phpunit.xml              # PHPUnit configuration
├── README.md                # Project documentation
└── vite.config.js           # Vite build configuration
```

### Key Directories Explained

- **`app/`**: Core Laravel application code
    - **`Http/Controllers/`**: API controllers handling requests
    - **`Models/`**: Eloquent ORM models
    - **`Services/`**: Business logic layer
    - **`Providers/`**: Service providers for dependency injection
- **`config/`**: Configuration files for various Laravel components
- **`database/`**: Database-related files (migrations, seeders, factories)
- **`routes/`**: Route definitions for API and web endpoints
- **`tests/`**: PHPUnit test files for feature and unit testing
- **`storage/`**: File storage and application logs

## Requirements

- **PHP**: >= 8.1
- **Composer**: >= 2.0
- **Database**: MySQL 8.0+ / PostgreSQL 13+ / SQLite 3.8+
- **Node.js**: >= 16.x (for asset compilation)
- **Git**: Latest version

## Installation

### 1. Clone the Repository

```bash
    git clone https://github.com/EmmyAnieDev/Job-Microservice.git
    cd Job-Microservice/auth-service
```

### 2. Install PHP Dependencies

```bash
    composer install
```

### 3. Install Node.js Dependencies (Optional)

```bash
    npm install
    # or
    yarn install
```

### 4. Environment Setup

Copy the example environment file and configure it:

```bash
    cp .env.example .env
```

### 5. Generate Application Key

```bash
    php artisan key:generate
```

## Configuration

### Database Configuration

Edit your `.env` file with your database credentials:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=job_auth_service
DB_USERNAME=your_username
DB_PASSWORD=your_password
```

### JWT Configuration

Configure JWT settings for token authentication:

```env
JWT_SECRET=your-jwt-secret-key
ACCESS_TIME_TO_LIVE=60
REFRESH_TIME_TO_LIVE=6400
JWT_ALGORITHM=HS256
JTI_TIME_TO_LIVE=60
```

## Database Setup

### 1. Create Database

Create a new database for the auth service:

```sql
CREATE DATABASE job_auth_service;
```

### 2. Run Migrations

Execute the database migrations:

```bash
    php artisan migrate
```

## Running the Application

### Development Server

Start the Laravel development server:

```bash
    php artisan serve
```

The auth service will be available at: `http://localhost:8000`

### Production Setup

For production deployment:

1. **Optimize Application**:
```bash
    php artisan config:cache
    php artisan route:cache
    php artisan view:cache
```

2. **Set Environment**:
```bash
    APP_ENV=production
    APP_DEBUG=false
```

3. **Use a Process Manager**:
```bash
    # Example with PM2
    pm2 start "php artisan serve --host=0.0.0.0 --port=8000" --name="auth-service"
```

## API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api` | API status check | No |
| POST | `/api/v1/auth/register` | User registration | No |
| POST | `/api/v1/auth/login` | User login | No |
| POST | `/api/v1/auth/logout` | User logout | Yes |
| POST | `/api/v1/auth/refresh` | Refresh token | Yes |
| POST | `/api/v1/auth/validate-token` | Validate token for Traefik API Gateway JWT Authentication | Yes |
| GET | `/api/v1/auth/validate-token` | Validate token for Traefik API Gateway JWT Authentication | Yes |
| GET | `/api/v1/me` | Get authenticated user | Yes |

## Testing

### Run Tests

Execute the test suite:

```bash
    # Run all tests
    php artisan test
    
    # Run specific test file
    php artisan test tests/Feature/AuthTest.php
    
    # Run with coverage
    php artisan test --coverage
    
    # Run unit tests only
    php artisan test --testsuite=Unit
    
    # Run feature tests only
    php artisan test --testsuite=Feature
```

### Logs

Check Laravel logs for debugging:

```bash
    tail -f storage/logs/laravel.log
```

### Debug Mode

Enable debug mode for detailed error messages:

```env
    APP_DEBUG=true
    APP_ENV=local
```

## Docker Support

### Dockerfile

### Build and Run with Docker

```bash
    # Build the image
    docker build -t auth-service .
    
    # Run the container
    docker run -p 8001:8001 --env-file .env auth-service
```

### Docker Compose

In the main Job-Microservice directory, cd to `docker-compose.yml`:

Run with Docker Compose:

```bash
    cd ..
    docker-compose up -d --build
```

**Note**: This is the authentication service for the Job Microservice Application. Make sure to also set up the Flask (job listings) and FastAPI (job applications) services for the complete application to function properly.
