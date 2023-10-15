'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Uses win32_group and the is not null operator to determine descriptions
'2.
'3. 
'==========================================================================

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_group where Description is not Null"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "Description: " & objItem.Description 
    WScript.echo "Is description field null? " & IsNull(objItem.description) 
    Wscript.Echo "Domain: " & objItem.Domain 
    Wscript.Echo "LocalAccount: " & objItem.LocalAccount 
    Wscript.Echo "Name: " & objItem.Name 
    Wscript.Echo "SID: " & objItem.SID 
    Wscript.Echo "SIDType: " & objItem.SIDType
    WScript.echo "" 
Next
