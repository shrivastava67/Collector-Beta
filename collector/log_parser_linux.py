import re
from datetime import datetime

def parse_linux_logs(logs):
    parsed_logs = []

    for log_entry in logs:
        # Example Linux log parsing - Modify as needed for your log format
        timestamp_match = re.search(r'(\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2})', log_entry)
        source_ip_match = re.search(r'Failed login attempt from (\S+)', log_entry)

        if timestamp_match and source_ip_match:
            timestamp_str = timestamp_match.group(1)
            source_ip = source_ip_match.group(1)
            # Detect timestamp format (e.g., Jan  1 01:23:45 or Jan  1 01:23:45.678)
            timestamp_format = '%b %d %H:%M:%S'
            if '.' in timestamp_str:
                timestamp_format += '.%f'
            timestamp = datetime.strptime(timestamp_str, timestamp_format)
            parsed_logs.append({
                'timestamp': timestamp,
                'source_ip': source_ip,
                'log_entry': log_entry
            })

    return parsed_logs
