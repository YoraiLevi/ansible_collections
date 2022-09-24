#!powershell
# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general_windows.html#developing-modules-general-windows
Set-StrictMode -Version 2.0

# ArgvParser: Utility used to convert a list of arguments to an escaped string compliant with the Windows argument parsing rules.
# CamelConversion: Utility used to convert camelCase strings/lists/dicts to snake_case.
# CommandUtil: Utility used to execute a Windows process and return the stdout/stderr and rc as separate objects.
# FileUtil: Utility that expands on the Get-ChildItem and Test-Path to work with special files like C:\pagefile.sys.
# Legacy: General definitions and helper utilities for Ansible module.
# LinkUtil: Utility to create, remove, and get information about symbolic links, junction points and hard inks.
# SID: Utilities used to convert a user or group to a Windows SID and vice versa
# https://github.com/ansible/ansible/tree/devel/lib/ansible/module_utils/powershell

# Requires -Module Ansible.ModuleUtils.Legacy
# Set-Attr
# Exit-Json
# Fail-Json
# Add-Warning
# Add-DeprecationWarning
# Expand-Environment
# Get-AnsibleParam 
# ConvertTo-Bool
# Parse-Args
# Get-FileChecksum
# Get-PendingRebootStatus



# Requires -Module Ansible.ModuleUtils.template_util_powershell
# AnsibleRequires -PowerShell template_util_powershell
# Requires -Version 5
# AnsibleRequires -OSVersion 
# AnsibleRequires -Become
