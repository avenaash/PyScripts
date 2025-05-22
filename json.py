import re
import json
import sys

def find_json_objects(text):
    """
    Extract JSON objects from a string.
    Handles edge cases where there might be multiple JSONs per line.
    """
    objects = []
    regex = r'({.*?})(?=\s|$)'  # Non-greedy JSON object match
    matches = re.finditer(regex, text)
    for match in matches:
        try:
            obj = json.loads(match.group(1))
            pretty = json.dumps(obj, indent=4)
            objects.append((match.group(1), pretty))
        except json.JSONDecodeError:
            continue
    return objects

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    print("\n🎯 Beautified Output:\n")

    for line in lines:
        found_jsons = find_json_objects(line)
        if found_jsons:
            for original, pretty in found_jsons:
                print("🔸 Raw Line:\n", line.strip())
                print("🔹 Beautified JSON:")
                print(pretty)
                print("-" * 60)
        else:
            print("📝 No JSON found in line:\n", line.strip())
            print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_formatter.py <path_to_log_file>")
    else:
        process_file(sys.argv[1])
