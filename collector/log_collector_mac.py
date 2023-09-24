import os
import sys
import platform
import subprocess
import json
import pyodbc
import configparser

def collect_mac_logs(config):
    logs = []

    # Check if the operating system is macOS
    if platform.system() != "Darwin":
        print("Error: This script is intended to run on macOS.")
        sys.exit(1)

    # Collect macOS logs using the appropriate method or command
    try:
        # Modify the command or method to collect macOS logs based on your requirements
        log_command = config.get("MacLogs", "log_command")
        log_data = subprocess.check_output(log_command, shell=True)
        logs = log_data.decode("utf-8").splitlines()
    except Exception as e:
        print(f"Error collecting macOS logs: {str(e)}")
        sys.exit(1)

    return logs

def save_logs_to_database(logs, db_config):
    try:
        # Connect to the database
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()

        # Insert each macOS log entry into the database
        for log in logs:
            cursor.execute("INSERT INTO MacLogTable (LogEntry) VALUES (?)", (log,))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving macOS logs to the database: {str(e)}")
        sys.exit(1)

def save_logs_to_file(logs, output_file):
    try:
        with open(output_file, 'w') as log_file:
            for log in logs:
                log_file.write(log + '\n')
        print(f"Collected macOS logs saved to {output_file}")
    except Exception as e:
        print(f"Error saving macOS logs to file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Collect macOS logs
    mac_logs = collect_mac_logs(config)

    # Option 5: Send collected macOS logs to the database
    db_config = config.get("Database", "db_connection_string")
    if db_config:
        save_logs_to_database(mac_logs, db_config)
        print("Collected macOS logs saved to the database.")

    # Option 6: Save collected macOS logs to a local log file
    output_file = config.get("MacLogs", "output_file")
    if output_file:
        save_logs_to_file(mac_logs, output_file)

    # Option 7: Customize log collection or processing based on your needs
    # You can further process the collected logs here or send them to an API.
    # Example: for log in mac_logs:
    #            process_log(log)
