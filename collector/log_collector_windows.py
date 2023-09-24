import os
import sys
import platform
import subprocess
import json
import pyodbc
import configparser

def collect_windows_logs(config):
    logs = []

    # Check if the operating system is Windows
    if platform.system() != "Windows":
        print("Error: This script is intended to run on Windows.")
        sys.exit(1)

    # Collect event logs using the 'wevtutil' command-line tool
    try:
        log_names = config.get("WindowsLogs", "log_names").split(',')
        for log_name in log_names:
            log_data = subprocess.check_output(
                ["wevtutil", "qe", log_name.strip(), "/f:json"]
            )
            log_entries = json.loads(log_data)
            logs.extend(log_entries)
    except Exception as e:
        print(f"Error collecting Windows logs: {str(e)}")
        sys.exit(1)

    return logs

def save_logs_to_database(logs, db_config):
    try:
        # Connect to the database
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()

        # Insert each log entry into the database
        for log in logs:
            log_json = json.dumps(log)
            cursor.execute("INSERT INTO LogTable (LogEntry) VALUES (?)", (log_json,))
        
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

    # Collect Windows logs
    windows_logs = collect_windows_logs(config)

    # Option 5: Save collected logs to a JSON file
    output_file = config.get("WindowsLogs", "output_file")
    if output_file:
        try:
            with open(output_file, 'w') as json_file:
                json.dump(windows_logs, json_file, indent=4)
            print(f"Collected logs saved to {output_file}")
        except Exception as e:
            print(f"Error saving logs to JSON file: {str(e)}")

    # Option 6: Send collected logs to the database
    db_config = config.get("Database", "db_connection_string")
    if db_config:
        save_logs_to_database(windows_logs, db_config)
        print("Collected logs saved to the database.")

    # Option 7: Customize log collection or processing based on your needs
    # You can further process the collected logs here, save them to a database, or send them to an API.
    # Example: for log in windows_logs:
    #            process_log(log)
