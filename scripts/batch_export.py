import os
import json
import argparse
import glob
from pathlib import Path
from typing import List, Dict, Any

# Import exporters from the existing script
try:
    from export import export_docker, export_vagrant, export_terraform, export_wsb, export_hyperv, export_vmware
except ImportError:
    # Handle case where script is run from root directory
    from scripts.export import export_docker, export_vagrant, export_terraform, export_wsb, export_hyperv, export_vmware


def find_profiles(root_dir: str = "profiles") -> List[str]:
    """Recursively finding all JSON profile files."""
    return glob.glob(os.path.join(root_dir, "**", "*.json"), recursive=True)

def filter_profiles(profile_paths: List[str], make_filter: str, os_filter: str) -> List[Dict[str, Any]]:
    """Loads and filters profiles based on criteria."""
    matches = []
    
    for path in profile_paths:
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            # Check Make Match
            make = data.get('metadata', {}).get('make', '') or data.get('make', '')
            if make_filter and make_filter.lower() not in make.lower():
                continue
                
            # Check OS Match
            os_target = data.get('metadata', {}).get('os_target', '') or data.get('os', '')
            if os_filter and os_filter.lower() not in os_target.lower():
                continue
            
            # Store path for logging references if needed, but return data object
            data['_source_path'] = path 
            matches.append(data)
            
        except Exception as e:
            # print(f"Warning: Could not load {path}: {e}")
            pass
            
    return matches

def main():
    parser = argparse.ArgumentParser(description="Batch export TestKit profiles.")
    parser.add_argument("--format", choices=["docker", "vagrant", "terraform", "wsb", "hyperv", "vmware"], required=True)
    parser.add_argument("--output", default="exports/batch", help="Output directory")
    parser.add_argument("--make", help="Filter by manufacturer (case-insensitive substring)")
    parser.add_argument("--os", help="Filter by OS name (case-insensitive substring)")
    parser.add_argument("--limit", type=int, help="Maximum number of profiles to export")
    
    args = parser.parse_args()
    
    # 1. Find all profiles
    print("Scanning for profiles...")
    all_files = find_profiles()
    print(f"Found {len(all_files)} profile files.")
    
    # 2. Filter
    print("Filtering...")
    matches = filter_profiles(all_files, args.make, args.os)
    print(f"Matched {len(matches)} profiles.")
    
    if args.limit and len(matches) > args.limit:
        print(f"Limiting export to {args.limit} profiles.")
        matches = matches[:args.limit]
        
    # 3. Export
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        
    print(f"Exporting {len(matches)} profiles to '{args.format}' format in '{args.output}'...")
    
    success_count = 0
    for profile in matches:
        try:
            if args.format == "docker":
                export_docker(profile, args.output)
            elif args.format == "vagrant":
                export_vagrant(profile, args.output)
            elif args.format == "terraform":
                export_terraform(profile, args.output)
            elif args.format == "wsb":
                export_wsb(profile, args.output)
            elif args.format == "hyperv":
                export_hyperv(profile, args.output)
            elif args.format == "vmware":
                export_vmware(profile, args.output)
            
            success_count += 1
        except Exception as e:
            print(f"Failed to export {profile.get('id')}: {e}")
            
    print(f"\nBatch Completed: {success_count}/{len(matches)} exported successfully.")

if __name__ == "__main__":
    main()
