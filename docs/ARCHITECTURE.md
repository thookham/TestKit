# TestKit Architecture

Technical deep-dive into TestKit's design, implementation, and extension points.

---

## 🏗️ **System Overview**

TestKit follows a three-stage pipeline architecture:

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Hardware DB   │─────▶│ Profile Generator│─────▶│   16,912 JSON   │
│  (laptops.json) │      │  (Python script)  │      │    Profiles     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        │                        │                          │
        │                        │                          │
        ▼                        ▼                          ▼
   45 hardware           Combinatorial          Organized by OS
    definitions           generation            version (win7/10/11)
```

---

## 📁 **Database Schema**

### Hardware Definition Structure

```json
{
  "make": "string",              // Manufacturer name
  "model": "string",             // Product model name
  "year": integer,               // Release year
  "form_factor": "enum",         // Device category
  "supported_os": ["string"],    // Compatible Windows versions
  "cpu_options": [               // Available CPU configurations
    {
      "name": "string",          // CPU model name
      "cores": integer           // Physical + logical cores
    }
  ],
  "ram_options": [integer],      // RAM sizes in MB
  "storage_options": [integer],  // Storage sizes in GB
  "gpu_options": [               // Available GPU configurations
    {
      "name": "string",          // GPU model name
      "vram": integer            // VRAM in MB (0 for integrated)
    }
  ],
  "resolution_options": ["string"] // Screen resolutions (WxH)
}
```

### Design Decisions

**Why separate `*_options` arrays?**
- Enables combinatorial profile generation
- Models real-world hardware configurability
- Allows accurate representation of manufacturer SKUs

**Why store everything in one JSON file?**
- Simple version control (single file diffs)
- Easy validation (one schema check)
- Efficient loading (single file read)
- As database grows, consider splitting by manufacturer

**Why MB/GB instead of bytes?**
- Matches manufacturer specifications
- Human-readable in source
- Sufficient precision for testing purposes

---

## 🔄 **Profile Generation Algorithm**

### Combinatorial Expansion

```python
for hardware in database:
    for os in hardware.supported_os:
        for cpu in hardware.cpu_options:
            for ram in hardware.ram_options:
                for storage in hardware.storage_options:
                    for gpu in hardware.gpu_options:
                        for resolution in hardware.resolution_options:
                            generate_profile(hardware, os, cpu, ram, storage, gpu, resolution)
```

**Complexity**: O(n × m × p × q × r × s × t) where:
- n = number of hardware definitions
- m = OS versions per hardware
- p = CPU options
- q = RAM options
- r = Storage options
- s = GPU options
- t = Resolution options

**Example**: ThinkPad T480
- 2 OS versions × 2 CPUs × 2 RAM × 2 storage × 2 GPUs × 2 resolutions = **64 profiles**

### Profile ID Generation

Pattern: `{make}-{model}-{os}-v{variant}`

```python
def generate_profile_id(make, model, os, variant_number):
    # Normalize to kebab-case
    make_slug = make.lower().replace(' ', '-')
    model_slug = model.lower().replace(' ', '-').replace('/', '-')
    os_slug = os.lower().replace(' ', '-')
    
    return f"{make_slug}-{model_slug}-{os_slug}-v{variant_number}"
```

**Example**: `lenovo-thinkpad-t480-windows-10-v23`

---

## 📤 **Export Architecture**

### Exporter Interface

All exporters implement a common interface:

```python
class Exporter:
    def __init__(self, profile, output_dir):
        self.profile = profile
        self.output_dir = output_dir
    
    def export(self):
        """Generate configuration files"""
        pass
    
    def validate(self):
        """Validate generated configuration"""
        pass
```

### Supported Formats

#### 1. Docker

**Output**: `Dockerfile`

**Mapping**:
```python
hardware.cpu_count → ENV TESTKIT_CPU_COUNT
hardware.ram_mb → ENV TESTKIT_RAM_MB
hardware.storage_gb → ENV TESTKIT_STORAGE_GB
hardware.gpu → ENV TESTKIT_GPU_NAME
metadata.os → FROM mcr.microsoft.com/windows/servercore:{os_version}
```

**Usage**: Testing in isolated containers

**Limitations**:
- Cannot directly emulate hardware (uses env vars)
- GUI applications require X11 forwarding or RDP
- Windows containers require Windows host

#### 2. Vagrant

**Output**: `Vagrantfile`

**Mapping**:
```ruby
config.vm.provider "virtualbox" do |vb|
  vb.cpus = hardware.cpu_count
  vb.memory = hardware.ram_mb
  vb.customize ["modifyvm", :id, "--vram", hardware.gpu_vram_mb]
end

config.vm.box = determine_vagrant_box(metadata.os)
```

**Usage**: Full OS virtualization for comprehensive testing

**Limitations**:
- Requires VirtualBox/VMware/Hyper-V
- Slower startup than containers
- Large disk footprint

#### 3. Terraform

**Output**: `main.tf`, `variables.tf`, `outputs.tf`

**Mapping**:
```hcl
resource "aws_instance" "testkit" {
  instance_type = determine_instance_type(hardware.cpu_count, hardware.ram_mb)
  
  tags = {
    TestKit_Profile = metadata.id
    TestKit_Make = metadata.make
    TestKit_Model = metadata.model
    TestKit_CPU = hardware.cpu
    TestKit_RAM_MB = hardware.ram_mb
  }
}
```

**Usage**: Cloud infrastructure provisioning

**Limitations**:
- Exact hardware matching not possible (uses closest instance type)
- Cost implications (cloud instances charge by time)
- Requires cloud credentials

#### 4. Windows Sandbox

**Output**: `.wsb` XML file

**Mapping**:
```xml
<Configuration>
  <vGPU>Enable/Disable based on gpu</vGPU>
  <MemoryInMB>{hardware.ram_mb}</MemoryInMB>
  <LogonCommand>
    <Command>cmd /c set TESTKIT_PROFILE={metadata.id}</Command>
  </LogonCommand>
</Configuration>
```

**Usage**: Quick, ephemeral testing on Windows 10/11 Pro

**Limitations**:
- Limited hardware control (GPU on/off, memory advisory only)
- Windows 10 Pro/Enterprise/Education only
- Cannot persist changes

---

## 🔌 **Extension Points**

### Adding a New Exporter

1. **Create exporter class** in `scripts/exporters/`

```python
# scripts/exporters/qemu_exporter.py
class QemuExporter(Exporter):
    def export(self):
        script = self.generate_qemu_script()
        with open(f"{self.output_dir}/start.sh", 'w') as f:
            f.write(script)
    
    def generate_qemu_script(self):
        return f"""#!/bin/bash
qemu-system-x86_64 \\
  -m {self.profile['hardware']['ram_mb']}M \\
  -smp {self.profile['hardware']['cpu_count']} \\
  -vga std \\
  -cdrom windows.iso
"""
```

2. **Register in export.py**

```python
EXPORTERS = {
    'docker': DockerExporter,
    'vagrant': VagrantExporter,
    'terraform': TerraformExporter,
    'wsb': WindowsSandboxExporter,
    'qemu': QemuExporter  # New exporter
}
```

3. **Add tests** for validation

### Adding New Hardware Fields

To add a new hardware property:

1. **Update database schema** in `scripts/db/laptops.json`
2. **Update validator** in `scripts/validate_db.py`
3. **Update generator** to include field in profiles
4. **Update exporters** to use new field (if applicable)
5. **Update documentation** with new field description

**Example**: Adding touchscreen support

```json
{
  "make": "Dell",
  "model": "XPS 13 2-in-1",
  "touchscreen": true,  // New field
  ...
}
```

---

## 🧪 **Validation Strategy**

### Database Validation

```python
def validate_database():
    # Schema validation
    validate_json_schema(laptops.json)
    
    # Business rules
    assert year >= 2000 and year <= current_year
    assert len(cpu_options) > 0
    assert all(ram > 0 for ram in ram_options)
    assert all(storage > 0 for storage in storage_options)
    
    # Uniqueness
    check_no_duplicate_models()
```

### Profile Validation

```python
def validate_profile(profile):
    # Required fields
    assert profile['id']
    assert profile['make']
    assert profile['model']
    
    # Reference integrity
    assert profile['os'] in profile['supported_os']
    assert profile['hardware']['cpu'] in cpu_options
```

---

## 📊 **Performance Characteristics**

### Generation Performance

**Current (45 models, 16,912 profiles)**:
- Generation time: ~15-30 seconds
- Memory usage: ~100 MB peak
- Disk usage: ~85 MB (compressed: ~12 MB)

**Scalability**:
- Linear with number of hardware definitions
- Exponential with option arrays (combinatorial explosion)
- File I/O is bottleneck (16k+ file writes)

**Optimization Opportunities**:
- Parallel profile writing
- In-memory generation with batch writes
- Profile deduplication
- Incremental generation (only changed hardware)

### Export Performance

**Docker**: <1 second per profile
**Vagrant**: <1 second per profile  
**Terraform**: <2 seconds per profile
**Windows Sandbox**: <1 second per profile

---

## 🔒 **Security Considerations**

### Data Sanitization
- No user credentials stored
- No network endpoints in configurations
- No executable code in profiles (pure data)

### Export Safety
- Terraform: Requires explicit user confirmation before `apply`
- Docker: Builds local images, no automatic push
- Vagrant: Local VMs only
- WSB: Sandboxed environment, no host access by default

### CI/CD Security
- Validation runs in isolated environment
- No secrets in repository
- GitHub Actions limited to read-only operations

---

## 🔮 **Future Architecture Considerations**

### Database Evolution
- **Split by manufacturer**: As we approach 100+ models
- **Separate OS mappings**: More granular OS version support
- **Hardware taxonomy**: Group by chipset architecture

### Generator Enhancements
- **Smart variant naming**: More descriptive variant IDs
- **Profile templates**: Pre-configured sets for common scenarios
- **Custom combinatorics**: User-defined generation rules

### Export Expansion
- **Ansible playbooks**: Configuration management integration
- **Cloud-init**: Cloud instance customization
- **Packer templates**: Custom image creation
- **GitHub Actions matrices**: Direct CI integration

---

**Architecture Version**: 1.1.0  
**Last Updated**: 2024-11-30
