
strComputer = "."
nSpace = "\root\cimv2"

Set objSWbemServices = _
    GetObject("winmgmts:\\" & strComputer & nSpace)
Set colClasses = objSWbemServices.SubclassesOf()

For Each objClass In colClasses
With objClass.path_
	strName= .Class
	If InStr(strName, "CIM") Then
		WScript.echo strName
	End If
End with
Next
