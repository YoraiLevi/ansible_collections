#!powershell
# wsl with ssh enabled on windows:
# ansible -i $(cat /etc/resolv.conf | grep nameserver | cut -d ' ' -f 2), -u $(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g') -k -e "ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'" -e "ansible_shell_type=cmd" -e "ansible_become_method=runas" all -m example_powershell
echo "{`"changed`": false}"