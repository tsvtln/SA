'==========================================================================
'
' COMMENT: <Creates a dictionary of WMI namespaces and then lists providers>
'
'==========================================================================
Option Explicit
'On Error Resume Next
Dim strComputer, objDictionary
Dim objSWbemServices, objWMIservice
Dim colNameSpaces, objNamespace
Dim colProviders, objProvider
Dim wmiNS

strComputer = "."

Set objDictionary = CreateObject("scripting.dictionary")

SubEnumNameSpaces("root") 'creates listing of WMI Namespaces
subListProviders 'Creates listing of WMI Providers

'#### Subs and Functions are below ######

Sub SubEnumNameSpaces(strNameSpace)
objDictionary.add "\"& strNameSpace, "\"& strNameSpace
    Set objSWbemServices = _
        GetObject("winmgmts:\\" & strComputer & "\" & strNameSpace)
    Set colNameSpaces = objSWbemServices.InstancesOf("__NAMESPACE")
    For Each objNameSpace In colNameSpaces
        Call SubEnumNameSpaces(strNameSpace & "\" & objNameSpace.Name)
    Next
End Sub

Sub subListProviders
For Each wmiNS In objdictionary
set objWMIService = GetObject ("winmgmts:\\" & strComputer & wmiNS)
Set colProviders = objWMIService.InstancesOf("__Win32Provider")
	WScript.Echo myFun(wmiNS)
For Each objProvider In colProviders
    Wscript.Echo objProvider.Name
Next
next
End Sub

Function myFun(input)
Dim lstr
lstr = Len(input)
myFun = input & vbcrlf & string(lstr,"=")
End function
