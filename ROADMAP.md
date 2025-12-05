# TestKit Roadmap

> **Last Updated**: December 1, 2024  
> **Current Version**: v1.3.0  
> **Status**: Active Development

---

## 📋 Executive Summary

TestKit has reached a strong foundation with 80 hardware models and 22,122 profiles across 4 export formats. This roadmap outlines strategic priorities for future development, organized into **Short-Term** (v1.4.0-v1.5.0), **Medium-Term** (v2.0.0), and **Long-Term** (v3.0.0+) milestones.

### Current State Assessment

**Strengths**:

- ✅ Comprehensive hardware coverage (Tier 1-3 manufacturers)
- ✅ Multi-platform export (Docker, Vagrant, Terraform, Windows Sandbox)
- ✅ Automated profile generation with strong validation
- ✅ Professional documentation and community standards
- ✅ CI/CD automation via GitHub Actions
- ✅ **Docker CLI Support**: Containerized runtime for profile generation

**Gaps & Opportunities**:

- 🔶 Limited **actual virtualization** - profiles are currently metadata definitions
- 🔶 No **automated testing** or **validation** of exported environments
- 🔶 Export formats are basic templates without advanced orchestration
- 🔶 No **web UI** or **interactive tooling** for profile browsing/selection
- 🔶 Limited **real-world integration** examples with CI/CD pipelines
- 🔶 No **performance benchmarking** or **profile comparison** tools

---

## 🎯 Short-Term Goals (v1.4.0 - v1.5.0)

### v1.4.0: Tier 4 Hardware & Export Enhancements

**Target Date**: January 2025

#### Hardware Database Expansion

- [ ] **Tier 4A: Emerging Form Factors** (10 models)
  - Foldable laptops (Asus Zenbook 17 Fold, Lenovo ThinkPad X1 Fold)
  - Dual-screen devices (Asus Zenbook Duo, Lenovo Yoga Book 9i)
  - E-ink laptops (Onyx Boox Tab Ultra C Pro)
  - Chromebooks running Windows (via dual-boot or Wine)

- [ ] **Tier 4B: Regional Manufacturers - Asia** (10 models)
  - Japanese: NEC Lavie, Panasonic Let's Note, Sharp Mebius
  - Korean: LG Gram variants, Samsung Notebook Flash
  - Chinese: Hasee, Mechrevo, Maibenben
  - Indian: iBall CompBook, Notion Ink Cain

- [ ] **Tier 4C: Vintage/Collector Systems** (5 models)
  - Windows 95/98 era (IBM ThinkPad 600, Compaq Armada)
  - Windows ME/2000 era (Sony Vaio PCG-SR, Toshiba Libretto)
  - Historical curiosities (HP Jornada, Compaq iPAQ)

**Expected Outcome**: **105 total hardware models**, **~28,000 profiles**

#### Export Improvements

- [ ] **Hyper-V Export Format** (.vhdx)
  - PowerShell scripts for Hyper-V VM creation
  - Integration with Windows Server environments
  - Support for Generation 1 and Generation 2 VMs

- [ ] **VMware Export Format** (.ovf/.ova)
  - VMware Workstation/ESXi compatibility
  - Template generation for vSphere environments

- [ ] **Batch Export Tool**
  - CLI: `python scripts/export_batch.py --format docker --filter "os=Windows 11"`
  - Parallel processing for multiple profiles
  - Progress reporting and error handling

- [ ] **Enhanced Launch Scripts**
  - Pre-flight checks (Docker installed, Vagrant plugins, AWS credentials)
  - Error handling with user-friendly messages
  - Auto-cleanup options for temporary resources

- [x] **Documentation**
  - [x] **EXPORT_GUIDE.md** - Deep-dive into each export format with best practices
  - [x] **HARDWARE_TIERS.md** - Explanation of Tier 1-4 classification
  - [ ] **TROUBLESHOOTING.md** - Common issues and solutions

---

### v1.5.0: Validation & CI/CD Integration

**Target Date**: March 2025

#### Profile Validation Suite

- [ ] **Smoke Testing Framework**
  - Automated tests for each export format
  - Verify Dockerfile builds successfully
  - Validate Vagrant box downloads and provisions
  - Test Terraform plan execution (dry-run)
  - Confirm Windows Sandbox .wsb file syntax

- [ ] **JSON Schema Enforcement**
  - Strict validation against `profiles/schema.json`
  - Pre-commit hooks to reject invalid profiles
  - CI pipeline fails on schema violations

- [ ] **Database Integrity Checks**
  - Detect duplicate hardware models
  - Flag unrealistic spec combinations (e.g., 64GB RAM on 2005 laptop)
  - Validate OS compatibility (e.g., no Windows 11 on 2010 hardware)

#### CI/CD Pipeline Examples

- [ ] **GitHub Actions Templates**
  - `.github/workflows/testkit-docker.yml` - Matrix build across profiles
  - `.github/workflows/testkit-terraform.yml` - Cloud deployment example
  - `.github/workflows/testkit-validation.yml` - Nightly profile smoke tests

- [ ] **Azure DevOps Pipelines**
  - Multi-stage pipeline with profile generation → export → test
  - Artifact storage for generated profiles
  - Integration with Azure Test Plans

- [ ] **GitLab CI Example**
  - Docker-in-Docker build for TestKit profiles
  - Terraform apply/destroy lifecycle in merge requests

#### Advanced Filtering

- [ ] **Profile Search Tool**
  - CLI: `python scripts/search.py --os "Windows 10" --min-ram 8192 --gpu-vendor NVIDIA`
  - JSON export of matching profiles
  - Interactive TUI (Text User Interface) mode

- [ ] **Recommendation Engine**
  - Input: "I need a profile for testing DirectX 12 games on Windows 11"
  - Output: Ranked list of suitable profiles with justifications

---

## 🚀 Medium-Term Goals (v2.0.0)

**Target Date**: Q3 2025

### Major Features

#### 1. **TestKit Web UI** (Dashboard)

A browser-based interface for exploring, comparing, and exporting profiles.

**Features**:

- [ ] **Profile Browser**
  - Searchable/filterable table of all 22k+ profiles
  - Quick preview cards with hardware specs
  - Download individual profiles or bulk export

- [ ] **Hardware Catalog**
  - Visual grid of all 80+ base hardware models
  - Manufacturer logos and device images
  - Filter by form factor, year, OS support

- [ ] **Comparison Tool**
  - Side-by-side comparison of up to 5 profiles
  - Highlight differences in CPU, RAM, GPU, etc.
  - Export comparison as PDF or CSV

- [ ] **Export Wizard**
  - Guided workflow: Select profile → Choose format → Configure options → Download
  - Real-time validation of export settings
  - Copy-paste ready launch commands

**Tech Stack**: React/Next.js frontend, Python FastAPI backend, profiles served as static JSON

#### 2. **Virtualization Testing Harness**

Move beyond metadata definitions to **actual VM provisioning and testing**.

- [ ] **Automated Environment Spin-Up**
  - GitHub Action triggers TestKit export for a profile
  - Provisions VM in cloud (AWS/Azure via Terraform)
  - Runs basic smoke tests (Windows boots, env vars set)
  - Tears down VM and reports results

- [ ] **Integration Tests**
  - Deploy a simple .NET/Electron app to TestKit VM
  - Verify app runs correctly on target hardware profile
  - Capture screenshots/logs for debugging

- [ ] **Performance Benchmarking**
  - Run standardized benchmarks (Geekbench, 3DMark) on provisioned VMs
  - Store historical results in `benchmarks/` directory
  - Compare actual performance vs. expected specs

#### 3. **Profile Versioning & Change Tracking**

- [ ] **Profile History**
  - Each profile has a version number (e.g., `v1`, `v2`)
  - Track changes to hardware specs over time
  - `CHANGELOG.md` auto-generated for profile updates

- [ ] **Deprecation Warnings**
  - Mark outdated profiles (e.g., Windows XP after EOL)
  - Suggest modern alternatives (e.g., ThinkPad T420 → T480)

#### 4. **Cloud Provider Integrations**

- [ ] **Azure DevTest Labs**
  - One-click deployment of TestKit profiles to Azure labs
  - Pre-configured ARM templates

- [ ] **AWS WorkSpaces/EC2**
  - Launch Windows VMs with TestKit profiles as user data
  - CloudFormation stack templates

- [ ] **Google Cloud Platform**
  - Compute Engine custom images with TestKit metadata

#### 5. **Advanced Hardware Definitions**

- [ ] **BIOS/UEFI Settings**
  - Capture common BIOS configurations (Secure Boot, TPM 2.0, legacy boot)
  - Export as Terraform variables or Ansible playbooks

- [ ] **Driver Manifests**
  - List of required drivers for each hardware model
  - Auto-download from manufacturer sites or Windows Update Catalog

- [ ] **Power Profiles**
  - Battery life estimates
  - Power consumption simulation

---

## 🌟 Long-Term Vision (v3.0.0+)

**Target Date**: 2026+

### Moonshot Ideas

#### 1. **AI-Powered Profile Generation**

- **Natural Language Input**: "Generate a profile for a budget laptop from 2019 with discrete graphics"
- **Auto-Discovery**: Scan hardware database from PassMark, UserBenchmark, or NotebookCheck
- **Spec Prediction**: AI suggests realistic component combinations for a given year/price point

#### 2. **TestKit Marketplace**

- **Community Profiles**: Users submit custom profiles (home labs, exotic hardware)
- **Verified Profiles**: Tested and approved by TestKit maintainers
- **Profile Packs**: Curated collections (e.g., "Gaming Handhelds 2023", "Enterprise Workstations")

#### 3. **Live Testing Environment (SaaS)**

- **TestKit Cloud**: On-demand provisioning of Windows VMs based on profiles
- **Pay-per-minute** pricing (compete with BrowserStack)
- **Pre-installed testing tools** (Selenium, Playwright, Appium)

#### 4. **Hardware-in-the-Loop (HIL) Testing**

- **Physical Device Farm**: Partner with hardware vendors to maintain physical devices
- **Remote Access**: RDP/VNC to real ThinkPads, Surfaces, Steam Decks
- **TestKit API**: Schedule tests on real hardware matching profiles

#### 5. **Cross-Platform Expansion**

- **MacOS Profiles**: Apple Silicon (M1/M2/M3) and Intel Mac definitions
- **Linux Hardware Database**: System76, Tuxedo, Purism devices
- **Chrome OS**: Chromebooks with Linux containers

#### 6. **TestKit SDK**

- **Python Library**: `pip install testkit-sdk`
  - `testkit.get_profile("lenovo-thinkpad-t480-windows-10-v1")`
  - `testkit.export_to_docker(profile)`
  - `testkit.search(os="Windows 11", min_ram=16384)`
- **REST API**: `GET /api/v1/profiles?os=Windows+11&manufacturer=Dell`
- **Webhooks**: Notify external systems when new profiles are added

---

## 🔧 Technical Debt & Refactoring

### Immediate (v1.4.0)

- [x] **Migrate from JSON to SQLite** for hardware database
  - Improves query performance for large datasets
  - Enables complex joins and aggregations
  - Easier to manage relationships (e.g., GPU → Manufacturer)

- [ ] **Type Hints & Linting**
  - Add Python type hints to all scripts
  - Enforce with `mypy` in CI pipeline
  - Black/isort for code formatting

- [ ] **Unit Tests**
  - Test suite for `generate_profiles.py`, `export.py`, `validate_db.py`
  - Codecov integration for coverage reporting
  - Target: >80% code coverage

### Future (v2.0.0+)

- [ ] **Modular Exporter Architecture**
  - Plugin system for exporters (e.g., `exporters/docker.py`, `exporters/terraform.py`)
  - Easier to add new formats (Multipass, LXD, Proxmox)

- [ ] **Caching Layer**
  - Cache generated profiles to avoid re-computation
  - Invalidate cache on `laptops.json` changes

- [ ] **Profile Compression**
  - 22k+ JSON files → tarball or database for distribution
  - On-demand decompression for specific profiles

---

## 📊 Metrics & Success Criteria

### Current Metrics (v1.3.0)

- **Hardware Models**: 80
- **Generated Profiles**: 22,122
- **Export Formats**: 4 (Docker, Vagrant, Terraform, WSB)
- **Documentation Pages**: 5 (README, Architecture, Tutorials, Hardware Guide, API Reference)
- **GitHub Stars**: _TBD_
- **Weekly Downloads**: _TBD_

### Target Metrics (v2.0.0)

- **Hardware Models**: 150+
- **Generated Profiles**: 50,000+
- **Export Formats**: 8+ (+ Hyper-V, VMware, Multipass, Proxmox)
- **Web UI Users**: 1,000+ monthly active users
- **CI/CD Integrations**: 20+ example pipelines
- **Community Contributions**: 10+ external profile submissions

---

## 🗓️ Release Schedule

| Version | Target Date | Focus Area | Key Deliverables |
|---------|-------------|------------|------------------|
| **v1.4.0** | Jan 2025 | Hardware Expansion | +25 models (Tier 4), Hyper-V/VMware exports |
| **v1.5.0** | Mar 2025 | Validation & CI/CD | Smoke tests, pipeline examples, search tool |
| **v2.0.0** | Sep 2025 | Web UI & Testing | Dashboard, VM provisioning, benchmarking |
| **v2.1.0** | Dec 2025 | Cloud Integrations | Azure/AWS/GCP templates, driver manifests |
| **v3.0.0** | 2026+ | Ecosystem Growth | Marketplace, SaaS offering, SDK |

---

## 🎯 Prioritization Framework

Each feature is evaluated on:

1. **User Impact** (1-5): How many users benefit?
2. **Effort** (1-5): Development complexity (1 = easy, 5 = hard)
3. **Strategic Value** (1-5): Does this unlock new use cases?

**Priority Score = (User Impact + Strategic Value) / Effort**

### Top 10 Priority Features

| Rank | Feature | Impact | Effort | Strategic | Score |
|------|---------|--------|--------|-----------|-------|
| 1 | Hyper-V Export | 5 | 2 | 4 | **4.5** |
| 2 | Profile Search Tool | 4 | 2 | 3 | **3.5** |
| 3 | Batch Export | 4 | 2 | 3 | **3.5** |
| 4 | Smoke Testing | 4 | 3 | 4 | **2.7** |
| 5 | Web UI Dashboard | 5 | 5 | 5 | **2.0** |
| 6 | SQLite Migration | 3 | 3 | 4 | **2.3** |
| 7 | CI/CD Examples | 4 | 3 | 4 | **2.7** |
| 8 | Tier 4 Hardware | 3 | 2 | 2 | **2.5** |
| 9 | VMware Export | 4 | 3 | 3 | **2.3** |
| 10 | BIOS/UEFI Settings | 2 | 4 | 3 | **1.25** |

---

## 🤝 Community Engagement

### Immediate Actions

- [ ] **Create GitHub Discussions** board for feature requests
- [ ] **Tag "Good First Issue"** for beginner-friendly tasks
- [ ] **Monthly Status Updates** in Discord/Slack/Reddit
- [ ] **Contributor Recognition** in CHANGELOG.md and README.md

### Long-Term

- [ ] **Bug Bounty Program** for critical issues
- [ ] **Annual TestKit Conference** (virtual) for power users
- [ ] **Partner Program** with hardware manufacturers for data access

---

## 🚧 Open Questions & Decisions Needed

1. **Licensing**: Should TestKit remain MIT, or adopt a copyleft license (GPL/AGPL) for v3.0.0 SaaS offering?
2. **Monetization**: If TestKit Cloud launches, what's the pricing model? Freemium? Enterprise only?
3. **Hardware Database Source**: Should we scrape NotebookCheck/PassMark, or partner with vendors for official specs?
4. **Profile Format**: Migrate from JSON to YAML/TOML for better human readability?
5. **Naming Convention**: Current slugs (`lenovo-thinkpad-t480-windows-10-v1`) work but get verbose. Shorten to UUIDs?

---

## 📞 Feedback & Contribution

This roadmap is a **living document**. Priorities may shift based on:

- **User feedback** (GitHub Issues, Discussions)
- **Ecosystem changes** (new Windows releases, hardware trends)
- **Resource availability** (maintainer time, sponsorships)

**Have ideas?**

- 💬 Open a [GitHub Discussion](https://github.com/thookham/TestKit/discussions)
- 🐛 File a [Feature Request](https://github.com/thookham/TestKit/issues/new?template=feature_request.md)
- 📧 Email: [your-email@example.com]

---

**Last Updated**: December 1, 2024  
**Document Version**: 1.0  
**Next Review**: March 1, 2025
