strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM CIM_ProcessExecutable",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "CIM_ProcessExecutable instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Antecedent: " & objItem.Antecedent
    Wscript.Echo "BaseAddress: " & objItem.BaseAddress
    Wscript.Echo "Dependent: " & objItem.Dependent
    Wscript.Echo "GlobalProcessCount: " & objItem.GlobalProcessCount
    Wscript.Echo "ModuleInstance: " & objItem.ModuleInstance
    Wscript.Echo "ProcessCount: " & objItem.ProcessCount
Next