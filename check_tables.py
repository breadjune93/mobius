import psycopg2
from urllib.parse import urlparse

DATABASE_URL = "postgresql://mobius:endless!%40@211.48.64.197:5432/mobius_agent"

# URL 파싱
result = urlparse(DATABASE_URL)
username = result.username
password = result.password.replace('%40', '@')
database = result.path[1:]
hostname = result.hostname
port = result.port

try:
    # 데이터베이스 연결
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    cursor = conn.cursor()

    # agents 테이블 DDL 조회
    print("=" * 80)
    print("AGENTS TABLE STRUCTURE")
    print("=" * 80)
    cursor.execute("""
        SELECT
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_name = 'agents'
        ORDER BY ordinal_position;
    """)

    agents_columns = cursor.fetchall()
    for col in agents_columns:
        print(f"Column: {col[0]:<20} Type: {col[1]:<20} Max Length: {col[2]:<10} Nullable: {col[3]:<10} Default: {col[4]}")

    # sessions 테이블 DDL 조회
    print("\n" + "=" * 80)
    print("SESSIONS TABLE STRUCTURE")
    print("=" * 80)
    cursor.execute("""
        SELECT
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_name = 'sessions'
        ORDER BY ordinal_position;
    """)

    sessions_columns = cursor.fetchall()
    for col in sessions_columns:
        print(f"Column: {col[0]:<20} Type: {col[1]:<20} Max Length: {col[2]:<10} Nullable: {col[3]:<10} Default: {col[4]}")

    # Primary Keys 확인
    print("\n" + "=" * 80)
    print("PRIMARY KEYS")
    print("=" * 80)

    cursor.execute("""
        SELECT tc.table_name, kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
        AND tc.table_name IN ('agents', 'sessions')
        ORDER BY tc.table_name, kcu.ordinal_position;
    """)

    pks = cursor.fetchall()
    for pk in pks:
        print(f"Table: {pk[0]:<20} Primary Key: {pk[1]}")

    cursor.close()
    conn.close()

    print("\n" + "=" * 80)
    print("SUCCESS: Database schema retrieved successfully")
    print("=" * 80)

except Exception as e:
    print(f"Error: {e}")
