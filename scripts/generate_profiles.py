import json
import os
import itertools

from typing import List, Dict, Any

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'laptops.json')
PROFILES_DIR = os.path.join(os.path.dirname(__file__), '..', 'profiles')

def load_db() -> List[Dict[str, Any]]:
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def generate_slug(make: str, model: str, os_name: str, variant_id: int) -> str:
    # Create a clean slug: lenovo-thinkpad-t480-win10-v1
    slug = f"{make}-{model}-{os_name}-v{variant_id}".lower()
    return slug.replace(" ", "-").replace(".", "")

def get_os_dir(os_name: str) -> str:
    # Map OS name to directory
    mapping = {
        "Windows XP": "xp",
        "Windows 7": "win7",
        "Windows 8": "win8",
        "Windows 8.1": "win8", # Grouping 8/8.1 for now or create separate if needed
        "Windows 10": "win10",
        "Windows 11": "win11"
    }
    return mapping.get(os_name, "other")

def main():
    laptops = load_db()
    count = 0

    for laptop in laptops:
        # Generate permutations for this laptop model
        # Define environment permutations
        accessibility_options = ["Standard", "High Contrast"]
        browser_options = ["Chrome", "Firefox", "Edge"]
        if "Windows XP" in laptop['supported_os'] or "Windows 7" in laptop['supported_os']:
             browser_options.append("Internet Explorer")

        # We cartesian product all options
        options = [
            laptop['supported_os'],
            laptop['cpu_options'],
            laptop['ram_options'],
            laptop['storage_options'],
            laptop['gpu_options'],
            laptop['resolution_options'],
            accessibility_options,
            browser_options
        ]

        # itertools.product creates every combination
        for i, (os_target, cpu, ram, storage, gpu, resolution, access_mode, browser) in enumerate(itertools.product(*options)):
            
            # Create Profile Object
            profile_id = generate_slug(laptop['make'], laptop['model'], os_target, i+1)
            
            profile = {
                "id": profile_id,
                "metadata": {
                    "make": laptop['make'],
                    "model": laptop['model'],
                    "year": laptop['year'],
                    "os_target": os_target,
                    "form_factor": laptop['form_factor']
                },
                "hardware": {
                    "cpu_cores": cpu['cores'],
                    "cpu_name": cpu['name'],
                    "ram_mb": ram,
                    "storage_gb": storage,
                    "gpu_name": gpu['name'],
                    "gpu_vram_mb": gpu['vram'],
                    "screen_resolution": resolution
                },
                "environment": {
                    "accessibility_mode": access_mode,
                    "boot_mode": "Normal"
                },
                "software": {
                    "primary_browser": browser
                }
            }

            # Save to file
            os_dir = get_os_dir(os_target)
            target_dir = os.path.join(PROFILES_DIR, os_dir)
            ensure_dir(target_dir)
            
            filename = f"{profile_id}.json"
            filepath = os.path.join(target_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(profile, f, indent=2)
            
            count += 1
            print(f"Generated: {filename}")

    print(f"Total profiles generated: {count}")

if __name__ == "__main__":
    main()
