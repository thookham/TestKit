# TestKit API Reference

Complete CLI and schema documentation for TestKit scripts.

---

## 📜 **Scripts Overview**

| Script | Purpose | Complexity |
|--------|---------|------------|
| [`generate_profiles.py`](#generate_profilespy) | Generate hardware profiles | Simple |
| [`export.py`](#exportpy) | Export profiles to various formats | Moderate |
| [`batch_export.py`](#batch_exportpy) | Batch export multiple profiles | Moderate |
| [`validate_db.py`](#validate_dbpy) | Validate hardware database | Simple |

---

## `generate_profiles.py`

Generate complete set of hardware profiles from the database.

### Synopsis

```bash
python scripts/generate_profiles.py [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--help` | Show help message | - |
| *(No options currently)* | Generates all profiles | - |

### Output

Generates 16,912+ JSON profile files in `profiles/` directory, organized by OS:

- `profiles/win7/` - Windows 7 profiles
- `profiles/win8/` - Windows 8/8.1 profiles
- `profiles/win10/` - Windows 10 profiles
- `profiles/win11/` - Windows 11 profiles
- `profiles/other/` - XP, Vista, Server editions

---

## `export.py`

Export hardware profile to specific format (Docker, Vagrant, Terraform, Windows Sandbox, Hyper-V, VMware).

### Synopsis

```bash
python scripts/export.py --profile PROFILE --format FORMAT --output OUTPUT
```

### Generated Launch Scripts 🆕

For every export, `export.py` now generates helper scripts to immediately launch the environment:

- `launch.ps1` (PowerShell)
- `launch.sh` (Bash)

**Usage:**

```bash
./exports/launch.ps1
```

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--profile` | Path to profile JSON file | `profiles/win11/acer-aspire-vero-windows-11-v1.json` |
| `--format` | Export format | `docker`, `vagrant`, `terraform`, `wsb`, `hyperv`, `vmware` |
| `--output` | Output directory | `exports` |

### Export Formats

#### `docker` - Docker Container

**Generated Files**:

- `Dockerfile`

**Environment Variables Set**:

```
TESTKIT_PROFILE_ID
TESTKIT_MAKE
TESTKIT_MODEL
TESTKIT_YEAR
TESTKIT_OS
TESTKIT_CPU
TESTKIT_CPU_COUNT
TESTKIT_RAM_MB
TESTKIT_STORAGE_GB
TESTKIT_GPU
TESTKIT_GPU_VRAM_MB
TESTKIT_SCREEN_RESOLUTION
TESTKIT_BROWSER
TESTKIT_ACCESSIBILITY
```

**Usage**:

```bash
cd exports
docker build -t testkit-profile .
docker run -it testkit-profile
```

#### `vagrant` - Vagrant VM

**Generated Files**:

- `Vagrantfile`

**Configured Properties**:

- CPU cores
- RAM size (MB)
- VRAM size (MB)
- Base box (OS-dependent)

**Usage**:

```bash
cd exports
vagrant up
vagrant ssh
```

#### `terraform` - Terraform (AWS)

**Generated Files**:

- `.tf` configuration targeting AWS EC2
- Instance type auto-selection (e.g., `t2.medium`)

**Usage**:

```bash
cd exports
terraform init
terraform apply
```

#### `wsb` - Windows Sandbox

**Generated Files**:

- `{profile-id}.wsb` XML configuration

**Configured Properties**:

- vGPU (Enable/Disable)
- Memory
- Logon command

**Usage**:

```powershell
start exports/profile-name.wsb
```

#### `hyperv` - Hyper-V (PowerShell)

**Generated Files**:

- `{profile-id}_setup.ps1`

**Features**:

- Creates Generation 2 VM
- Enables TPM/Secure Boot for Windows 11
- Configures RAM and Processor Count

**Usage**:

```powershell
./exports/launch.ps1
# or output_setup.ps1 directly
```

#### `vmware` - VMware Workstation

**Generated Files**:

- `{profile-id}.vmx`

**Features**:

- Standard vHW 16 configuration
- Sound and Network enabled

**Usage**:

```bash
./exports/launch.ps1
# or "vmrun start <file.vmx>"
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Profile file not found |
| 2 | Invalid format specified |
| 3 | Output directory creation failed |

---

## `batch_export.py`

Export multiple profiles at once based on criteria.

### Synopsis

```bash
python scripts/batch_export.py --format FORMAT [--make MAKE] [--os OS] [--limit N]
```

### Options

| Option | Description | Required | Example |
|--------|-------------|----------|---------|
| `--format` | Target format | Yes | `docker`, `hyperv` |
| `--make` | Filter by manufacturer substring | No | `Lenovo` |
| `--os` | Filter by OS substring | No | `Windows 11` |
| `--limit` | Max profiles to export | No | `100` |
| `--output` | Output directory | No | `exports/batch` |

### Example

```bash
python scripts/batch_export.py --make Valve --format hyperv --limit 5
```

---

## `validate_db.py`

Validate hardware database JSON structure and content.

### Synopsis

```bash
python scripts/validate_db.py
```

### Validation Checks

✅ **JSON Syntax**: Valid JSON structure  
✅ **Required Fields**: All mandatory fields present  
✅ **Data Types**: Correct types (string, int, array)  
✅ **Value Ranges**: Realistic values (year, RAM, storage)  
✅ **Enum Values**: Form factors and OS names valid  
✅ **No Duplicates**: Unique make/model combinations

### Example

```bash
python scripts/validate_db.py

# Success output:
# Successfully loaded JSON. Found 45 entries.

# Failure output:
# JSON Decode Error: Expecting ',' delimiter: line 42 column 5 (char 1234)
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation successful |
| 1 | JSON syntax error or validation failure |

---

## 📋 **Profile JSON Schema**

### Complete Schema

```json
{
  "id": "string",                    // Unique profile identifier (kebab-case)
  "make": "string",                  // Manufacturer name
  "model": "string",                 // Model name
  "year": integer,                   // Release year (2000-2024)
  "os": "string",                    // Operating system
  "form_factor": "enum",             // Device category
  "hardware": {
    "cpu": "string",                 // CPU model name
    "cpu_count": integer,            // Number of cores
    "ram_mb": integer,               // RAM in megabytes
    "storage_gb": integer,           // Storage in gigabytes
    "gpu": "string",                 // GPU model name
    "gpu_vram_mb": integer,          // GPU VRAM in MB (0 for integrated)
    "screen_resolution": "string"    // Resolution (WxH format)
  },
  "software": {
    "browser": "enum",               // Default browser
    "accessibility": "enum"          // Accessibility setting
  }
}
```

### Field Specifications

#### `id`

- **Type**: string
- **Format**: `{make}-{model}-{os}-v{number}`
- **Example**: `acer-aspire-vero-windows-11-v1`

#### `make`

- **Type**: string
- **Examples**: `Lenovo`, `Dell`, `HP`, `Acer`, `MSI`

#### `model`

- **Type**: string
- **Examples**: `ThinkPad T480`, `XPS 13`, `Aspire Vero`

#### `year`

- **Type**: integer
- **Range**: 2000-2024
- **Example**: `2021`

#### `os`

- **Type**: string (enum)
- **Valid Values**:
  - `windows-xp`
  - `windows-vista`
  - `windows-7`
  - `windows-8`
  - `windows-8.1`
  - `windows-10`
  - `windows-11`
  - `windows-server-2012-r2`
  - `windows-server-2016`
  - `windows-server-2019`
  - `windows-server-2022`

#### `form_factor`

- **Type**: string (enum)
- **Valid Values**:
  - `Laptop`
  - `Desktop`
  - `Tablet`
  - `2-in-1`
  - `Handheld`
  - `Server`
  - `Cloud VM`
  - `Mini PC`
  - `Rugged`
  - `Netbook`

#### `hardware.cpu`

- **Type**: string
- **Examples**: `Intel Core i7-1165G7`, `AMD Ryzen 5 5500U`

#### `hardware.cpu_count`

- **Type**: integer
- **Range**: 1-128
- **Note**: Includes all cores (P-cores + E-cores for hybrid architectures)

#### `hardware.ram_mb`

- **Type**: integer
- **Common Values**: `4096`, `8192`, `16384`, `32768`, `65536`
- **Range**: 512-131072

#### `hardware.storage_gb`

- **Type**: integer
- **Common Values**: `256`, `512`, `1024`, `2048`
- **Range**: 30-4096

#### `hardware.gpu`

- **Type**: string
- **Examples**: `Intel Iris Xe Graphics`, `NVIDIA GeForce RTX 3070`

#### `hardware.gpu_vram_mb`

- **Type**: integer
- **Range**: 0-24576
- **Note**: Use `0` for integrated graphics

#### `hardware.screen_resolution`

- **Type**: string
- **Format**: `{width}x{height}`
- **Examples**: `1920x1080`, `2560x1440`, `3840x2160`

#### `software.browser`

- **Type**: string (enum)
- **Valid Values**: `Edge`, `Chrome`, `Firefox`, `None`

#### `software.accessibility`

- **Type**: string (enum)
- **Valid Values**: `None`, `High Contrast`, `High Visibility`, `Screen Reader`

---

## 🔧 **Environment Variables**

### Export Scripts

TestKit exporters may use these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `TESTKIT_DB_PATH` | Override database path | `./custom/laptops.json` |
| `TESTKIT_OUTPUT_DIR` | Default output directory | `./my-exports` |

### Generated Environments

Profile exports set these environment variables in target environments:

| Variable | Source | Example Value |
|----------|--------|---------------|
| `TESTKIT_PROFILE_ID` | `id` | `acer-aspire-vero-windows-11-v1` |
| `TESTKIT_MAKE` | `make` | `Acer` |
| `TESTKIT_MODEL` | `model` | `Aspire Vero` |
| `TESTKIT_YEAR` | `year` | `2021` |
| `TESTKIT_OS` | `os` | `windows-11` |
| `TESTKIT_FORM_FACTOR` | `form_factor` | `Laptop` |
| `TESTKIT_CPU` | `hardware.cpu` | `Intel Core i5-1155G7` |
| `TESTKIT_CPU_COUNT` | `hardware.cpu_count` | `4` |
| `TESTKIT_RAM_MB` | `hardware.ram_mb` | `8192` |
| `TESTKIT_STORAGE_GB` | `hardware.storage_gb` | `256` |
| `TESTKIT_GPU` | `hardware.gpu` | `Intel Iris Xe Graphics` |
| `TESTKIT_GPU_VRAM_MB` | `hardware.gpu_vram_mb` | `0` |
| `TESTKIT_SCREEN_RESOLUTION` | `hardware.screen_resolution` | `1920x1080` |
| `TESTKIT_BROWSER` | `software.browser` | `Edge` |
| `TESTKIT_ACCESSIBILITY` | `software.accessibility` | `None` |

---

## 📊 **Database Schema** (`laptops.json`)

### Structure

```json
[
  {
    "make": "string",
    "model": "string", 
    "year": integer,
    "form_factor": "enum",
    "supported_os": ["string"],
    "cpu_options": [
      {
        "name": "string",
        "cores": integer
      }
    ],
    "ram_options": [integer],
    "storage_options": [integer],
    "gpu_options": [
      {
        "name": "string",
        "vram": integer
      }
    ],
    "resolution_options": ["string"]
  }
]
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed field guidelines.

---

## 🚨 **Common Error Messages**

### `FileNotFoundError: profiles/...json`

**Cause**: Profile hasn't been generated  
**Solution**: Run `python scripts/generate_profiles.py`

### `KeyError: 'hardware'`

**Cause**: Invalid profile JSON structure  
**Solution**: Validate profile against schema above

### `ValueError: Invalid format: xyz`

**Cause**: Unsupported export format  
**Solution**: Use `docker`, `vagrant`, `terraform`, or `wsb`

### `PermissionError: Cannot create directory`

**Cause**: Insufficient permissions for output directory  
**Solution**: Check directory permissions or use different output path

---

## 📚 **Related Documentation**

- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical deep-dive
- [TUTORIALS.md](TUTORIALS.md) - Step-by-step guides
- [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) - Complete hardware catalog

---

**API Version**: 1.1.0  
**Last Updated**: 2024-11-30
