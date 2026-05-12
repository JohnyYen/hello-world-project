import asyncpg
import asyncio

async def check():
    conn = await asyncpg.connect(host='postgresql_db', user='value', password='password', database='hwp_db')
    
    print("=== VERIFICATION ===")
    print(f"Students: {await conn.fetchval('SELECT COUNT(*) FROM students')}")
    print(f"Courses: {await conn.fetchval('SELECT COUNT(*) FROM courses')}")
    print(f"Enrollments: {await conn.fetchval('SELECT COUNT(*) FROM course_enrollments')}")
    print(f"Sync events: {await conn.fetchval('SELECT COUNT(*) FROM sync_events')}")
    print(f"Game instances: {await conn.fetchval('SELECT COUNT(*) FROM game_instances')}")
    print(f"Progress: {await conn.fetchval('SELECT COUNT(*) FROM progresses')}")
    print(f"xAPI: {await conn.fetchval('SELECT COUNT(*) FROM xapi_statements')}")
    
    # Show courses by year
    print("\nCourses by year:")
    rows = await conn.fetch('SELECT school_year, COUNT(*) as cnt FROM courses GROUP BY school_year ORDER BY school_year')
    for r in rows:
        print(f"  {r['school_year']}: {r['cnt']} courses")
    
    await conn.close()

asyncio.run(check())
