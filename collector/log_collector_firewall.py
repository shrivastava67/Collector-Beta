import os
import sys
import platform
import subprocess
import json
import pyodbc
import configparser

def collect_firewall_logs(config):
    logs = []

    # Check if the operating system is compatible with the firewall log collection method
    if platform.system() not in ["Windows", "Linux"]:
        print("Error: This script is intended to run on Windows or Linux.")
        sys.exit(1)

    # Collect firewall logs using the appropriate method or command
    try:
        # Modify the command or method to collect firewall logs based on your firewall device
        firewall_command = config.get("FirewallLogs", "firewall_command")
        firewall_log_data = subprocess.check_output(firewall_command, shell=True)
        firewall_logs = firewall_log_data.decode("utf-8").splitlines()

        logs.extend(firewall_logs)
    except Exception as e:
        print(f"Error collecting firewall logs: {str(e)}")
        sys.exit(1)

    return logs

def save_logs_to_database(logs, db_config):
    try:
        # Connect to the database
        conn = pyodbc.connect(db_config)
        cursor = conn.cursor()

        # Insert each firewall log entry into the database
        for log in logs:
            cursor.execute("INSERT INTO FirewallLogTable (LogEntry) VALUES (?)", (log,))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving firewall logs to the database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Collect firewall logs
    firewall_logs = collect_firewall_logs(config)

    # Option 5: Send collected firewall logs to the database
    db_config = config.get("Database", "db_connection_string")
    if db_config:
        save_logs_to_database(firewall_logs, db_config)
        print("Collected firewall logs saved to the database.")

    # Option 6: Customize log collection or processing based on your needs
    # You can further process the collected logs here or send them to an API.
    # Example: for log in firewall_logs:
    #            process_log(log)
