import json

try:
    with open('scripts/db/laptops.json', 'r') as f:
        data = json.load(f)
    
    print(f"Successfully loaded JSON. Found {len(data)} entries.")
    
    for i, laptop in enumerate(data):
        if 'resolution_options' not in laptop:
            print(f"Entry {i} ({laptop.get('make', 'Unknown')} {laptop.get('model', 'Unknown')}) is missing 'resolution_options'")
        if 'gpu_options' not in laptop:
             print(f"Entry {i} ({laptop.get('make', 'Unknown')} {laptop.get('model', 'Unknown')}) is missing 'gpu_options'")

except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
except Exception as e:
    print(f"Error: {e}")
