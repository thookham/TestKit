import json
import os
import argparse
from pathlib import Path

from typing import Dict, Any

def generate_launch_script(output_dir: str, profile_id: str, commands: Dict[str, str], description: str) -> None:
    """Generates cross-platform launch scripts (.ps1 and .sh)."""
    
    # PowerShell Script
    ps1_content = f"""# Launch Script for {profile_id}
# {description}
Write-Host "Starting {profile_id} environment..." -ForegroundColor Cyan
{commands['ps1']}
"""
    ps1_path = os.path.join(output_dir, "launch.ps1")
    with open(ps1_path, 'w') as f:
        f.write(ps1_content)
        
    # Bash Script
    sh_content = f"""#!/bin/bash
# Launch Script for {profile_id}
# {description}
echo "Starting {profile_id} environment..."
{commands['sh']}
"""
    sh_path = os.path.join(output_dir, "launch.sh")
    with open(sh_path, 'w') as f:
        f.write(sh_content)
    
    # Make bash script executable
    try:
        os.chmod(sh_path, 0o755)
    except:
        pass
        
    print(f"Generated launch scripts: {ps1_path}, {sh_path}")

def export_docker(profile: Dict[str, Any], output_dir: str) -> None:
    """Generates a Dockerfile for the given profile."""
    profile_id = profile.get('id', 'unknown')
    dockerfile_content = f"""# TestKit Profile: {profile.get('make')} {profile.get('model')}
# OS: {profile.get('os')}
# Hardware: {profile.get('hardware', {}).get('cpu_count')} Cores, {profile.get('hardware', {}).get('ram_mb')}MB RAM

FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set Environment Variables to simulate hardware specs
ENV TESTKIT_PROFILE_ID="{profile_id}"
ENV TESTKIT_MAKE="{profile.get('make')}"
ENV TESTKIT_MODEL="{profile.get('model')}"
ENV TESTKIT_CPU_CORES="{profile.get('hardware', {}).get('cpu_count')}"
ENV TESTKIT_RAM_MB="{profile.get('hardware', {}).get('ram_mb')}"
ENV TESTKIT_GPU_VRAM_MB="{profile.get('hardware', {}).get('gpu_vram_mb')}"
ENV TESTKIT_RESOLUTION="{profile.get('hardware', {}).get('screen_resolution')}"

# Placeholder for actual simulation logic
RUN echo "Initializing TestKit Environment for {profile_id}"
"""
    output_path = os.path.join(output_dir, f"{profile_id}.Dockerfile")
    with open(output_path, 'w') as f:
        f.write(dockerfile_content)
    print(f"Exported Dockerfile: {output_path}")
    
    # Generate Launch Scripts
    commands = {
        'ps1': f'docker build -t testkit-{profile_id} -f {profile_id}.Dockerfile .\ndocker run -it --rm testkit-{profile_id}',
        'sh': f'docker build -t testkit-{profile_id} -f {profile_id}.Dockerfile .\ndocker run -it --rm testkit-{profile_id}'
    }
    generate_launch_script(output_dir, profile_id, commands, "Builds and runs the Docker container")

def export_vagrant(profile: Dict[str, Any], output_dir: str) -> None:
    """Generates a Vagrantfile for the given profile."""
    profile_id = profile.get('id', 'unknown')
    ram_mb = profile.get('hardware', {}).get('ram_mb', 2048)
    cpu_cores = profile.get('hardware', {}).get('cpu_count', 2)
    
    vagrantfile_content = f"""# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/windows10" # Placeholder box
  config.vm.define "{profile_id}" do |node|
    node.vm.provider "virtualbox" do |vb|
      vb.memory = "{ram_mb}"
      vb.cpus = "{cpu_cores}"
      vb.name = "TestKit - {profile_id}"
    end
    node.vm.provision "shell", inline: <<-SHELL
      echo "Setting up TestKit Profile: {profile_id}"
      setx TESTKIT_PROFILE_ID "{profile_id}" /M
    SHELL
  end
end
"""
    output_path = os.path.join(output_dir, f"{profile_id}.Vagrantfile")
    with open(output_path, 'w') as f:
        f.write(vagrantfile_content)
    print(f"Exported Vagrantfile: {output_path}")
    
    # Generate Launch Scripts
    commands = {
        'ps1': 'vagrant up\nvagrant ssh',
        'sh': 'vagrant up\nvagrant ssh'
    }
    generate_launch_script(output_dir, profile_id, commands, "Provisions and connects to the Vagrant VM")

def export_terraform(profile: Dict[str, Any], output_dir: str) -> None:
    """Generates a Terraform configuration for the given profile."""
    profile_id = profile.get('id', 'unknown')
    ram_mb = profile.get('hardware', {}).get('ram_mb', 2048)
    cpu_cores = profile.get('hardware', {}).get('cpu_count', 2)
    os_target = profile.get('os', 'windows-10')
    
    # Convert RAM to GB for cloud instances
    ram_gb = max(1, ram_mb // 1024)
    
    # Map to AWS instance types (simplified)
    instance_type_map = {
        1: "t2.micro",
        2: "t2.small",
        4: "t2.medium",
        8: "t2.large",
        16: "t2.xlarge"
    }
    instance_type = instance_type_map.get(ram_gb, "t2.medium")
    
    terraform_content = f"""# TestKit Profile: {profile_id}
# Generated Terraform configuration for cloud deployment

terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

variable "aws_region" {{
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}}

resource "aws_instance" "testkit_{profile_id.replace('-', '_')}" {{
  ami           = data.aws_ami.windows.id
  instance_type = "{instance_type}"
  
  tags = {{
    Name               = "TestKit-{profile_id}"
    TestKitProfileID   = "{profile_id}"
    TestKitCPUCores    = "{cpu_cores}"
    TestKitRAM_MB      = "{ram_mb}"
    TestKitOS          = "{os_target}"
  }}
  
  user_data = <<-EOT
    <powershell>
    Write-Host "Initializing TestKit Profile: {profile_id}"
    [Environment]::SetEnvironmentVariable("TESTKIT_PROFILE_ID", "{profile_id}", "Machine")
    [Environment]::SetEnvironmentVariable("TESTKIT_CPU_CORES", "{cpu_cores}", "Machine")
    [Environment]::SetEnvironmentVariable("TESTKIT_RAM_MB", "{ram_mb}", "Machine")
    </powershell>
  EOT
}}

data "aws_ami" "windows" {{
  most_recent = true
  owners      = ["amazon"]
  
  filter {{
    name   = "name"
    values = ["Windows_Server-2019-English-Full-Base-*"]
  }}
}}

output "instance_id" {{
  value = aws_instance.testkit_{profile_id.replace('-', '_')}.id
}}

output "public_ip" {{
  value = aws_instance.testkit_{profile_id.replace('-', '_')}.public_ip
}}
"""
    output_path = os.path.join(output_dir, f"{profile_id}.tf")
    with open(output_path, 'w') as f:
        f.write(terraform_content)
    print(f"Exported Terraform: {output_path}")
    
    # Generate Launch Scripts
    commands = {
        'ps1': 'terraform init\nterraform apply -auto-approve',
        'sh': 'terraform init\nterraform apply -auto-approve'
    }
    generate_launch_script(output_dir, profile_id, commands, "Initializes and applies Terraform configuration")

def export_wsb(profile: Dict[str, Any], output_dir: str) -> None:
    """Generates a Windows Sandbox configuration (.wsb) for the given profile."""
    profile_id = profile.get('id', 'unknown')
    ram_mb = profile.get('hardware', {}).get('ram_mb', 2048)
    cpu_cores = profile.get('hardware', {}).get('cpu_count', 2)
    gpu_vram = profile.get('hardware', {}).get('gpu_vram_mb', 0)
    
    # Windows Sandbox supports vGPU (Enable/Disable)
    vgpu_enabled = "Enable" if gpu_vram > 0 else "Disable"
    
    wsb_content = f"""<Configuration>
  <VGpu>{vgpu_enabled}</VGpu>
  <MemoryInMB>{ram_mb}</MemoryInMB>
  <LogonCommand>
    <Command>powershell -ExecutionPolicy Bypass -Command "Write-Host 'TestKit Profile: {profile_id}' -ForegroundColor Green; [Environment]::SetEnvironmentVariable('TESTKIT_PROFILE_ID', '{profile_id}', 'Machine'); [Environment]::SetEnvironmentVariable('TESTKIT_CPU_CORES', '{cpu_cores}', 'Machine'); [Environment]::SetEnvironmentVariable('TESTKIT_RAM_MB', '{ram_mb}', 'Machine'); [Environment]::SetEnvironmentVariable('TESTKIT_GPU_VRAM_MB', '{gpu_vram}', 'Machine'); Write-Host 'Environment configured for testing.' -ForegroundColor Cyan"</Command>
  </LogonCommand>
</Configuration>
"""
    output_path = os.path.join(output_dir, f"{profile_id}.wsb")
    with open(output_path, 'w') as f:
        f.write(wsb_content)
    print(f"Exported Windows Sandbox: {output_path}")
    
    # Generate Launch Scripts
    commands = {
        'ps1': f'Start-Process "{profile_id}.wsb"',
        'sh': f'cmd.exe /c start {profile_id}.wsb'
    }
    generate_launch_script(output_dir, profile_id, commands, "Launches Windows Sandbox")

def main():
    parser = argparse.ArgumentParser(description="Export TestKit profiles to various formats.")
    parser.add_argument("--profile", help="Path to a specific profile JSON file", required=True)
    parser.add_argument("--format", choices=["docker", "vagrant", "terraform", "wsb"], required=True, help="Export format")
    parser.add_argument("--output", default="exports", help="Output directory")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        
    try:
        with open(args.profile, 'r') as f:
            profile_data = json.load(f)
            
        if args.format == "docker":
            export_docker(profile_data, args.output)
        elif args.format == "vagrant":
            export_vagrant(profile_data, args.output)
        elif args.format == "terraform":
            export_terraform(profile_data, args.output)
        elif args.format == "wsb":
            export_wsb(profile_data, args.output)
            
    except Exception as e:
        print(f"Error exporting profile: {e}")

if __name__ == "__main__":
    main()
