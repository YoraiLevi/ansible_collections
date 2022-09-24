
# https://github.com/ansible-collections/ansible.windows/blob/main/plugins/module_utils/WebRequest.psm1
Function Invoke-YoraiLeviTutorialTemplateUtilPowershell {
    <#
    .SYNOPSIS
        A function that takes in an AnsibleModule object called under the -Module parameter which it can use to get the shared options
    .DESCRIPTION
        Because these options can be shared across various module it is highly recommended to keep the module option names and aliases in the shared spec as specific as they can be. For example do not have a util option called password, rather you should prefix it with a unique name like acme_password
    .NOTES
        Information or caveats about the function e.g. 'This function is not supported in Linux'
    .LINK
        https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general_windows.html#exposing-shared-module-options
    .EXAMPLE
        Test-MyTestFunction -Verbose
        Explanation of the function or its result. You can include multiple examples with additional .EXAMPLE lines
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [ValidateScript({ $_.GetType().FullName -eq 'Ansible.Basic.AnsibleModule' })]
        $Module,

        [Alias("msg")]
        [System.String]
        $Message
    )

     # Set module options for parameters unless they were explicitly passed in.
     if ($Module) {
        foreach ($param in $PSCmdlet.MyInvocation.MyCommand.Parameters.GetEnumerator()) {
            if ($PSBoundParameters.ContainsKey($param.Key)) {
                # Was set explicitly we want to use that value
                continue
            }

            foreach ($alias in @($Param.Key) + $param.Value.Aliases) {
                if ($Module.Params.ContainsKey($alias)) {
                    $var_value = $Module.Params.$alias -as $param.Value.ParameterType
                    Set-Variable -Name $param.Key -Value $var_value
                    break
                }
            }
        }
    }
    # code here
    $Module.Result.message = $Message
}
Function Get-YoraiLeviTutorialTemplateUtilPowershellSpec {
    <#
    .SYNOPSIS
        Used by modules to get the argument spec fragment for AnsibleModule.
    .DESCRIPTION
        PowerShell module utils can easily expose common module options that a module can use when building its argument spec. This allows common features to be stored and maintained in one location and have those features used by multiple modules with minimal effort. Any new features or bugfixes added to one of these utils are then automatically used by the various modules that call that util.
        An example of this would be to have a module util that handles authentication and communication against an API This util can be used by multiple modules to expose a common set of module options like the API endpoint, username, password, timeout, cert validation, and so on without having to add those options to each module spec.
        The standard convention for a module util that has a shared argument spec would have
        A Get-<namespace.name.util name>Spec function that outputs the common spec for a module
            It is highly recommended to make this function name be unique to the module to avoid any conflicts with other utils that can be loaded
            The format of the output spec is a Hashtable in the same format as the $spec used for normal modules
        
    .NOTES
        ???
    .LINK
        https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general_windows.html#exposing-shared-module-options
    .EXAMPLE
        $spec = @{
        options = @{}
        }
        $module = [Ansible.Basic.AnsibleModule]::Create($args, $spec, @(Get-YoraiLeviTutorialTemplateUtilPowershellSpec))
    #>
    @{
        options = @{
            msg = @{ type = 'str'; required=$true}
        }
    }
}
$export_members = @{
    Function = "Get-YoraiLeviTutorialTemplateUtilPowershellSpec", "Invoke-YoraiLeviTutorialTemplateUtilPowershell"
}
Export-ModuleMember @export_members