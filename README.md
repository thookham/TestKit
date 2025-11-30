# TestKit - Hardware Profile Library for Windows Testing

**TestKit** is a comprehensive, industry-leading repository of hardware profiles specifically designed for testing and debugging Windows applications across diverse device configurations. With **12,254+ unique profiles** spanning Windows XP through Windows 11, TestKit provides standardized hardware definitions that can be exported to Docker, Vagrant, Terraform, and Windows Sandbox.

---

## 🎯 **Why TestKit?**

Modern software must work across an enormous range of hardware configurations. TestKit solves the "Standard Library of Hardware Definitions" problem by providing:

✅ **Pre-defined hardware profiles** - No more manual spec lookups  
✅ **Industry-leading coverage** - 34+ base hardware models × hundreds of configuration variants  
✅ **Multi-platform export** - Docker, Vagrant, Terraform, Windows Sandbox  
✅ **Global hardware representation** - American, European, and Chinese manufacturers  
✅ **Historical depth** - From Windows XP (Pentium 4) to Windows 11 (latest handhelds)

### Use Cases

- **QA Testing**: Validate software across realistic hardware constraints
- **DevOps**: Provision test environments matching real-world deployment targets  
- **Support Teams**: Reproduce customer issues on specific hardware configurations
- **Performance Testing**: Benchmark across different CPU/RAM/GPU combinations
- **Compatibility Testing**: Ensure legacy support (XP/7) and cutting-edge compatibility (Win 11)

---

## 📊 **Profile Coverage**

### Hardware Categories (34 Base Models)

| Category | Examples | Profiles Generated |
|----------|----------|-------------------|
| **Standard Laptops** | ThinkPad T420/T480, Dell XPS 13, HP EliteBook | 2,100+ |
| **Netbooks** | Asus Eee PC 1000HE | 80+ |
| **Tablets/2-in-1** | Surface Pro 3, Surface Pro X (ARM) | 450+ |
| **Gaming** | Alienware M17x, Razer Blade 15 | 600+ |
| **Workstations** | Dell Precision M4800 | 350+ |
| **Handhelds** | Steam Deck, ROG Ally, Legion Go, GPD Win | 1,800+ |
| **Mini PCs** | Intel NUC 11/12, Mac Mini | 1,200+ |
| **Rugged** | Panasonic Toughbook, Dell Latitude Rugged | 450+ |
| **Servers** | Dell PowerEdge R740, HP ProLiant DL380 | 850+ |
| **Cloud VMs** | AWS EC2 t2.micro, Azure Standard_D2s_v3 | 120+ |
| **Legacy** | Dell Dimension (XP), HP Compaq (Vista/7) | 300+ |
| **Chinese Mfrs** | Xiaomi, Huawei, GPD | 900+ |

### Operating System Coverage

- Windows XP (2001-2014)
- Windows 7 (2009-2020)
- Windows 8/8.1 (2012-2016)  
- Windows 10 (2015-2025)
- Windows 11 (2021+)
- Windows Server (2012 R2 - 2022)

---

## 🚀 **Quick Start**

### 1. Generate Profiles

```bash
cd TestKit
python scripts/generate_profiles.py
```

**Output**: `12,254 profiles` generated in `profiles/` directory, organized by OS version.

### 2. Export to Your Platform

#### Docker
```bash
python scripts/export.py \
  --profile "profiles/win10/lenovo-thinkpad-t480-windows-10-v1.json" \
  --format docker \
  --output exports
```

#### Vagrant (VirtualBox)
```bash
python scripts/export.py \
  --profile "profiles/win10/lenovo-thinkpad-t480-windows-10-v1.json" \
  --format vagrant \
  --output exports
```

#### Terraform (AWS)
```bash
python scripts/export.py \
  --profile "profiles/win10/lenovo-thinkpad-t480-windows-10-v1.json" \
  --format terraform \
  --output exports

# Deploy to AWS
cd exports
terraform init
terraform apply
```

#### Windows Sandbox
```bash
python scripts/export.py \
  --profile "profiles/win10/lenovo-thinkpad-t480-windows-10-v1.json" \
  --format wsb \
  --output exports

# Double-click the .wsb file to launch Windows Sandbox with the profile
```

---

## 📁 **Repository Structure**

```
TestKit/
├── profiles/              # Generated JSON profiles (12,254 files)
│   ├── win7/
│   ├── win8/
│   ├── win10/
│   ├── win11/
│   └── other/             # Server editions, XP, Vista
├── scripts/
│   ├── db/
│   │   └── laptops.json   # Hardware database (34 base models)
│   ├── generate_profiles.py  # Profile generator
│   ├── export.py          # Multi-platform exporter
│   └── validate_db.py     # Database validation utility
├── exports/               # Exported configurations
├── docs/
│   └── profile_schema.json  # JSON schema definition
├── README.md
└── CONTRIBUTING.md
```

---

## 🔧 **Profile Schema**

Each profile is a JSON file with the following structure:

```json
{
  "id": "lenovo-thinkpad-t480-windows-10-v1",
  "make": "Lenovo",
  "model": "ThinkPad T480",
  "year": 2018,
  "os": "windows-10",
  "form_factor": "Laptop",
  "hardware": {
    "cpu": "Intel Core i5-8250U",
    "cpu_count": 4,
    "ram_mb": 8192,
    "storage_gb": 256,
    "gpu": "Intel UHD Graphics 620",
    "gpu_vram_mb": 1024,
    "screen_resolution": "1920x1080"
  },
  "software": {
    "browser": "Chrome",
    "accessibility": "High Visibility"
  }
}
```

---

## 🌐 **Interoperability**

TestKit is designed to integrate seamlessly with existing testing infrastructure:

### Device Farms  
Export profiles to **Docker** and deploy to on-premise device labs or cloud platforms like AWS Device Farm.

###
 Virtualization  
Use **Vagrant** or **Terraform** exporters to provision VMs with infrastructure-as-code tools like Ansible,Puppet, or Chef.

### Local Testing  
Use **Windows Sandbox** (.wsb) files for lightweight, ephemeral testing environments on Windows 10 Pro/Enterprise.

### CI/CD Integration  
Profiles can be integrated into GitHub Actions, Azure DevOps, or Jenkins pipelines for automated cross-hardware testing.

---

## 📖 **Common Workflows**

### Testing Legacy Application on Windows 7
```bash
# Find a Windows 7 profile
ls profiles/win7/

# Export to Vagrant
python scripts/export.py \
  --profile "profiles/win7/hp-elitebook-840-g3-windows-7-v1.json" \
  --format vagrant \
  --output exports

# Launch VM
cd exports
vagrant up
```

### Reproducing ARM-based Surface Issue
```bash
# Export Surface Pro X (Qualcomm ARM)
python scripts/export.py \
  --profile "profiles/win10/microsoft-surface-pro-x-windows-10-v1.json" \
  --format wsb \
  --output exports

# Test in Windows Sandbox
./exports/microsoft-surface-pro-x-windows-10-v1.wsb
```

### Cloud Testing on AWS
```bash
# Export to Terraform
python scripts/export.py \
  --profile "profiles/win11/asus-rog-ally-windows-11-v1.json" \
  --format terraform \
  --output exports

# Deploy
cd exports
terraform apply
# Instance launched with tags matching TestKit profile
```

---

## 🛠️ **Development**

### Adding New Hardware

1. Edit `scripts/db/laptops.json`
2. Add new entry following the schema:

```json
{
  "make": "Framework",
  "model": "Laptop 13",
  "year": 2023,
  "form_factor": "Laptop",
  "supported_os": ["Windows 10", "Windows 11"],
  "cpu_options": [
    {"name": "Intel Core i7-1165G7", "cores": 4}
  ],
  "ram_options": [16384, 32768],
  "storage_options": [512, 1024],
  "gpu_options": [{"name": "Intel Iris Xe Graphics", "vram": 0}],
  "resolution_options": ["2256x1504"]
}
```

3. Regenerate profiles:
```bash
python scripts/generate_profiles.py
```

### Running Validation

```bash
python scripts/validate_db.py
```

---

## 📝 **Contributing**

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new hardware definitions
- Improving exporters
- Reporting issues
- Submitting pull requests

---

## 📜 **License**

This project is open-source and available under the MIT License.

---

## 🙋 **FAQ**

**Q: Why JSON profiles instead of directly provisioning VMs?**  
A: TestKit provides **definitions**, not **implementations**. This separation allows you to use the same profile across Docker, Vagrant, Terraform, or custom tooling.

**Q: Can I use TestKit for Linux/Mac testing?**  
A: TestKit focuses on Windows testing, but the profile format is extensible. You could adapt it for other platforms.

**Q: How accurate are the hardware profiles?**  
A: Profiles are based on manufacturer specifications. For exact hardware behavior, use real devices or manufacturer-provided VMs (e.g., Windows Dev VMs).

**Q: What's the difference between TestKit and BrowserStack?**  
A: BrowserStack is a cloud device farm offering real devices. TestKit provides **profile definitions** you can use to provision your own environments (cloud or on-premise).

---

## 🔗 **Related Projects**

- [Vagrant](https://www.vagrantup.com/) - Development environment provisioning  
- [Terraform](https://www.terraform.io/) - Infrastructure as Code  
- [Windows Sandbox](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview) - Lightweight desktop testing  
- [AWS Device Farm](https://aws.amazon.com/device-farm/) - Cloud-based device testing  

---

**Built with ❤️ for the Windows testing community**
