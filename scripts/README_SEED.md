# Database Seeder Script

## Overview

This script completely populates the Hello World Project database with realistic test data based on the actual database schemas.

## Location

`scripts/seed_database.py`

## Prerequisites

1. The backend dependencies must be installed
2. Database must be accessible and migrations applied
3. Environment variables configured (DATABASE_URL)

## Usage

### Basic Usage

```bash
# Run from project root
python scripts/seed_database.py
```

### With Custom .env File

```bash
python scripts/seed_database.py --env apps/backend/.env
```

### Reset Database Before Seeding

⚠️ **WARNING**: This will destroy all existing data!

```bash
python scripts/seed_database.py --reset
```

## What Gets Seeded

The script seeds data in the following order:

### Phase 1: Core Data
- **Roles**: admin, professor, student
- **Admin User**: superadmin account

### Phase 2: Users
- **5 Professors** with complete profiles (department, contact info)
- **20 Students** with profiles

### Phase 3: LMS Credentials
- LMS credentials for all 5 professors
- LMS credentials for first 10 students

### Phase 4: Games
- **5 Educational Games** with complete structure:
  - Matemáticas Básicas (3 levels, 7 segments)
  - Química Introductoria (2 levels, 3 segments)
  - Física Fundamental (2 levels, 5 segments)
  - Biología Celular (2 levels, 2 segments)
  - Programación con Python (3 levels, 7 segments)

### Phase 5: Game Instances
- **10-30 game instances** distributed among first 10 students
- Random statuses: COMPLETED, ACTIVE, FAILED

### Phase 6: Courses
- **8 Academic Courses** with professors assigned:
  - Introducción a la Programación
  - Matemáticas Discretas
  - Química General
  - Física I
  - Biología Celular
  - Estructuras de Datos
  - Cálculo Diferencial
  - Base de Datos

### Phase 7: Course Enrollments
- **40-100 enrollments** (each student enrolled in 2-5 courses)

### Phase 8: Statistics
- **7 Metric Types** (accuracy, time_spent, attempts, etc.)
- **15 Feedback records** from students to professors
- **Progress records** for students in game segments
- **50 xAPI statements** from game interactions

### Phase 9: Notifications
- **60-150 notifications** distributed across users
- Various types: game_invite, course_enrollment, feedback_received, etc.

## Test Accounts

### Admin
- **Username**: superadmin
- **Password**: adminpass123
- **Email**: admin@example.com

### Professors
- **Usernames**: prof_juan_perez, prof_maria_lopez, prof_carlos_garcia, prof_ana_martinez, prof_roberto_sanchez
- **Password**: password123 (all professors)

### Students
- **Usernames**: student_001 through student_020
- **Password**: password123 (all students)

## Configuration

The script uses the backend's database configuration. Ensure your `.env` file has:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database_name
# or for SQLite:
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

## Technical Details

- **Async/Await**: Uses SQLAlchemy async session
- **Idempotent**: Safe to run multiple times (skips existing records)
- **Realistic Data**: Uses actual Spanish names, realistic emails, and proper relationships
- **Randomization**: Some data uses randomization for variety (game instances, enrollments, etc.)

## Troubleshooting

### "DATABASE_URL environment variable is not set"
Make sure your `.env` file exists and has the DATABASE_URL configured.

### "Connection refused"
Verify your database is running and accessible. Check host, port, and credentials.

### "Table doesn't exist"
Run database migrations first:
```bash
cd apps/backend
alembic upgrade head
```

### Import errors
Ensure you're running the script from the project root directory, not from within the scripts folder.

## Example Output

```
======================================================================
Hello World Project - Database Seeder
======================================================================
Loading environment from: /path/to/apps/backend/.env
Database URL: postgresql+asyncpg://...
Reset database: No

[Phase 1] Seeding roles and admin...
  ✓ Seeded role: admin
  ✓ Seeded role: professor
  ✓ Seeded role: student
  ✓ Seeded admin user: superadmin

[Phase 2] Seeding users...
  ✓ Seeded professor: prof_juan_perez
  ...
  ✓ Total: 5 professors, 20 students

...

======================================================================
Seeding completed successfully!
======================================================================
```
