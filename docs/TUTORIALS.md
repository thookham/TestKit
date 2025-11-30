# TestKit Tutorials

Step-by-step guides for common TestKit scenarios.

---

## 📚 **Tutorial Overview**

| Tutorial | Difficulty | Time | Use Case |
|----------|-----------|------|----------|
| [1. Your First Test Environment](#tutorial-1-your-first-test-environment) | Beginner | 10 min | Getting started |
| [2. Reproducing a Customer Bug](#tutorial-2-reproducing-a-customer-bug-report) | Intermediate | 15 min | Support workflow |
| [3. CI/CD Integration](#tutorial-3-cicd-integration) | Advanced | 30 min | Automation |
| [4. Creating Custom Export Formats](#tutorial-4-creating-custom-export-formats) | Advanced | 45 min | Extension |
| [5. Contributing Hardware Profiles](#tutorial-5-contributing-hardware-profiles) | Beginner | 20 min | Community |

---

## Tutorial 1: Your First Test Environment

**Goal**: Generate profiles and deploy a test environment using Windows Sandbox.

**Prerequisites**: Windows 10/11 Pro/Enterprise, Python 3.7+

### Step 1: Clone and Setup

```bash
git clone https://github.com/thookham/TestKit.git
cd TestKit
```

### Step 2: Generate Profiles

```bash
python scripts/generate_profiles.py
```

**Output**: 16,912 profiles in `profiles/` directory

### Step 3: Browse Available Profiles

```bash
# List Windows 11 profiles
ls profiles/win11/

# Find a specific laptop
ls profiles/win11/ | grep "acer"
```

### Step 4: Export to Windows Sandbox

```bash
python scripts/export.py \
  --profile "profiles/win11/acer-aspire-vero-windows-11-v1.json" \
  --format wsb \
  --output exports
```

### Step 5: Launch Windows Sandbox

```bash
# Open the generated .wsb file
start exports/acer-aspire-vero-windows-11-v1.wsb
```

**Result**: Windows Sandbox launches with environment variables matching the Acer Aspire Vero profile.

### Step 6: Verify Profile in Sandbox

Inside the sandbox, open PowerShell:

```powershell
# Check environment variables
Get-ChildItem Env: | Where-Object {$_.Name -like "TESTKIT_*"}

# Should show:
# TESTKIT_PROFILE_ID=acer-aspire-vero-windows-11-v1
# TESTKIT_CPU=Intel Core i5-1155G7
# TESTKIT_RAM_MB=8192
# etc.
```

**✅ Success!** You've deployed your first TestKit test environment.

---

## Tutorial 2: Reproducing a Customer Bug Report

**Scenario**: Customer reports application crash on "MSI GS66 Stealth, Windows 11, 32GB RAM"

### Step 1: Find Matching Profile

```bash
# Search for MSI GS66 profiles
ls profiles/win11/ | grep "msi-gs66"

# View available variants
ls profiles/win11/msi-gs66-stealth-windows-11-*
```

### Step 2: Select Exact Configuration

```bash
# Find 32GB RAM variant
cat profiles/win11/msi-gs66-stealth-windows-11-v* | grep -l '"ram_mb": 32768'
```

**Result**: `msi-gs66-stealth-windows-11-v15.json`

### Step 3: Export toVagrant for Full OS Testing

```bash
python scripts/export.py \
  --profile "profiles/win11/msi-gs66-stealth-windows-11-v15.json" \
  --format vagrant \
  --output exports
```

### Step 4: Launch VM

```bash
cd exports
vagrant up
```

### Step 5: Install and Test Your Application

```bash
# SSH into VM
vagrant ssh

# Install your application
# Run reproduction steps
```

### Step 6: Debug

```bash
# Attach debugger, collect logs, etc.
# Profile ensures hardware specs match customer environment
```

**✅ Success!** You've reproduced the issue in an environment matching customer specs.

---

## Tutorial 3: CI/CD Integration

**Goal**: Integrate TestKit into GitHub Actions for automated cross-hardware testing.

### Step 1: Create GitHub Actions Workflow

`.github/workflows/test-cross-hardware.yml`:

```yaml
name: Cross-Hardware Testing

on: [push, pull_request]

jobs:
  test-matrix:
    runs-on: windows-latest
    strategy:
      matrix:
        profile:
          - profiles/win10/lenovo-thinkpad-t480-windows-10-v1.json
          - profiles/win11/acer-aspire-vero-windows-11-v1.json
          - profiles/win11/msi-gs66-stealth-windows-11-v5.json
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Export Profile
        run: |
          python scripts/export.py \
            --profile "${{ matrix.profile }}" \
            --format wsb \
            --output exports
      
      - name: Set Environment from Profile
        run: |
          $profile = Get-Content "${{ matrix.profile }}" | ConvertFrom-Json
          echo "TESTKIT_CPU=$($profile.hardware.cpu)" >> $env:GITHUB_ENV
          echo "TESTKIT_RAM_MB=$($profile.hardware.ram_mb)" >> $env:GITHUB_ENV
      
      - name: Run Tests
        run: |
          # Your test commands here
          pytest tests/ --hardware-profile="${{ matrix.profile }}"
```

### Step 2: Update Test Suite

Modify your tests to read TestKit environment variables:

```python
# tests/conftest.py
import os
import pytest

@pytest.fixture
def hardware_profile():
    return {
        'cpu': os.getenv('TESTKIT_CPU'),
        'ram_mb': int(os.getenv('TESTKIT_RAM_MB', 0)),
        'gpu': os.getenv('TESTKIT_GPU')
    }

# tests/test_performance.py
def test_memory_usage(hardware_profile):
    if hardware_profile['ram_mb'] < 8192:
        pytest.skip("Low memory configuration")
    
    # Run memory-intensive test
    assert check_memory_usage() < hardware_profile['ram_mb']
```

### Step 3: Push and Verify

```bash
git add .github/workflows/test-cross-hardware.yml
git commit -m "Add cross-hardware CI testing"
git push
```

**✅ Success!** Your tests now run across multiple hardware profiles automatically.

---

## Tutorial 4: Creating Custom Export Formats

**Goal**: Add a QEMU exporter for Linux-based testing.

### Step 1: Create Exporter Class

`scripts/exporters/qemu_exporter.py`:

```python
import os
from .base_exporter import Exporter

class QemuExporter(Exporter):
    def export(self):
        """Generate QEMU launch script"""
        script_path = os.path.join(self.output_dir, 'start-qemu.sh')
        
        with open(script_path, 'w') as f:
            f.write(self.generate_qemu_script())
        
        os.chmod(script_path, 0o755)
        print(f"Generated QEMU script: {script_path}")
    
    def generate_qemu_script(self):
        hw = self.profile['hardware']
        
        return f"""#!/bin/bash
# TestKit QEMU Launch Script
# Profile: {self.profile['id']}

qemu-system-x86_64 \\
  -name "TestKit - {self.profile['make']} {self.profile['model']}" \\
  -m {hw['ram_mb']}M \\
  -smp cores={hw['cpu_count']} \\
  -vga std \\
  -cdrom windows-{self.profile['os']}.iso \\
  -drive file=testkit-{self.profile['id']}.qcow2,format=qcow2,size={hw['storage_gb']}G \\
  -netdev user,id=net0 \\
  -device e1000,netdev=net0

echo "Profile: {self.profile['id']}"
echo "CPU: {hw['cpu']}"
echo "RAM: {hw['ram_mb']} MB"
echo "Storage: {hw['storage_gb']} GB"
"""
```

### Step 2: Register Exporter

`scripts/export.py`:

```python
from exporters.qemu_exporter import QemuExporter

EXPORTERS = {
    'docker': DockerExporter,
    'vagrant': VagrantExporter,
    'terraform': TerraformExporter,
    'wsb': WindowsSandboxExporter,
    'qemu': QemuExporter  # Add new exporter
}
```

### Step 3: Test Your Exporter

```bash
python scripts/export.py \
  --profile "profiles/win11/acer-aspire-vero-windows-11-v1.json" \
  --format qemu \
  --output exports

# Verify generated script
cat exports/start-qemu.sh
```

### Step 4: Run with QEMU

```bash
cd exports
./start-qemu.sh
```

**✅ Success!** You've created a custom TestKit exporter.

---

## Tutorial 5: Contributing Hardware Profiles

**Goal**: Add the Framework Laptop 13 to TestKit.

### Step 1: Research Specifications

Visit [Framework Official Specs](https://frame.work/) and collect:
- CPU options
- RAM configurations
- Storage options
- Display resolution
- Supported Windows versions

### Step 2: Add to Database

Edit `scripts/db/laptops.json`:

```json
{
  "make": "Framework",
  "model": "Laptop 13",
  "year": 2023,
  "form_factor": "Laptop",
  "supported_os": ["Windows 10", "Windows 11"],
  "cpu_options": [
    {"name": "Intel Core i5-1340P", "cores": 12},
    {"name": "Intel Core i7-1370P", "cores": 14}
  ],
  "ram_options": [16384, 32768],
  "storage_options": [512, 1024, 2048],
  "gpu_options": [
    {"name": "Intel Iris Xe Graphics", "vram": 0}
  ],
  "resolution_options": ["2256x1504"]
}
```

### Step 3: Validate

```bash
python scripts/validate_db.py
# Output: Successfully loaded JSON. Found 46 entries.
```

### Step 4: Generate Profiles

```bash
python scripts/generate_profiles.py
```

### Step 5: Verify Generated Profiles

```bash
ls profiles/*/framework-laptop-13-*
# Should see 48 profiles (2 CPUs × 3 RAM × 4 storage × 2 OS)
```

### Step 6: Submit Pull Request

```bash
git checkout -b add-framework-laptop-13
git add scripts/db/laptops.json
git commit -m "feat: Add Framework Laptop 13 (2023)"
git push origin add-framework-laptop-13
```

Open PR on GitHub with description:

```markdown
## Hardware Addition: Framework Laptop 13 (2023)

**Source**: https://frame.work/products/laptop-13-gen-intel

**Profiles Generated**: 48
- 2 CPU options × 3 RAM × 4 storage × 2 OS versions

**Notes**:
- Modular, user-repairable laptop
- All configurations use Intel Iris Xe integrated graphics
- 3:2 aspect ratio display (2256x1504)
```

**✅ Success!** You've contributed a new hardware profile to TestKit.

---

## 🆘 **Troubleshooting**

### Profile Not Found

**Problem**: `File not found: profiles/win11/xyz.json`

**Solution**:
```bash
# Regenerate profiles
python scripts/generate_profiles.py

# Verify file exists
ls profiles/win11/ | grep xyz
```

### Export Fails

**Problem**: Exporter throws an error

**Solution**:
```bash
# Validate profile JSON
python scripts/validate_db.py

# Check profile format
cat profiles/win11/your-profile.json | python -m json.tool
```

### Windows Sandbox Won't Launch

**Problem**: `.wsb` file doesn't open

**Solution**:
1. Verify Windows version (10 Pro/Enterprise/Education or 11)
2. Enable Windows Sandbox feature:
   ```powershell
   Enable-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM"
   ```
3. Restart computer

---

## 📚 **Next Steps**

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Explore [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for complete hardware catalog
- Check [API_REFERENCE.md](API_REFERENCE.md) for CLI options

**Happy Testing!**
