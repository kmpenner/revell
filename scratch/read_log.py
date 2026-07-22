import json

log_path = "/Users/lamar/.gemini/antigravity-ide/brain/f75189a3-9b0c-446f-a82b-76c2732a4f3c/.system_generated/logs/transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            step = json.loads(line)
            # Print timestamp and request details
            if "content" in step and step["content"]:
                # Check if it has timestamps or dates from July 2nd
                print(f"Step {step.get('step_index')}: {step.get('source')} - {step.get('type')}")
                print(step["content"][:200])
                print("-" * 40)
        except Exception as e:
            pass
