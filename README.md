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
```
#/tmp/args.json
{
    "ANSIBLE_MODULE_ARGS": {
        "name": "hello",
        "new": true
    }
}
python ./windows/plugins/modules/example_module.py /tmp/args.json
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
# Modules vs Plugins:
https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#modules-and-plugins-what-is-the-difference
| |  execute on  | purpose
|-|-|-|
Modules | target system | scripts that can be used by the Ansible API, the ansible command, or the ansible-playbook command
Plugins | the control node |  extend Ansible’s core functionality - transforming data, logging output, connecting to inventory, and more.

To confirm that `my_local_module` is available:  
type `ansible-doc -t module my_local_module` to see the documentation for that module  
```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible-doc -t module  example_module
```
!!!
Currently, the ansible-doc command can parse module documentation only from modules written in Python. If you have a module written in a programming language other than Python, please write the documentation in a Python file adjacent to the module file.
!!!
# Modules
## Info and facts
Info and facts modules, are just like any other Ansible Module, with a few minor requirements:

1) They MUST be named <something>_info or <something>_facts, where <something> is singular.

2) Info *_info modules MUST return in the form of the result dictionary so other modules can access them.

3) Fact *_facts modules MUST return in the ansible_facts field of the result dictionary so other modules can access them.

4) They MUST support check_mode.

5) They MUST NOT make any changes to the system.

6) They MUST document the return fields and examples.


# Reference
https://docs.ansible.com/ansible/latest/user_guide/index.html


# Testing TODO
https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#testing-your-newly-created-



# Reading Material
Conventions, tips, and pitfalls: https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html
Ansible for Network Automation: https://docs.ansible.com/ansible/latest/network/index.html
Ansible: Up and Running, 3rd Edition
