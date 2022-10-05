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

#AnsibleRequires -CSharpUtil Ansible.Basic
## Requires -Module Ansible.ModuleUtils.template_util_powershell
## AnsibleRequires -PowerShell template_util_powershell
## Requires -Version 5
## AnsibleRequires -OSVersion 
## AnsibleRequires -Become

# public static object FromJson(string json); https://github.com/search?q=FromJson+repo%3Aansible%2Fansible+repo%3Aansible-collections%2Fansible.windows+repo%3Aansible-collections%2Fcommunity.windows+extension%3Aps1&type=Code
# public static T FromJson<T>(string json); https://github.com/search?q=FromJson+repo%3Aansible%2Fansible+repo%3Aansible-collections%2Fansible.windows+repo%3Aansible-collections%2Fcommunity.windows+extension%3Aps1&type=Code
# public void Debug(string message); https://github.com/search?p=1&q=Debug+repo%3Aansible%2Fansible+repo%3Aansible-collections%2Fansible.windows+repo%3Aansible-collections%2Fcommunity.windows+extension%3Aps1&type=Code
# public void LogEvent(string message, EventLogEntryType logEntryType = EventLogEntryType.Information, bool sanitise = true); https://github.com/search?q=LogEvent+repo%3Aansible%2Fansible+repo%3Aansible-collections%2Fansible.windows+repo%3Aansible-collections%2Fcommunity.windows+extension%3Aps1&type=Code


# $module.CheckMode - https://docs.ansible.com/ansible/latest/user_guide/playbooks_checkmode.html#using-check-mode
# $module.Diff - https://docs.ansible.com/ansible/latest/user_guide/playbooks_checkmode.html#using-diff-mode

# $module.Deprecate - Deprecate warning output
# $module.Warn - Warning output
# $module.FailJson
# $module.ExitJson
# $module.Params
# $module.Result
# $module.TmpDir - Temporary directory for the module to use
# $module.Verbosity
# $module.ModuleName

#AnsibleRequires -PowerShell ..module_utils.TemplateUtilPowershell

# Create the module spec
# https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
# https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general_windows.html
$spec = @{
    supports_check_mode = $true # https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#declaring-check-mode-support
    # no_log = $false
    options = @{
        argument_required = @{required = $true} # type: str
        argument_str = @{type = 'str'; default = 'default_string'}
        argument_str_choices = @{type = 'str'; default = 'choice1'; choices = @('choice1', 'choice2')}
        argment_str_nolog = @{type = 'str'; default = 'secret_password'; no_log = $true} # doesn't long only when passed explicitly
        argument_bool = @{type = 'bool'; default = $false}
        argument_int = @{type = 'int'; default = 42}
        argument_float = @{type = 'float'; default = 3.14}
        argument_path = @{type = 'path'; default = '%TEMP%'; aliases = @( 'dest' )} # path is evaluated at runtime.
        argument_raw = @{type = 'raw'; default = 'this can be anything'}
        argument_json = @{type = 'json'}
        
        argument_list_str = @{type = 'list'; elements = 'str'; default = @('one','two','three')}
        argument_list_int = @{type = 'list'; elements = 'int'; default = @(1,2,3)}

        # dict
        # options will fill in the default/None values for the arguments.
        # apply_defaults will substiture None with a dictionary of options' default values.
        argument_dict = @{type = 'dict'}
        argument_dict_default = @{type = 'dict'; default = @{key1 = 'default_value'}}
        # options - fills missing keys with option's default value (if no default specified it is None)
        argument_dict_options = @{type = 'dict'; options = @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_dict_default_and_options = @{type = 'dict'; default = @{key1 = 'default_value'}; options = @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_dict_default_and_options_with_defaults = @{type = 'dict'; default = @{key1 = 'default_value'}; options = @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=5}}}
        argument_dict_options_with_defaults = @{type = 'dict'; options = @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=5}}}
        # apply_defaults - substitutes None with dictionary full of option's default
        argument_dict_options_apply_defaults_true = @{type = 'dict'; apply_defaults = $true; options = @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_dict_default_and_options_apply_defaults_true = @{type = 'dict'; default = @{key1 = 'default_value'}; apply_defaults = $true; options = @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_dict_default_and_options_with_defaults_apply_defaults_true = @{type = 'dict'; default = @{key1 = 'default_value'}; apply_defaults = $true; options = @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=5}}}
        argument_dict_options_with_defaults_apply_defaults_true = @{type = 'dict'; apply_defaults = $true; options = @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=5}}}
        
        # list of dicts        
        argument_list_of_dicts = @{type = 'list'; elements = 'dict'}
        argument_list_of_dicts_default = @{type = 'list'; elements = 'dict'; default=@($null,@{},@{key1 = 'default_value'})}
        # options - fills missing keys with option's default value (if no default specified it is None)
        argument_list_of_dicts_options = @{type = 'list'; elements = 'dict'; options= @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_list_of_dicts_default_and_options = @{type = 'list'; elements = 'dict'; default=@($null,@{},@{key1 = 'default_value'}); options= @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_list_of_dicts_options_with_defaults = @{type = 'list'; elements = 'dict'; options= @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=6}}}
        argument_list_of_dicts_default_and_options_with_defaults = @{type = 'list'; elements = 'dict'; default=@($null,@{},@{key1 = 'default_value'}); options= @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=6}}}
        # apply_defaults - substitutes None with dictionary full of option's default
        argument_list_of_dicts_options_apply_defaults_true = @{type = 'list'; elements = 'dict'; apply_defaults = $true; options= @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_list_of_dicts_default_and_options_apply_defaults_true = @{type = 'list'; elements = 'dict'; default=@($null,@{},@{key1 = 'default_value'}); apply_defaults = $true; options= @{key1 = @{type='str'};key2 = @{type='int'}}}
        argument_list_of_dicts_options_with_defaults_apply_defaults_true = @{type = 'list'; elements = 'dict'; apply_defaults = $true; options= @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=6}}}
        argument_list_of_dicts_default_and_options_with_defaults_apply_defaults_true = @{type = 'list'; elements = 'dict'; default=@($null,@{},@{key1 = 'default_value'}); apply_defaults = $true; options= @{key1 = @{type='str'; default='options_value'};key2 = @{type='int'; default=6}}}
        
        # windows only
        argument_sid = @{type = 'sid'}

        # mutually mutually_exclusive
        #interesting usage https://github.com/ansible-collections/ansible.windows/blob/d489bff665954848334e19601109b7fdeeb8c2ab/plugins/modules/win_environment.ps1#L18
        mutually_exclusive_1 = @{type = 'str'}
        mutually_exclusive_2 = @{type = 'str'}

        # pair of required_together arguments
        required_together_1 = @{type = 'str'}
        required_together_2 = @{type = 'str'}
        
        # pair of required_one_of arguments
        required_one_of_1 = @{type = 'str'}
        required_one_of_2 = @{type = 'str'}
        # https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/csharp/Ansible.Basic.cs
        # If required_if_condition has no value (no default/ no input aka null) then this error is thrown
        # "Unhandled exception while executing module: Exception calling \"Create\" with \"3\" argument(s): \"Object reference not set to an instance of an object.\""
        required_if_condition = @{type = 'str'; default="Something that isn't null"}#; choices = @('A','B','C')}
        # Require both
        required_if_A = @{type = 'str'}
        required_if_AA = @{type = 'str'}
        # Require at least one
        required_if_B = @{type = 'str'}
        required_if_BB = @{type = 'str'}
        # required_by with a list of required arguments when condition is specified
        required_by_condition_1 = @{type = 'str'}
        required_by_A = @{type = 'str'}
        required_by_B = @{type = 'str'}
        # required_by with a single of required argument when condition is specified
        required_by_condition_2 = @{type = 'str'}
        required_by_C = @{type = 'str'}
    }
    mutually_exclusive = @(, @('mutually_exclusive_1','mutually_exclusive_2'))
    required_together = @(, @('required_together_1','required_together_2'))
    required_one_of =  @(, @('required_one_of_1','required_one_of_2'))
    required_if = @(@("required_if_condition", "A", @("required_if_A","required_if_AA"),$false),@("required_if_condition", "B", @("required_if_B","required_if_BB"),$true))
    required_by = @{required_by_condition_1 = @('required_by_A','required_by_B'); required_by_condition_2 = @('required_by_C')}
}
#code
# Create the module from the module spec but also include the util spec to merge into our own.
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec, @(Get-YoraiLeviTutorialTemplateUtilPowershellSpec))
$module.Diff.before = @{}
$module.Diff.after = @{}

#Example: Call the module util and pass in the module object so it can access the module options.
Invoke-YoraiLeviTutorialTemplateUtilPowershell -Module $module 
# In diff mode, Ansible provides before-and-after comparisons. Modules that support diff mode display detailed information. 
$module.Diff.before.key = "value_before"
$module.Diff.after.key = "value_after"

$module.Result.ModuleName =  $module.ModuleName
$module.Result.TmpDir =  $module.TmpDir
$module.Result.Verbosity =  $module.Verbosity #-v's
$module.Result.DebugMode = $module.DebugMode
$module.Deprecate("Some Deprecated Text", "2.13")
$module.Warn("Some Warning Text")
$module.Debug("use ANSIBLE_DEBUG=true uses window's event log. doesn't print to console")
if ($module.CheckMode){
    # Modules that support check mode report the changes they would have made. Modules that do not support check mode report nothing and do nothing.
    $module.Result.changed = $false
    $module.Result.output_value = "Module ran in check-mode"
    $module.ExitJson()
}
Try {
    foreach ($tuple in $module.Params.GetEnumerator() )
    {
        # echo the module options to output
        $module.Result[$tuple.Name] = $tuple.Value
    }
    $module.Result.output_value = "this value will be in the output of this module"
    $module.Result.changed = $false
}
Catch {
    $module.FailJson("Failed to execute : $($_.Exception.Message)", $_)
}
$module.ExitJson()