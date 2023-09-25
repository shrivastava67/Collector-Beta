import requests
import json
import logging
from cryptography.fernet import Fernet

def encrypt_payload(payload, encryption_key):
    f = Fernet(encryption_key)
    encrypted_payload = f.encrypt(json.dumps(payload).encode())
    return encrypted_payload

def send_logs_to_server(config, windows_logs, linux_logs, firewall_logs, switch_logs, mac_logs):
    api_url = config.get("API", "api_url")

    if not api_url:
        logging.error("API URL is not specified in the configuration.")
        return

    api_token = config.get("API", "api_token")
    encryption_key = config.get("API", "encryption_key")

    if not api_token or not encryption_key:
        logging.error("API token or encryption key is missing in the configuration.")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": api_token
    }

    # Prepare the payload
    payload = {
        "windows_logs": windows_logs,
        "linux_logs": linux_logs,
        "firewall_logs": firewall_logs,
        "switch_logs": switch_logs,
        "mac_logs": mac_logs
    }

    # Encrypt the payload
    encrypted_payload = encrypt_payload(payload, encryption_key)

    try:
        response = requests.post(api_url, headers=headers, data=encrypted_payload)

        if response.status_code == 200:
            logging.info("Logs sent successfully to the central server.")
        else:
            logging.error(f"Failed to send logs. Server returned status code {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending logs to the central server: {str(e)}")

# Example usage in main.py:
# send_logs_to_server(config, parsed_windows_logs, parsed_linux_logs, parsed_firewall_logs, parsed_switch_logs, parsed_mac_logs)
