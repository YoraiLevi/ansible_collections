#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#ansible-metadata-block
# example documentation string: https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml

# See https://docs.ansible.com/ansible/devel/dev_guide/developing_modules_documenting.html for more information
# If a key doesn't apply to your module (ex: choices, default, or
# aliases) you can use the word 'null', or an empty list, [], where
# appropriate.
DOCUMENTATION = r'''
---
# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#documentation-fields
module: win_template_powershell
short_description: A template module that uses Powershell
description:
    - Longer description of the module.
    - You might include instructions.
version_added: "1.0.0"
author: "Author Name (@github_handle)"
options:
# One or more of the following
    option_name:
        description:
            - Description of the options goes here.
            - Must be written in sentences.
        required: true
        default: a string or the word null
        aliases:
          - repo_name
        version_added: "1.0.0"
notes:
    - This is a complete example with all the options.
requirements:
    - list of required things.
    - like the factor package
    - zypper >= 1.0
extends_documentation_fragment:
    - yorailevi.tutorial.TemplateUtilPowershell
'''

# examples are ready for the user to copy and paste into a playbook
EXAMPLES = r'''
# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#examples-block
- name: Ensure foo is installed
  yorailevi.tutorial.win_template_powershell:
    name: foo
    state: present
'''


RETURN = r'''
# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#return-block
# extends_documentation_fragment is not yet supported for RETURN. https://groups.google.com/u/1/g/ansible-project/c/dvNL9z9MfSc
output_from_module_util: 
    description: a string returned by the module util, which is the same as the input
    returned: success
    type: str

return_value_one:
    description: string describing the return value
    returned: success
    type: string
    # elements: null
    sample: hello
    version_added: 1.0.0
    # contains: 
'''
