# Contributing to TestKit

Thank you for your interest in contributing to TestKit! We aim to build the most comprehensive database of hardware profiles to help developers test Windows applications across the entire hardware spectrum.

---

## 📋 **Types of Contributions**

We welcome several types of contributions:

### 🖥️ Hardware Profiles
Adding new hardware definitions to expand TestKit's coverage

### 💻 Code Improvements
- Enhancing the profile generator
- Improving export formats
- Adding new export targets
- Optimizing performance

### 📖 Documentation
- Improving guides and tutorials
- Adding examples
- Fixing typos or clarifications
- Translating documentation

### 🐛 Bug Reports
Reporting inaccuracies in profiles or bugs in generator scripts

### 💡 Feature Requests
Suggesting new capabilities or improvements

---

## 🎯 **Adding New Hardware Profiles**

### Step 1: Research the Hardware

**Acceptable Sources:**
- Official manufacturer specifications
-  Tech review sites (AnandTech, NotebookCheck, LaptopMag)
- Retailer listings (with manufacturer part numbers)
- Service manuals

**Required Information:**
- Make and Model (exact marketing name)
- Year of release
- Form factor (Laptop, Desktop, Tablet, Handheld, Server, Cloud VM)
- Supported Windows versions
- All available CPU options with core counts
- RAM configuration options (in MB)
- Storage options (in GB)
- GPU options with VRAM (in MB, 0 for integrated)
- Screen resolution options

### Step 2: Check for Duplicates

```bash
# Search existing database
grep -i "model_name" scripts/db/laptops.json

# Browse generated profiles
ls profiles/*/
```

### Step 3: Add to Database

Edit `scripts/db/laptops.json` and add your entry following this template:

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
  "ram_options": [16384, 32768, 64512],
  "storage_options": [256, 512, 1024, 2048],
  "gpu_options": [
    {"name": "Intel Iris Xe Graphics", "vram": 0}
  ],
  "resolution_options": ["2256x1504"]
}
```

**Field Guidelines:**

| Field | Format | Notes |
|-------|--------|-------|
| `make` | String | Official manufacturer name (e.g., "Lenovo" not "lenovo") |
| `model` | String | Marketing name without make (e.g., "ThinkPad T480" not "Lenovo ThinkPad T480") |
| `year` | Integer | Year of initial release |
| `form_factor` | String | One of: Laptop, Desktop, Tablet, 2-in-1, Handheld, Server, Cloud VM, Mini PC, Rugged |
| `supported_os` | Array | Windows versions this hardware officially supports |
| `cpu_options` | Array of Objects | All CPU configurations offered |
| `ram_options` | Array of Integers | RAM sizes in MB (e.g., 8192 for 8GB) |
| `storage_options` | Array of Integers | Storage sizes in GB |
| `gpu_options` | Array of Objects | All GPU configurations (use `vram: 0` for integrated graphics) |
| `resolution_options` | Array of Strings | Screen resolutions in "WxH" format (e.g., "1920x1080") |

### Step 4: Validate Your Changes

```bash
# Run validation
python scripts/validate_db.py

# Test profile generation
python scripts/generate_profiles.py

# Verify your profiles were created
ls profiles/*/your-make-your-model-*.json
```

### Step 5: Submit a Pull Request

1. Fork the repository
2. Create a feature branch (`git checkout -b add-framework-laptop-13`)
3. Commit your changes (`git commit -m "feat: Add Framework Laptop 13 (2023)"`)
4. Push to your fork (`git push origin add-framework-laptop-13`)
5. Open a Pull Request with:
   - Clear title: "Add [Make] [Model] ([Year])"
   - Description including:
     - Source of specifications
     - Number of profiles generated
     - Any special notes

**Example PR Description:**
```markdown
## Hardware Addition: Framework Laptop 13 (2023)

**Source**: [Framework Official Specs](https://frame.work/products/laptop)

**Profiles Generated**: 48
- 2 CPU options × 3 RAM options × 4 storage options × 2 OS versions

**Notes**:
- Modular design allows extensive customization
- Uses Intel 13th gen P-series processors
- All configurations use integrated graphics
```

---

## 🔍 **Profile Quality Standards**

To maintain TestKit's reputation for accuracy:

### ✅ Do:
- Use official manufacturer specifications
- Include all major configuration variants
- Verify CPU core counts from official sources
- Double-check VRAM for dedicated GPUs
- List all officially supported Windows versions

### ❌ Don't:
- Guess specifications
- Include prototype or unreleased hardware
- Add custom/modified configurations
- Use rounded or approximated values
- Include Linux-specific configurations

### 🔶 Edge Cases:
- **Multiple display options**: List all available resolutions
- **Configurable hardware**: Include all documented factory configurations
- **Regional variants**: Add separate entries if specifications differ significantly
- **Refresh/revision models**: Use year to differentiate (e.g., "ThinkPad T480 (2018)")

---

## 💻 **Code Contributions**

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/TestKit.git
cd TestKit

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if any added in future)
pip install -r requirements.txt
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Testing Your Changes
```bash
# Validate database integrity
python scripts/validate_db.py

# Test profile generation
python scripts/generate_profiles.py

# Test all export formats
python scripts/export.py --profile profiles/win11/test-profile.json --format docker
python scripts/export.py --profile profiles/win11/test-profile.json --format vagrant
python scripts/export.py --profile profiles/win11/test-profile.json --format terraform
python scripts/export.py --profile profiles/win11/test-profile.json --format wsb
```

---

## 📝 **Documentation Contributions**

### Improving Existing Docs
- Fix typos, grammar, or formatting issues
- Add clarifying examples
- Update outdated information
- Improve navigation or organization

### Adding New Content
- Create tutorials for common scenarios
- Document advanced use cases
- Add troubleshooting guides
- Create video walkthroughs (link in docs)

### Documentation Standards
- Use clear, concise language
- Include code examples where relevant
- Add screenshots or diagrams for visual clarity
- Link to related documentation sections
- Test all code examples before submitting

---

## 🐛 **Reporting Issues**

### Before Reporting
1. Search existing issues to avoid duplicates
2. Verify the issue with the latest version
3. Collect relevant information (OS, Python version, error messages)

### Good Bug Reports Include:
- **Clear title**: "Profile generator fails on hardware with..."
- **Environment**: OS, Python version, TestKit version
- **Steps to reproduce**: Exact commands or actions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error text or screenshots
- **Relevant files**: Hardware database entry if applicable

**Use the bug report template** when creating issues.

---

## 🏅 **Recognition**

Contributors who add hardware profiles will be:
- Listed in the profile's metadata (if desired)
- Mentioned in release notes
- Added to the [Contributors](https://github.com/thookham/TestKit/graphs/contributors) page

**Hall of Fame** (coming soon): Top contributors featured in documentation.

---

## 🔄 **Review Process**

### What Maintainers Look For:
1. **Accuracy**: Specifications match official sources
2. **Completeness**: All required fields present
3. **Format**: Follows JSON schema and style guide
4. **Testing**: Profiles generate successfully
5. **Documentation**: PR description is clear and complete

### Typical Timeline:
- Initial review: 1-3 days
- Feedback/iteration: As needed
- Merge: After approval and passing CI checks

### Getting Faster Reviews:
- Follow all guidelines above
- Include source links in PR description
- Respond promptly to feedback
- Keep PRs focused (one hardware model per PR preferred)

---

## 🤝 **Code of Conduct**

Please be respectful and constructive in all interactions. See our [Code of Conduct](CODE_OF_CONDUCT.md) for details.

---

## 📞 **Getting Help**

- **Questions**: Open a [Discussion](https://github.com/thookham/TestKit/discussions)
- **Issues**: Use [GitHub Issues](https://github.com/thookham/TestKit/issues)
- **Security**: See [SECURITY.md](SECURITY.md)

---

## 🚀 **Priority Contributions**

Help us expand coverage in these areas:

### High Priority:
- **ARM-based Windows devices** (Qualcomm Snapdragon laptops)
- **Foldable/Dual-screen devices** (Surface Duo, ThinkPad X1 Fold)
- **Recent gaming handhelds** (2023-2024 models)
- **Workstation laptops** (Professional creator systems)

### Medium Priority:
- **Budget laptops** ($300-600 range)
- **International manufacturers** (Asian, European brands)
- **Small form factor desktops** (NUC-style systems)

### Nice to Have:
- **Historical systems** (2000-2010 era)
- **Niche form factors** (Rugged, industrial)
- **Server configurations** (Rack-mount, blade)

---

**Thank you for contributing to TestKit! Together we're building the most comprehensive Windows hardware testing resource available.**
