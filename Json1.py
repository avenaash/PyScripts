import json
import pyperclip

def beautify_json_from_clipboard():
    try:
        raw_data = pyperclip.paste()
        parsed_json = json.loads(raw_data)
        pretty_json = json.dumps(parsed_json, indent=4, sort_keys=True)
        print("\n✅ Beautified JSON from Clipboard:\n")
        print(pretty_json)
    except json.JSONDecodeError as e:
        print(f"\n❌ Invalid JSON in clipboard: {e}")
    except Exception as e:
        print(f"\n⚠️ Error occurred: {e}")

if __name__ == "__main__":
    beautify_json_from_clipboard()
