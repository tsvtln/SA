'==========================================================================
'
'
' COMMENT: <returns list of providers and their Class ID>
'1. The class ID is required to look the provider up in the registry
'2. In the registry you can find the name of the DLL the provider is contained
'3. in. 
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select name, clsid from __Win32Provider"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo objItem.name & vbtab & objItem.clsid
    
Next