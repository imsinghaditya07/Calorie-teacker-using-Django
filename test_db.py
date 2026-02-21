"""
Script to test Supabase database connection.
"""
import dj_database_url
import psycopg2

db_url = 'postgresql://postgres:%40Harshakaadit01@db.hefslfmprncrqulbdjgy.supabase.co:5432/postgres'
db = dj_database_url.parse(db_url)
try:
    conn = psycopg2.connect(
        dbname=db['NAME'],
        user=db['USER'],
        password=db['PASSWORD'],
        host=db['HOST'],
        port=db['PORT']
    )
    print("SUCCESS")
except Exception as e:
    print("FAILED", e)
