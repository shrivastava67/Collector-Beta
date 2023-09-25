import os
import sys
import platform
import subprocess
import json
import pyodbc
import configparser

def collect_linux_logs(config):
    logs = []

    # Check if the operating system is Linux
    if platform.system() != "Linux":
        print("Error: This script is intended to run on Linux.")
        sys.exit(1)

    # Collect logs using the 'rsyslog' command-line tool (example command)
    try:
        log_file_paths = config.get("LinuxLogs", "log_file_paths").split(',')
        for log_file_path in log_file_paths:
            log_data = subprocess.check_output(
                ["cat", log_file_path.strip()]
            )
            # For this example, we assume logs are in plain text format; you may need to adapt this for your log format.
            log_entries = log_data.decode("utf-8").splitlines()
            logs.extend(log_entries)
    except Exception as e:
        print(f"Error collecting Linux logs: {str(e)}")
        sys.exit(1)

    return logs

def save_logs_to_database(logs, db_config):
    try:
        # Connect to the database
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()

        # Insert each log entry into the database
        for log in logs:
            cursor.execute("INSERT INTO LogTable (LogEntry) VALUES (?)", (log,))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving logs to the database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Collect Linux logs
    linux_logs = collect_linux_logs(config)

    # Option 5: Send collected logs to the database
    db_config = config.get("Database", "db_connection_string")
    if db_config:
        save_logs_to_database(linux_logs, db_config)
        print("Collected logs saved to the database.")

    # Option 6: Customize log collection or processing based on your needs
    # You can further process the collected logs here, save them to a database, or send them to an API.
    # Example: for log in linux_logs:
    #            process_log(log)
