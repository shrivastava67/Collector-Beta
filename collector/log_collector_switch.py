import os
import sys
import platform
import subprocess
import json
import pyodbc
import configparser

def collect_switch_logs(config):
    logs = []

    # Check if the operating system is compatible with switch log collection
    if platform.system() not in ["Windows", "Linux"]:
        print("Error: This script is intended to run on Windows or Linux.")
        sys.exit(1)

    # Collect switch logs using the appropriate method or command
    try:
        # Modify the command or method to collect switch logs based on your switch device
        switch_command = config.get("SwitchLogs", "switch_command")
        switch_log_data = subprocess.check_output(switch_command, shell=True)
        switch_logs = switch_log_data.decode("utf-8").splitlines()

        logs.extend(switch_logs)
    except Exception as e:
        print(f"Error collecting switch logs: {str(e)}")
        sys.exit(1)

    return logs

def save_logs_to_database(logs, db_config):
    try:
        # Connect to the database
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()

        # Insert each switch log entry into the database
        for log in logs:
            cursor.execute("INSERT INTO SwitchLogTable (LogEntry) VALUES (?)", (log,))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving switch logs to the database: {str(e)}")
        sys.exit(1)

def save_logs_to_file(logs, output_file):
    try:
        with open(output_file, 'w') as log_file:
            for log in logs:
                log_file.write(log + '\n')
        print(f"Collected switch logs saved to {output_file}")
    except Exception as e:
        print(f"Error saving switch logs to file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Collect switch logs
    switch_logs = collect_switch_logs(config)

    # Option 5: Send collected switch logs to the database
    db_config = config.get("Database", "db_connection_string")
    if db_config:
        save_logs_to_database(switch_logs, db_config)
        print("Collected switch logs saved to the database.")

    # Option 6: Save collected switch logs to a local log file
    output_file = config.get("SwitchLogs", "output_file")
    if output_file:
        save_logs_to_file(switch_logs, output_file)

    # Option 7: Customize log collection or processing based on your needs
    # You can further process the collected logs here or send them to an API.
    # Example: for log in switch_logs:
    #            process_log(log)
