
WScript.Echo(Now)
strComputer = "."
Call EnumNameSpaces("root")

Sub EnumNameSpaces(strNameSpace)
    Wscript.Echo strNameSpace
    Set objSWbemServices = _
        GetObject("winmgmts:\\" & strComputer & "\" & strNameSpace)
    Set colNameSpaces = objSWbemServices.InstancesOf("__NAMESPACE")
    For Each objNameSpace In colNameSpaces
        Call EnumNameSpaces(strNameSpace & "\" & objNameSpace.Name)
    Next
End Sub
WScript.Echo("all done " & Now)