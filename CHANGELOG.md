# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2024-12-01

### Added
- **Tier 3 / Specialized Hardware**: Added 15 new profiles for edge cases and industrial use:
  - **Industrial/Rugged**: Zebra L10, Honeywell RT10, Getac V110
  - **Point of Sale (POS)**: NCR RealPOS XR7, Oracle Micros Workstation 6, Toshiba TCx 800
  - **Medical**: HP EliteOne Healthcare, Dell Latitude Rugged Extreme, Onyx Venus
  - **Legacy/Obscure**: Sony Vaio P, OQO Model 02, Fujitsu P1610, IBM ThinkPad 701C
  - **SBC**: Raspberry Pi 4 (WoA), Odroid H3+
- **Profile Expansion**: Total hardware definitions increased to **80** models.
- **Generated Profiles**: Total count reached **22,122** (+8%).

### Changed
- Updated documentation with new categories and statistics.

## [1.2.0] - 2024-12-01

### Added
- **Tier 2 / Regional Manufacturers**: Added 20 new hardware profiles from diverse global manufacturers:
  - **Europe/Boutique**: Framework, System76, Schenker (XMG), Medion, Tuxedo, Purism, Slimbook
  - **Asia/Regional**: Fujitsu, Vaio, Dynabook (Toshiba), Chuwi, Teclast, Infinix, Tecno
  - **Specialized/OEM**: Clevo, Tongfang, Getac, Durabook, Panasonic, Pine64
- **Automated Launch Scripts**: `export.py` now generates `launch.ps1` and `launch.sh` for all exports, enabling one-click environment startup.
- **Profile Expansion**: Total hardware definitions increased to **65** models.
- **Generated Profiles**: Total count reached **20,446** (+21%).

### Changed
- Updated `export.py` to include launch script generation logic.
- Updated documentation to reflect new hardware and features.

## [1.1.0] - 2024-11-30

### Added
- **Tier 1 Manufacturers**: Added 11 new hardware profiles from industry-leading manufacturers
  - **Acer** (3 models): Aspire Vero (2021), Swift 3 (2020), Predator Helios 300 (2021)
  - **MSI** (2 models): GS66 Stealth (2020), Creator Z16 (2021)
  - **Gigabyte** (2 models): Aero 15 OLED (2021), Aorus 15G (2020)
  - **System76** (2 models): Thelio Desktop (2021), Lemur Pro (2020)
  - **Toshiba** (2 models): Satellite C55 (2014), Portégé X30 (2017)
- **Profile Expansion**: Total hardware definitions increased from 34 to 45 models (+32%)
- **Generated Profiles**: Profile count increased from 12,254 to **16,912** (+38%)
- **Visual Documentation**: Added professional diagrams and visual assets
  - Architecture workflow diagram
  - Hardware coverage heat map
  - Export flow diagram
  - Professional banner/logo
- **Enhanced Documentation**:
  - Comprehensive README overhaul with badges, statistics, and best practices
  - New ARCHITECTURE.md - Technical deep-dive into TestKit design
  - New TUTORIALS.md - Step-by-step guides for common scenarios
  - New HARDWARE_GUIDE.md - Complete catalog of all 45 base models
  - New API_REFERENCE.md - Complete CLI and schema documentation
  - Enhanced CONTRIBUTING.md with detailed contribution guidelines
  - GitHub issue templates and PR template
- **Documentation Sections**:
  - "Why TestKit Stands Out" - Competitive comparisons
  - "Best Practices" - Guidelines for effective profile usage
  - "Learning Resources" - Organized documentation index
  - "Statistics" - Comprehensive project metrics
  - Enhanced FAQ with 6 common questions

### Changed
- Updated all documentation to reflect expanded hardware coverage
- Reorganized README structure for better navigation
- Enhanced Quick Start section with examples using new Tier 1 models
- Improved Hardware Categories table with detailed profile counts
- Updated repository structure documentation

### Technical Details
- All new profiles validated against JSON schema
- CI/CD pipeline successfully processes expanded 45-model database
- Profile generation time scales linearly with hardware count
- All export formats (Docker, Vagrant, Terraform, WSB) tested with new profiles

---

## [1.0.0] - 2024-11-29

### Added
- Initial public release of TestKit.
- **Database**: 34 hardware definitions covering laptops, servers, handhelds, and cloud VMs.
- **Generator**: Script to generate combinatorial profiles based on hardware specs and OS versions.
- **Profiles**: 12,254 unique hardware profiles generated.
- **Exporters**:
    - Docker (`Dockerfile`)
    - Vagrant (`Vagrantfile`)
    - Terraform (`.tf`)
    - Windows Sandbox (`.wsb`)
- **Documentation**: Comprehensive README with usage guides and examples.
- **CI/CD**: GitHub Actions for validation and auto-generation.
- **Community Files**:
    - MIT License
    - Code of Conduct (Contributor Covenant 2.1)
    - Security Policy
    - Contributing Guidelines
- **Validation**: Database validation script with schema checking
- **Hardware Coverage**:
    - Standard Laptops (Lenovo, Dell, HP)
    - Gaming Systems (Razer, Alienware)
    - Handhelds (Steam Deck, ROG Ally, Legion Go, GPD)
    - Tablets/2-in-1 (Microsoft Surface)
    - Servers (Dell PowerEdge, HP ProLiant)
    - Cloud VMs (AWS, Azure)
    - Legacy Systems (Windows XP, Vista, 7)
    - Global Manufacturers (Xiaomi, Huawei)
