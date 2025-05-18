import re
import json
import sys

LOG_LEVELS = ["ERROR", "WARN", "CRITICAL", "FATAL"]
ANOMALY_PATTERNS = [
    r'Exception', r'Traceback', r'failed', r'retry', r'denied', r'unexpected', r'timeout'
]

ERROR_CODE_PATTERNS = [
    r'error[_\-]?code[:= ]+(\w+)',
    r'code[:= ]+(\w+)',
    r'err[:= ]+(\w+)',
]

def is_anomalous(line, custom_keywords=[]):
    line_lower = line.lower()
    if any(re.search(pat, line_lower) for pat in ANOMALY_PATTERNS):
        return True
    if any(kw.lower() in line_lower for kw in custom_keywords):
        return True
    return False

def extract_json(line):
    try:
        json_part = re.search(r'({.*})', line)
        if json_part:
            return json.loads(json_part.group(1))
    except json.JSONDecodeError:
        return None
    return None

def extract_error_code(line, json_data=None):
    for pattern in ERROR_CODE_PATTERNS:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1)
    if json_data:
        for key in ['errorCode', 'error_code', 'code', 'err']:
            if key in json_data:
                return json_data[key]
    return None

def extract_timestamp(line):
    match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', line)
    return match.group(0) if match else "No Timestamp"

def extract_log_level(line):
    for level in LOG_LEVELS:
        if level in line:
            return level
    return "ANOMALY"

def parse_log_file(file_path, custom_keywords=[]):
    anomalies = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if any(level in line for level in LOG_LEVELS) or is_anomalous(line, custom_keywords):
                json_data = extract_json(line)
                error_code = extract_error_code(line, json_data)
                anomalies.append({
                    "timestamp": extract_timestamp(line),
                    "level": extract_log_level(line),
                    "message": line.strip(),
                    "json": json_data,
                    "error_code": error_code,
                })

    return anomalies

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Usage: python log_analyzer.py <logfile> [custom_keyword1 custom_keyword2 ...]")
        sys.exit(1)

    log_file = sys.argv[1]
    custom_keywords = sys.argv[2:]  # Extra args as keywords

    print(f"🔍 Scanning {log_file} for anomalies and keywords: {custom_keywords} ...")
    results = parse_log_file(log_file, custom_keywords)

    # Pretty-print JSON output to console
    print(json.dumps(results, indent=4, default=str))
