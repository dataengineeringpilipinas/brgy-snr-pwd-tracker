# Barangay Senior & PWD Support Tracker

App/Database for monitoring senior citizens and PWDs — for distributing benefits, scheduling visits, or organizing assistance drives.

## Features

- **Senior Citizens Management**: Track and manage senior citizen records
- **PWD Management**: Track and manage Persons with Disabilities records
- **Benefits Distribution**: Record and track benefit distributions
- **Visit Scheduling**: Schedule and track home visits and assessments
- **Assistance Drives**: Organize and track community assistance programs

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
# Option 1: Using the run script
python run.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload
```

3. Access the application:
- **Web interface**: http://localhost:8000
- **API documentation**: http://localhost:8000/docs
- **API root**: http://localhost:8000/api

4. Database:
- The SQLite database (`brgy_snr_pwd.db`) will be created automatically on first run
- For production on Fly.io, configure a volume at `/data` for persistence

## Project Structure

```
app/
├── models/          # Database models (SQLModel)
├── controllers/     # Business logic layer
├── routes/          # API route definitions
├── templates/       # Jinja2 templates with TailwindCSS
├── utils/           # Utility functions
└── database.py      # Database configuration
```

## API Endpoints

- `/api/seniors` - Senior citizens CRUD operations
- `/api/pwds` - PWDs CRUD operations
- `/api/benefits` - Benefits CRUD operations
- `/api/visits` - Visits CRUD operations
- `/api/assistance-drives` - Assistance drives CRUD operations

## Web Pages

- `/` - Dashboard
- `/seniors` - Senior citizens list
- `/pwds` - PWDs list
- `/benefits` - Benefits list
- `/visits` - Visits list
- `/assistance-drives` - Assistance drives list

## License

A Vibecamp Creation
