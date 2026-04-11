# Quick Start - Database Seeder

## Run from project root

```bash
# Option 1: Using the shell script
./scripts/seed-database.sh

# Option 2: Using Makefile
make seed-db

# Option 3: Direct Python (if in backend venv)
python scripts/seed_database.py
```

## Reset and reseed (WARNING: destroys all data!)

```bash
# Using the shell script
./scripts/seed-database.sh --reset

# Using Makefile
make seed-db-reset
```

## Custom .env file

```bash
./scripts/seed-database.sh --env /path/to/your/.env
```

## What you get

✅ 3 roles (admin, professor, student)  
✅ 1 admin user (superadmin / adminpass123)  
✅ 5 professors with complete profiles  
✅ 20 students with profiles  
✅ LMS credentials for professors + 10 students  
✅ 5 educational games with 12 levels and 24 segments  
✅ 10-30 game instances  
✅ 8 academic courses with professors  
✅ 40-100 course enrollments  
✅ 7 metric types  
✅ 15 feedback records  
✅ Progress records for students  
✅ 50 xAPI statements  
✅ 60-150 notifications  

All passwords are `password123` for users, `adminpass123` for admin.

## Full documentation

See `scripts/README_SEED.md` for complete documentation.
