'==========================================================================
'
'
' COMMENT: <Find the MSI Provider>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strProv
Dim strMsg
strComputer = "."
wmiNS = "\root\cimv2"
strProv = "MSI"
Set objWMIService = _
    GetObject ("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.InstancesOf("__Win32Provider")

For Each objItem In colItems
With objItem
If InStr(1,.name, strProv,1) then
    WScript.echo .Name, .clsid _
    & vbcrlf & "hostingModel: " & .hostingModel
    
End If
End with
Next
