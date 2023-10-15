strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_LogicalShareAccess",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_LogicalShareAccess instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "AccessMask: " & objItem.AccessMask
    Wscript.Echo "GuidInheritedObjectType: " & objItem.GuidInheritedObjectType
    Wscript.Echo "GuidObjectType: " & objItem.GuidObjectType
    Wscript.Echo "Inheritance: " & objItem.Inheritance
    Wscript.Echo "SecuritySetting: " & objItem.SecuritySetting
    Wscript.Echo "Trustee: " & objItem.Trustee
    Wscript.Echo "Type: " & objItem.Type
Next