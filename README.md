# Mikro Backend

Backend API for the Mikro transportation application built with FastAPI.

## Features

- User authentication and authorization
- Route management and search
- Location sharing
- Traffic data integration
- Advanced analytics
- Complaint and feedback system
- Friendship management
- Real-time location tracking

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Database Migrations**: Alembic
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx

## Project Structure

```
backend/
├── alembic/                 # Database migrations
├── config/                  # Configuration files
├── frontend/               # Frontend components
├── scripts/                # Utility scripts
├── src/
│   ├── config/             # App configuration
│   ├── models/             # Database models
│   ├── routers/            # API routes
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── main.py            # Application entry point
├── docker-compose.yml      # Docker services
├── Dockerfile             # Container configuration
├── requirements.txt       # Python dependencies
└── nginx.conf            # Nginx configuration
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
python src/main.py
```

## Docker Setup

To run the application using Docker:

```bash
docker-compose up -d
```

## API Documentation

Once the application is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## License

This project is proprietary software. 