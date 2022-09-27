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
# public class AnsibleModule{
#     public delegate void ExitHandler(int rc);
#     public static ExitHandler Exit = new ExitHandler(ExitModule);
#     public delegate void WriteLineHandler(string line);
#     public static WriteLineHandler WriteLine = new WriteLineHandler(WriteLineModule);
#     public static bool _DebugArgSpec = false;
#     public Dictionary<string, object> Diff = new Dictionary<string, object>();
#     public IDictionary Params = null;
#     public Dictionary<string, object> Result = new Dictionary<string, object>() { { "changed", false } };
#     public bool CheckMode { get; private set; }
#     public bool DebugMode { get; private set; }
#     public bool DiffMode { get; private set; }
#     public bool KeepRemoteFiles { get; private set; }
#     public string ModuleName { get; private set; }
#     public bool NoLog { get; private set; }
#     public int Verbosity { get; private set; }
#     public string AnsibleVersion { get; private set; }
#     public string Tmpdir
#     public AnsibleModule(string[] args, IDictionary argumentSpec, IDictionary[] fragments = null);
#     public static AnsibleModule Create(string[] args, IDictionary argumentSpec, IDictionary[] fragments = null);
#     public void Debug(string message);
#     public void Deprecate(string message, string version);
#     public void Deprecate(string message, string version, string collectionName);
#     public void Deprecate(string message, DateTime date);
#     public void Deprecate(string message, DateTime date, string collectionName);
#     public void ExitJson();
#     public void FailJson(string message);
#     public void FailJson(string message, ErrorRecord psErrorRecord);
#     public void FailJson(string message, Exception exception);
#     public void LogEvent(string message, EventLogEntryType logEntryType = EventLogEntryType.Information, bool sanitise = true);
#     public void Warn(string message);
#     public static object FromJson(string json);
#     public static T FromJson<T>(string json);
#     public static string ToJson(object obj);
#     public static IDictionary GetParams(string[] args);
#     public static bool ParseBool(object value);
#     public static Dictionary<string, object> ParseDict(object value);
#     public static float ParseFloat(object value);
#     public static int ParseInt(object value);
#     public static string ParseJson(object value);
#     public static List<object> ParseList(object value);
#     public static string ParsePath(object value);
#     public static object ParseRaw(object value);
#     public static SecurityIdentifier ParseSid(object value);
#     public static string ParseStr(object value);
# }



## Requires -Module Ansible.ModuleUtils.template_util_powershell
## AnsibleRequires -PowerShell template_util_powershell
## Requires -Version 5
## AnsibleRequires -OSVersion 
## AnsibleRequires -Become

# Include the module util ServiceAuth.psm1 from the my_namespace.my_collection collection
#AnsibleRequires -PowerShell ..module_utils.TemplateUtilPowershell

# Create the module spec like normal
$spec = @{
    options = @{
        text = @{ type = 'str'; required = $true }
    }
}

# Create the module from the module spec but also include the util spec to merge into our own.
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec, @(Get-YoraiLeviTutorialTemplateUtilPowershellSpec))

#your code

#Example: Call the module util and pass in the module object so it can access the module options.
Invoke-YoraiLeviTutorialTemplateUtilPowershell -Module $module 

#your code
$text = $module.Params.text
$module.Result.text = $text

$module.ExitJson()