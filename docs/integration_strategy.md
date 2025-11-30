# Integration Strategy

TestKit aims to be the central "Source of Truth" for hardware and environment definitions. While our core profiles are stored as strictly typed JSON, their real power comes from **exporting** to standard Windows testing formats.

## Supported Formats (Planned)

### 1. Application & Unit Testing (`.runsettings`)
- **Target**: Visual Studio / MSTest
- **Usage**: Configure unit tests to run with specific environment variables or data collectors defined in the profile.
- **Mapping**:
    - `metadata.os_target` -> Test Run Parameters
    - `hardware` -> Custom Data Collectors (mocking hardware info)

### 2. Isolated Testing (`.wsb`)
- **Target**: Windows Sandbox
- **Usage**: Quickly spin up a disposable sandbox configured to match the profile's constraints (where possible).
- **Mapping**:
    - `vGPU` -> Enable/Disable based on `gpu_name`
    - `LogonCommand` -> Scripts to simulate environment variables
    - `MemoryInMB` -> *If supported by host configuration*

### 3. Virtual Machines (`.vbox`, `Vagrantfile`)
- **Target**: VirtualBox, VMware, Hyper-V
- **Usage**: The "Gold Standard" for full OS and Hardware simulation.
- **Mapping**:
    - `cpu_cores` -> VM CPU count
    - `ram_mb` -> VM Memory
    - `storage_gb` -> Disk Size
    - `os_target` -> Base Box / ISO selection

## Workflow
1.  **Select Profile**: `lenovo-t480-win10.json`
2.  **Run Exporter**: `python scripts/export.py --format wsb --output t480.wsb`
3.  **Execute**: Double-click `t480.wsb` to launch the sandbox.
