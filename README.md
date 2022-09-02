# ansible_windows_modules
A collection of ansible windows modules that I deem missing for personal usage 


# Install
```
ansible-galaxy collection install git+https://github.com/YoraiLevi/ansible_windows_modules.git
```

# Develop
## creating collections
https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_creating.html#creating-collections
Currently the ansible-galaxy collection command implements the following sub commands:

`init`: Create a basic collection skeleton based on the default template included with Ansible or your own template.

`build`: Create a collection artifact that can be uploaded to Galaxy or your own repository.

`publish`: Publish a built collection artifact to Galaxy.

`install`: Install one or more collections.

## collection structure
https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html#collection-structure

```
collection/
├── docs/
├── galaxy.yml
├── meta/
│   └── runtime.yml
├── plugins/
│   ├── modules/
│   │   └── module1.py
│   ├── inventory/
│   └── .../
├── README.md
├── roles/
│   ├── role1/
│   ├── role2/
│   └── .../
├── playbooks/
│   ├── files/
│   ├── vars/
│   ├── templates/
│   └── tasks/
└── tests/
```
## developing modules
### executing modules from command line (linux/wsl)

Linux localhost connection:
```
ansible -m ping localhost
```
Windows localhost (wsl) connection, requires SSH server active and password authentication enabled:
```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible -i $(cat /etc/resolv.conf | grep nameserver | cut -d ' ' -f 2), -u $(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g') -k -e "ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'" -e "ansible_shell_type=cmd" -e "ansible_become_method=runas" all -m win_ping
```


https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#developing-modules

```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible -m example_module -a 'name=hello new=true' localhost
```

windows module
```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible -i $(cat /etc/resolv.conf | grep nameserver | cut -d ' ' -f 2), -u $(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g') -k -e "ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'" -e "ansible_shell_type=cmd" -e "ansible_become_method=runas" all -m example_win_ping
```