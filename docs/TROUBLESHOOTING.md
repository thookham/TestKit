# TestKit Troubleshooting Guide

This document provides solutions to common issues encountered when using TestKit.

## 🐳 Docker Issues

### Container Fails to Start

**Error:** `Error response from daemon: driver failed programming external connectivity...`
**Solution:**

- Ensure port 8000 is not in use by another application.
- Check if the Docker daemon is running.
- Try restarting Docker Desktop.

### Volume Mount Errors

**Error:** `docker: Error response from daemon: invalid mode: /app/profiles.`
**Solution:**

- Ensure you are running the command from the root of the repository.
- On Windows, ensure you have shared the drive with Docker in Docker Desktop settings.
- Use absolute paths if relative paths fail (e.g., `-v %cd%/profiles:/app/profiles`).

## 🔐 Permission Issues

### Access Denied on Export

**Error:** `PermissionError: [Errno 13] Permission denied: 'exports/...'`
**Solution:**

- Ensure the `exports` directory is not open in another program (like File Explorer or VS Code).
- Run the terminal or command prompt as Administrator.
- Check file attributes to ensure they are not Read-Only.

### Script Execution Disabled

**Error:** `cannot be loaded because running scripts is disabled on this system.`
**Solution:**

- This is a PowerShell security feature.
- Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` to allow local scripts.

## ⚙️ Profile Generation Issues

### Missing Hardware Data

**Error:** `KeyError: 'cpu_options'`
**Solution:**

- The `laptops.json` database might be corrupt or missing entries.
- Verify the JSON syntax in `scripts/db/laptops.json`.
- Ensure you are using the latest version of the repository.

### Invalid JSON Output

**Solution:**

- If generated profiles are empty or invalid, check the `generate_profiles.py` script output for any warnings.
- Ensure you have write permissions to the `profiles` directory.

## 📝 General

### Where are the logs?

- TestKit currently outputs logs to the console (stdout/stderr).
- When running in Docker, use `docker logs <container_id>` to view them.

### Reporting Bugs

If you encounter an issue not listed here, please open an issue on GitHub with:

1. The command you ran.
2. The full error message.
3. Your OS and Python/Docker version.
