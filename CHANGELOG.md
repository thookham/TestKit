# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
