'==========================================================================
'
'
' COMMENT: <ListWMIClassesInNameSpaceInputBox.vbs>
'1. makes WMI query for classes
'2. uses an InputBox to query for the namespace to search
'==========================================================================
Option Explicit
'On Error Resume Next
Dim StrComputer
Dim nSpace, Name, NameSpace
Dim objSWbemServices, colClasses, objClass
Dim msgOut ' holds results of query
strComputer = "."
'valid namespace:
'SECURITY,perfmon,RSOP,Cli,MSCluster,WMI,CIMV2,
'MicrosoftExchangeV2,MicrosoftActiveDirectory,
'MicrosoftIISv2,Policy,MicrosoftDNS,MicrosoftNLB,
'Microsoft,DEFAULT,directory,subscription
nSpace ="\root\"
Name = InputBox ("Type the NameSpace you want to browse" & Chr(13)& Chr(10) _
	& "valid classes are:" & Chr(13)& Chr(10)_
	& "SECURITY,perfmon,RSOP,Cli,MSCluster,WMI" & Chr(13)& Chr(10)_
	& "CimV2,MicrosoftExchangeV2,DEFAULT" & Chr(13)& Chr(10)_
	& "MicrosoftIISv2,Policy,MicrosoftDNS,MicrosoftNLB" & Chr(13)& Chr(10)_
	& "MicrosoftActiveDirectory,Microsoft,directory" & Chr(13)& Chr(10))
namespace = nspace & Name
WScript.echo "you want to search " & Namespace
Set objSWbemServices = _
    GetObject("winmgmts:\\" & strComputer & nameSpace)
Set colClasses = objSWbemServices.SubclassesOf()

For Each objClass In colClasses
   msgOut = msgout & objClass.Path_.Path & vbcrlf
Next
WScript.echo msgOUT