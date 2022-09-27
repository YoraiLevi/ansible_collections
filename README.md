# ansible_windows_modules

A collection of ansible windows modules that I deem missing for personal usage

---

* [ansible_windows_modules](#ansible_windows_modules)
  * [Useful github links](#useful-github-links)
  * [Install](#install)
  * [Playbooks](#playbooks)
    * [TODO ⏳: Testing playboks](#todo--testing-playboks)
  * [Develop](#develop)
  * [docs/Creating Collections](#docscreating-collections)
  * [docs/Collection structure](#docscollection-structure)
  * [Developing plugins](#developing-plugins)
    * [connection](#connection)
      * [WSL_local](#wsl_local)
    * [Developing modules](#developing-modules)
      * [TODO ⏳: Testing Modules](#todo--testing-modules)
        * [TODO ⏳: Integration tests](#todo--integration-tests)
        * [TODO ⏳: Sanity Tests](#todo--sanity-tests)
        * [TODO ⏳: Testing module documentation](#todo--testing-module-documentation)
        * [Unit Tests](#unit-tests)
      * [READ](#read)
      * [Executing](#executing)
        * [Executing Modules from adhoc](#executing-modules-from-adhoc)
        * [Executing Modules from playbook](#executing-modules-from-playbook)
        * [Developing roles](#developing-roles)
  * [Playbooks](#playbooks-1)
    * [Executing](#executing-1)
      * [Executing playbook from collection](#executing-playbook-from-collection)
    * [TODO ⏳: Name resolution](#todo--name-resolution)
    * [TODO ⏳: Search Path](#todo--search-path)
    * [TODO ⏳: python?](#todo--python)
    * [TODO ⏳: powershell?](#todo--powershell)
    * [TODO ⏳: others?](#todo--others)
    * [module_utils](#module_utils)
    * [executing modules from command line (linux/wsl)](#executing-modules-from-command-line-linuxwsl)
* [More Technical Information?](#more-technical-information)
  * [Modules vs Plugins](#modules-vs-plugins)
  * [Modules](#modules)
    * [Install dir](#install-dir)
    * [Info and facts](#info-and-facts)
  * [Reference](#reference)
* [Reading Material](#reading-material)
* [Weird behaviors](#weird-behaviors)

## Useful github links

<https://github.com/ansible/ansible>  
<https://github.com/ansible-collections/ansible.windows>  
<https://github.com/ansible-collections/community.windows>  
[list of all doc documents - https://github.com/ansible/ansible/tree/devel/docs/docsite/rst/dev_guide](https://github.com/ansible/ansible/tree/devel/docs/docsite/rst/dev_guide)

## Install

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

```
python -m ansible galaxy collection install git+https://github.com/YoraiLevi/ansible_windows_modules.git
```

## Playbooks

### TODO ⏳: Testing playboks

<https://docs.ansible.com/ansible/latest/reference_appendices/test_strategies.html>  

## Develop

## [docs/Creating Collections](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_creating.html#creating-collections)

Currently the ansible-galaxy collection command implements the following sub commands:
command | description
-|-
`init`| Create a basic collection skeleton based on the default template included with Ansible or your own template.
`build`| Create a collection artifact that can be uploaded to Galaxy or your own repository.
`publish`| Publish a built collection artifact to Galaxy.
`install`| Install one or more collections.

## [docs/Collection structure](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html#collection-structure)

```
collection/
├── docs/
├── galaxy.yml
├── meta/
│   └── runtime.yml
├── plugins/
│   ├── action
│   ├── become
│   ├── cache
│   ├── callback
│   ├── cliconf
│   ├── connection
│   ├── filter
│   ├── httpapi
│   ├── inventory
│   ├── lookup
│   ├── module_utils
│   ├── modules/
│   │   ├── module1.py
│   │   └── module1.ps1
│   ├── netconf
│   ├── shell
│   ├── strategy
│   ├── terminal
│   ├── test
│   ├── vars
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

## Developing plugins

### connection

winrm: <https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/winrm.py>  
local: <https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/local.py>

#### WSL_local

### Developing modules

#### TODO ⏳: Testing Modules

##### TODO ⏳: Integration tests

`python -m ansible test integration --local`
`ansible-test windows-integration`

Tests for playbooks, by playbooks.
Every new `module` and `plugin` should have integration tests.
<https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html#testing-integration>

<https://github.com/ansible/ansible/tree/devel/test/integration>
<https://github.com/ansible-collections/ansible.windows/tree/main/tests/integration>

<https://docs.ansible.com/ansible/latest/community/collection_contributors/collection_integration_about.html>
<https://kottapar.medium.com/ansible-role-testing-with-molecule-in-windows-subsystem-for-linux-wsl-61a828bf9174>
<https://www.youtube.com/watch?v=FkBX7DXTDc0>

<https://www.ansible.com/blog/adding-integration-tests-to-ansible-content-collections>

<https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general_windows.html#windows-integration-testing>

##### TODO ⏳: Sanity Tests

The primary purpose of these tests is to enforce Ansible coding standards and requirements.
<https://docs.ansible.com/ansible/latest/dev_guide/testing_sanity.html>

##### TODO ⏳: Testing module documentation

<https://docs.ansible.com/ansible/latest/dev_guide/testing_documentation.html#testing-module-documentation>  
<https://docs.ansible.com/ansible/latest/community/documentation_contributions.html#testing-documentation-locally>

##### Unit Tests

<https://docs.ansible.com/ansible/latest/dev_guide/testing_units.html>
<https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html#testing-units-modules>

Unit tests are small isolated tests that target a specific library or module.
Unit tests can be found in test/units <https://github.com/ansible/ansible/tree/devel/test/units>

Normally the Ansible integration tests (which are written in Ansible YAML) provide better testing for most module functionality.

When To Use Unit Tests
There are a number of situations where unit tests are a better choice than integration tests. For example, testing things which are impossible, slow or very difficult to test with integration tests, such as:

Forcing rare / strange / random situations that can’t be forced, such as specific network failures and exceptions

Extensive testing of slow configuration APIs

Situations where the integration tests cannot be run as part of the main Ansible continuous integration running in Azure Pipelines

<https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html#a-complete-example>

#### READ

<https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#testing-your-newly-created>  
<https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html#testing-collections>  
[Testing Ansible](https://docs.ansible.com/ansible/latest/dev_guide/testing_units.html) &
[testing_running_locally](https://docs.ansible.com/ansible/latest/dev_guide/testing_running_locally.html)  
<https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/index.html>  

#### Executing

##### Executing Modules from adhoc

##### Executing Modules from playbook

##### Developing roles

---------------------------------------------------------------

## Playbooks

### Executing

#### Executing playbook from collection

### TODO ⏳: Name resolution

How to do short-hand not fqcn names?

### TODO ⏳: [Search Path](https://docs.ansible.com/ansible/latest/dev_guide/overview_architecture.html#the-ansible-search-path)  

### TODO ⏳: python?

### TODO ⏳: powershell?

### TODO ⏳: others?

### [module_utils](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html#module-utils)

Importing a utility from `module_utils`

```
from ansible_collections.{namespace}.{collection}.plugins.module_utils.{util} import {something}
```

```
#AnsibleRequires -PowerShell ansible_collections.{namespace}.{collection}.plugins.module_utils.{util}
```

### executing modules from command line (linux/wsl)

Linux localhost connection:

Playbook:

```
python -m ansible playbook -i localhost, --connection=local yorailevi.tutorial.facts
```

```
python -m ansible adhoc -m ping localhost
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

<https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#developing-modules>

```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible -m example_module -a 'name=hello new=true' localhost
```

```
ANSIBLE_LIBRARY=./windows/plugins/modules python -m ansible adhoc -m example_module -a 'name=hello new=true' localhost
```

```
python -m ansible adhoc -m yorailevi.windows.example_module -a 'name=hello new=true' localhost
```

windows module

```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible -i $(cat /etc/resolv.conf | grep nameserver | cut -d ' ' -f 2), -u $(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g') -k -e "ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'" -e "ansible_shell_type=cmd" -e "ansible_become_method=runas" all -m example_win_ping
```

# More Technical Information?

## Modules vs Plugins

<https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#modules-and-plugins-what-is-the-difference>
| |  execute on  | purpose
|-|-|-|
Modules | target system | scripts that can be used by the Ansible API, the ansible command, or the ansible-playbook command
Plugins | the control node |  extend Ansible’s core functionality - transforming data, logging output, connecting to inventory, and more.

To confirm that `my_local_module` is available:  
type `ansible-doc -t module my_local_module` to see the documentation for that module  

```
ANSIBLE_LIBRARY=./windows/plugins/modules ansible-doc -t module example_module
ansible-doc -t module  yorailevi.windows.example_module
```

!!!
Currently, the ansible-doc command can parse module documentation only from modules written in Python. If you have a module written in a programming language other than Python, please write the documentation in a Python file adjacent to the module file.
!!!

## Modules

### Install dir

```
ansible-config dump | grep COLLECTIONS
```

### Info and facts

Info and facts modules, are just like any other Ansible Module, with a few minor requirements:

1) They MUST be named <something>_info or <something>_facts, where <something> is singular.

2) Info *_info modules MUST return in the form of the result dictionary so other modules can access them.

3) Fact *_facts modules MUST return in the ansible_facts field of the result dictionary so other modules can access them.

4) They MUST support check_mode.

5) They MUST NOT make any changes to the system.

6) They MUST document the return fields and examples.

## Reference

* [User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)  
* [Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)

# Reading Material

Conventions, tips, and pitfalls: <https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html>  
Ansible for Network Automation: <https://docs.ansible.com/ansible/latest/network/index.html>  
Ansible: Up and Running, 3rd Edition  

# Weird behaviors

1) running with `ANSIBLE_LIBRARY-` module is resolved correctly for both linux and windows (powershell is executed for windows and py to linux) where without it only powershell is resolved

```
$ ansible -m yorailevi.windows.example_module localhost
localhost | FAILED! => {
    "changed": false,
    "module_stderr": "/bin/sh: 1: powershell: Permission denied\n",
    "module_stdout": "",
    "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error",
    "rc": 127
}
```

```
$ ANSIBLE_LIBRARY=./windows/plugins/modules ansible -m example_module localhost -a 'name=hello new=true'
localhost | CHANGED => {
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}
```

```
$ ansible -i $(cat /etc/resolv.conf | grep nameserver | cut -d ' ' -f 2), -u $(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g') -k -e "ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'" -e "ansible_shell_type=cmd" -e "ansible_become_method=runas" all -m yorailevi.windows.example_module
172.30.96.1 | SUCCESS => {
    "changed": false,
    "ping": "example pong"
}
```
