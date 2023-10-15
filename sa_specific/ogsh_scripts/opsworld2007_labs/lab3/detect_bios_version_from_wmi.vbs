On Error Resume Next
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")
Set colItems = objWMIService.ExecQuery("Select * from Win32_BIOS where PrimaryBIOS = TRUE",,48)
 For Each objItem in colItems
  wscript.Echo objItem.Name
next
