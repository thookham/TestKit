# TestKit Troubleshooting Guide

This document provides solutions to common issues encountered when using TestKit.

---

## 🐍 Python & Installation Issues

### `ModuleNotFoundError: No module named 'xxx'`

**Solution:**

```bash
pip install -r requirements.txt
```

If there's no `requirements.txt`, TestKit uses only Python stdlib. Ensure you're using Python 3.7+.

### `python: command not found`

**Solution:**

- On Windows, try `py` instead of `python`
- Ensure Python is in your PATH: `py --version`
- Install from [python.org](https://www.python.org/downloads/)

---

## 🐳 Docker Issues

### Container Fails to Start

**Error:** `Error response from daemon: driver failed programming external connectivity...`

**Solution:**

- Ensure port 8000 is not in use by another application
- Check if the Docker daemon is running: `docker info`
- Try restarting Docker Desktop
- On Windows, ensure "Use WSL 2 based engine" is enabled

### Volume Mount Errors

**Error:** `docker: Error response from daemon: invalid mode: /app/profiles.`

**Solution:**

- Ensure you are running the command from the root of the repository
- On Windows, share the drive with Docker in Docker Desktop → Settings → Resources → File Sharing
- Use absolute paths: `-v %cd%/profiles:/app/profiles` (CMD) or `-v $(pwd)/profiles:/app/profiles` (Bash)

### Windows Containers Not Available

**Error:** `no matching manifest for linux/amd64 in the manifest list`

**Solution:**

- TestKit uses Windows-based images. Right-click Docker tray icon → "Switch to Windows containers"
- Requires Windows 10 Pro/Enterprise with Hyper-V enabled

---

## ⚡ Hyper-V Issues

### Script Fails with Access Denied

**Error:** `Access is denied. You need Administrator rights...`

**Solution:**

- Run PowerShell as **Administrator** (right-click → Run as administrator)
- Ensure your user is in the "Hyper-V Administrators" group

### Hyper-V Not Installed

**Error:** `The term 'New-VM' is not recognized...`

**Solution:**

1. Open PowerShell as Admin
2. Run: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`
3. Restart your computer
4. Import the module: `Import-Module Hyper-V`

### Windows 11 VM Won't Boot (TPM/Secure Boot)

**Error:** `This PC doesn't meet the minimum system requirements`

**Solution:**

The generated script enables TPM and Secure Boot by default. If issues persist:

```powershell
# Check if TPM is enabled on the VM
Get-VMSecurity -VMName "YourVM"

# Manually enable if needed
Set-VMKeyProtector -VMName "YourVM" -NewLocalKeyProtector
Enable-VMTPM -VMName "YourVM"
```

---

## 🖥️ VMware Issues

### .vmx File Won't Open

**Error:** `Cannot open the configuration file`

**Solution:**

- Ensure VMware Workstation/Player is installed (not just VMware vSphere Client)
- Check that the `.vmx` file path contains no special characters
- Try importing via File → Open instead of double-clicking

### "The configuration file was created by a different version"

**Solution:**

- Edit the `.vmx` file and change `virtualHW.version` to match your VMware version:
  - VMware 16: `virtualHW.version = "18"`
  - VMware 15: `virtualHW.version = "16"`

---

## 📦 Vagrant Issues

### Box Download Fails

**Error:** `The box 'xxx' could not be found`

**Solution:**

- Ensure you have internet connectivity
- Check the box name is correct (e.g., `gusztavvargadr/windows-10`)
- Try `vagrant box add <box_name>` separately to diagnose

### Vagrant Up Hangs at "Waiting for machine to boot"

**Solution:**

- Ensure VirtualBox is installed and up to date
- Enable virtualization in BIOS (VT-x/AMD-V)
- Check VirtualBox GUI for any error dialogs on the VM
- Try adding `config.vm.boot_timeout = 600` to Vagrantfile

### VirtualBox Kernel Driver Not Installed (Linux)

**Error:** `Kernel driver not installed (rc=-1908)`

**Solution:**

```bash
sudo /sbin/vboxconfig
# Or reinstall VirtualBox
```

---

## ☁️ Terraform Issues

### AWS Credentials Not Found

**Error:** `No valid credential sources found`

**Solution:**

1. Configure AWS CLI: `aws configure`
2. Or set environment variables:

   ```bash
   export AWS_ACCESS_KEY_ID="your-key"
   export AWS_SECRET_ACCESS_KEY="your-secret"
   export AWS_REGION="us-east-1"
   ```

### Terraform Init Fails

**Error:** `Error: Failed to install provider`

**Solution:**

- Check internet connectivity
- If behind a proxy, configure `HTTP_PROXY` and `HTTPS_PROXY` environment variables
- Try: `terraform init -upgrade`

### Instance Type Not Available

**Error:** `The requested instance type is not supported in the requested Availability Zone`

**Solution:**

- Edit the `.tf` file and change the `availability_zone` or `instance_type`
- Use `aws ec2 describe-instance-type-offerings --location-type availability-zone` to find supported types

---

## 🪟 Windows Sandbox Issues

### Sandbox Fails to Start

**Error:** `Windows Sandbox failed to start`

**Solution:**

1. Ensure Windows Sandbox feature is enabled:

   ```powershell
   Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -Online
   ```

2. Restart your computer
3. Check that Hyper-V is also enabled (required dependency)

### .wsb File Opens in Notepad Instead of Sandbox

**Solution:**

- Right-click the `.wsb` file → Open with → Choose another app → Windows Sandbox
- Set as default for `.wsb` files

### Sandbox Runs But Apps Don't Work

**Solution:**

- Windows Sandbox is a minimal environment. Some apps may need:
  - .NET Framework: Add a `<Command>` in `.wsb` to install it
  - Visual C++ Redistributables
  - Internet access enabled in the `.wsb` file: `<Networking>Enable</Networking>`

---

## 🔐 Permission Issues

### Access Denied on Export

**Error:** `PermissionError: [Errno 13] Permission denied: 'exports/...'`

**Solution:**

- Ensure the `exports` directory is not open in another program (File Explorer, VS Code, etc.)
- Run the terminal as Administrator
- Check file attributes are not Read-Only: `attrib -r exports\* /s`

### Script Execution Disabled (PowerShell)

**Error:** `cannot be loaded because running scripts is disabled on this system.`

**Solution:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## ⚙️ Profile Generation Issues

### Missing Hardware Data

**Error:** `KeyError: 'cpu_options'`

**Solution:**

- The `laptops.json` database might be corrupt or have invalid entries
- Validate JSON syntax: `python -m json.tool scripts/db/laptops.json`
- Pull the latest version: `git pull origin main`

### Invalid JSON Output

**Solution:**

- Check `generate_profiles.py` output for warnings
- Ensure write permissions to `profiles/` directory
- Clear the profiles directory and regenerate: `rm -rf profiles/* && python scripts/generate_profiles.py`

### `TypeError: unhashable type: 'dict'`

**Solution:**

- This was a known bug in versions before v1.4.0
- Update to the latest version: `git pull origin main`

---

## 🔍 Search & Batch Export Issues

### No Profiles Found

**Error:** `Found 0 matching profiles`

**Solution:**

- Check your filter values (case-sensitive for some fields)
- Use `--make "Lenovo"` not `--make "lenovo"` (exact case match)
- List available values first: `python scripts/search_profiles.py --list-makes`

### Batch Export Very Slow

**Solution:**

- Use `--limit` to restrict the number of profiles: `--limit 100`
- Export to SSD instead of HDD
- Ensure antivirus isn't scanning each generated file

---

## 📝 General

### Where Are the Logs?

- TestKit outputs to console (stdout/stderr)
- Redirect to file if needed: `python scripts/export.py ... 2>&1 | tee export.log`
- For Docker: `docker logs <container_id>`

### How Do I Update TestKit?

```bash
git pull origin main
python scripts/generate_profiles.py  # Regenerate profiles with latest hardware
```

### Profile Says Win11 But VM Shows Win10

- TestKit provides **profile definitions**, not actual OS images
- You need to provide a Windows ISO matching the profile's OS
- The profile sets hardware specs and environment variables

---

## 🐛 Still Stuck?

If your issue isn't listed here, please [open a GitHub issue](https://github.com/thookham/TestKit/issues/new) with:

1. The exact command you ran
2. The full error message (copy/paste, not screenshot)
3. Your environment:
   - OS version (`winver` or `cat /etc/os-release`)
   - Python version (`python --version`)
   - Docker version (`docker --version`) if applicable
4. TestKit version (`git describe --tags` or check CHANGELOG.md)
