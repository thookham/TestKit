import argparse
import json
import os
import sys
from pathlib import Path

def load_profile(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def search_profiles(profiles_dir, query, field=None):
    matches = []
    print(f"Searching in {profiles_dir}...")
    
    count = 0
    for root, _, files in os.walk(profiles_dir):
        for file in files:
            if not file.endswith('.json'):
                continue
            
            count += 1
            if count % 1000 == 0:
                print(f"Scanned {count} profiles...", end='\r')

            file_path = os.path.join(root, file)
            
            # Optimization: Check filename first if field is not specified
            if not field and query.lower() in file.lower():
                matches.append(file_path)
                continue

            # Deep inspection
            profile = load_profile(file_path)
            if not profile:
                continue

            if field:
                val = str(profile.get(field, "")).lower()
                if query.lower() in val:
                    matches.append(file_path)
            else:
                # Search common fields
                search_text = f"{profile.get('make', '')} {profile.get('model', '')} {profile.get('os', '')} {profile.get('id', '')}".lower()
                if query.lower() in search_text:
                    matches.append(file_path)

    print(f"Scanned {count} profiles. Found {len(matches)} matches.")
    return matches

def main():
    parser = argparse.ArgumentParser(description="Search TestKit hardware profiles.")
    parser.add_argument("query", help="Search term (e.g., 'Dell', 'Windows 11')")
    parser.add_argument("--field", "-f", help="Specific field to search (e.g., 'make', 'model', 'os')")
    parser.add_argument("--dir", "-d", default="profiles", help="Profiles directory (default: profiles)")
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent / args.dir
    if not base_dir.exists():
        print(f"Error: Directory {base_dir} not found.")
        sys.exit(1)

    results = search_profiles(base_dir, args.query, args.field)
    
    print("\nResults:")
    for res in results[:20]:
        print(f" - {res}")
    
    if len(results) > 20:
        print(f"... and {len(results) - 20} more.")

if __name__ == "__main__":
    main()
