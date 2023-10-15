
strComputer = "."
wmiNS = "\root\wmi"
Set objSWbemServices = _
    GetObject ("winmgmts:\\" & strComputer & wmiNS)
Set colWin32Providers = objSWbemServices.InstancesOf("__Win32Provider")

For Each objWin32Provider In colWin32Providers
    Wscript.Echo objWin32Provider.Name
Next

