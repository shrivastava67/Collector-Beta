import psycopg2
import pymssql
import pymysql
import sys

def connect_to_database(db_config):
    try:
        db_type = db_config.get("db_type").lower()
        if db_type == "postgresql":
            conn = psycopg2.connect(**db_config)
        elif db_type == "mssql":
            conn = pymssql.connect(**db_config)
        elif db_type == "mariadb":
            conn = pymysql.connect(**db_config)
        else:
            print("Error: Unsupported database type specified in config.")
            sys.exit(1)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        sys.exit(1)

def create_log_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LogTable (
                id SERIAL PRIMARY KEY,
                log_entry TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating log table: {str(e)}")
        conn.rollback()
        sys.exit(1)

def insert_log_entry(conn, log_entry):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO LogTable (log_entry) VALUES (%s)", (log_entry,))
        conn.commit()
    except Exception as e:
        print(f"Error inserting log entry into the database: {str(e)}")
        conn.rollback()
        sys.exit(1)

def get_logs_from_database(conn, start_time=None, end_time=None):
    try:
        cursor = conn.cursor()
        query = "SELECT log_entry, timestamp FROM LogTable"
        if start_time and end_time:
            query += " WHERE timestamp BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
        else:
            cursor.execute(query)
        logs = cursor.fetchall()
        return logs
    except Exception as e:
        print(f"Error retrieving logs from the database: {str(e)}")
        conn.rollback()
        sys.exit(1)

def close_database_connection(conn):
    try:
        conn.close()
    except Exception as e:
        print(f"Error closing the database connection: {str(e)}")
        sys.exit(1)
