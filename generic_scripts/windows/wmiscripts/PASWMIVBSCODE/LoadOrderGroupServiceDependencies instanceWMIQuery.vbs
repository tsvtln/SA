strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_LoadOrderGroupServiceDependencies",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_LoadOrderGroupServiceDependencies instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Antecedent: " & objItem.Antecedent
    Wscript.Echo "Dependent: " & objItem.Dependent
Next