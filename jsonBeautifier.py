import json
import re
import sys
import pyperclip

def extract_log_parts(line):
    # Regex to parse log line format
    # Example: timestamp level service: message: {json}
    pattern = re.compile(
        r'^(?P<timestamp>\S+)\s+'             # timestamp
        r'(?P<level>\S+)\s+'                  # log level
        r'(?P<service>[^:]+):\s+'             # service name before colon
        r'(?P<message>.*?)'                   # message text (non-greedy)
        r'(?P<json_part>\{.*\})?$'            # optional JSON part at the end (greedy to end)
    )
    match = pattern.match(line)
    if not match:
        return None

    parts = match.groupdict()
    json_obj = None
    if parts['json_part']:
        try:
            json_obj = json.loads(parts['json_part'])
        except json.JSONDecodeError:
            # If JSON parse fails, treat as plain text
            json_obj = parts['json_part']

    return {
        "timestamp": parts['timestamp'],
        "level": parts['level'],
        "service": parts['service'].strip(),
        "message": parts['message'].strip(),
        "json": json_obj
    }

def main():
    # Read raw log text from clipboard (or use sys.stdin or a file)
    raw_text = pyperclip.paste()
    if not raw_text:
        print("❌ No data found in clipboard!")
        return

    lines = raw_text.strip().splitlines()
    parsed_logs = []
    for line in lines:
        parsed = extract_log_parts(line)
        if parsed:
            parsed_logs.append(parsed)
        else:
            # If line does not match, add raw line as fallback
            parsed_logs.append({"raw_line": line})

    # Print beautified JSON
    print(json.dumps(parsed_logs, indent=4))

if __name__ == "__main__":
    main()
