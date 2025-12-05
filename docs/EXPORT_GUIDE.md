# TestKit Export Guide

TestKit can export hardware profiles into various formats for virtualization and simulation. This guide covers how to use the export tools and the specifics of each format.

## Tools

### 1. Single Profile Export (`export.py`)

Use `scripts/export.py` to export a single profile JSON file.

**Usage**:

```bash
python scripts/export.py --profile <path/to/profile.json> --format <format> [--output <dir>]
```

**Examples**:

```bash
# Export Steam Deck profile to Hyper-V
python scripts/export.py --profile profiles/win11/valve-steam-deck-oled-windows-11-v24.json --format hyperv

# Export ThinkPad profile to Docker
python scripts/export.py --profile profiles/win10/lenovo-thinkpad-t480.json --format docker
```

### 2. Batch Export (`batch_export.py`)

Use `scripts/batch_export.py` to filter and export multiple profiles at once.

**Usage**:

```bash
python scripts/batch_export.py --format <format> [--make <string>] [--os <string>] [--limit <int>] [--output <dir>]
```

**Examples**:

```bash
# Export all "Lenovo" profiles to VMware format
python scripts/batch_export.py --make Lenovo --format vmware --output exports/lenovo_vmware

# Export all "Windows 11" profiles to Docker
python scripts/batch_export.py --os "Windows 11" --format docker
```

---

## Supported Formats

### 🐳 Docker (`--format docker`)

Generates a `Dockerfile` derived from `mcr.microsoft.com/windows/servercore`.

- **Use Case**: CI/CD pipelines, containerized testing.
- **Output**: `.Dockerfile`, `launch.ps1`, `launch.sh`
- **Simulated Hardware**: Environment variables (`TESTKIT_RAM_MB`, etc.) are set in the container.

### 📦 Vagrant (`--format vagrant`)

Generates a `Vagrantfile` for VirtualBox.

- **Use Case**: Local full-VM testing with Vagrant workflows.
- **Output**: `.Vagrantfile`, launch scripts.
- **Requires**: Vagrant, VirtualBox.

### ☁️ Terraform (`--format terraform`)

Generates a `.tf` configuration for AWS EC2.

- **Use Case**: Cloud-based testing environments.
- **Output**: `.tf` file mapping RAM to AWS Instance Types (e.g., `t2.medium`).
- **Requires**: Terraform CLI, AWS Credentials.

### 🪟 Windows Sandbox (`--format wsb`)

Generates a `.wsb` configuration file.

- **Use Case**: Quick, disposable desktop testing on Windows Pro/Ent.
- **Output**: `.wsb` file.
- **Features**: Enables vGPU if the profile has VRAM.

### ⚡ Hyper-V (`--format hyperv`)

Generates a PowerShell script to create a VM in Hyper-V.

- **Use Case**: Professional local virtualization on Windows.
- **Output**: `_setup.ps1` script.
- **Features**:
  - Sets Generation 2 for modern OS profiles.
  - Enables TPM and Secure Boot (vital for Windows 11).
  - Configures RAM and CPU counts.

### 🖥️ VMware (`--format vmware`)

Generates a `.vmx` configuration file.

- **Use Case**: VMware Workstation Pro or Player.
- **Output**: `.vmx` file.
- **Features**: Standard hardware definition (vHW 16).

---

## Troubleshooting

- **"unhashable type: 'dict'" error**: Ensure you are using the latest version of the scripts. This was a known formatting bug fixed in v1.4.0.
- **Hyper-V script fails**: Ensure you run PowerShell as **Administrator** and have the Hyper-V Module installed.
