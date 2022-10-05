#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# https://github.com/ansible-collections/ansible.windows/blob/main/plugins/doc_fragments/web_request.py
class ModuleDocFragment(object):
    # Documentation for TemplateUtilPowershell module util
    # https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#documentation-fragments
    DOCUMENTATION = r'''
options:
    module_util_string_argument:
        description:
            - a string argument provided by the module util
        required: true
        default: null
        version_added: "1.0.0"
    '''
    RETURN = r'''
# extends_documentation_fragment is not yet supported for RETURN. https://groups.google.com/u/1/g/ansible-project/c/dvNL9z9MfSc
output_from_module_util:
    description: a string returned by the module util, which is the same as the input
    returned: success
    type: str
'''
