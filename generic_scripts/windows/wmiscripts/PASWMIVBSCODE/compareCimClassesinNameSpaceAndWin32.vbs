'==========================================================================
' COMMENT: <takes list of cim classes, and compares win32 classes to it>
'
'==========================================================================
Option Explicit
On Error Resume next
dim strComputer, nSpace, objSWbemServices
Dim i, colClasses, objDictionary
Dim strClass, objClass
strComputer = "."
nSpace = "\root\cimv2"
i = 0'used to control which sub to go into.
Set objSWbemServices = _
    GetObject("winmgmts:\\" & strComputer & nSpace)
Set colClasses = objSWbemServices.SubclassesOf()
Set objDictionary = CreateObject("scripting.dictionary")

subAddCim
subCheckWin


Sub subAddCim 'adds cim names to dictionary
	For Each objClass In colClasses
	With objClass.path_
				If InStr(1,.Class, "cim",1) Then
				strClass = ucase(Mid(.Class, 5))
				'WScript.echo .class & vbtab & strClass'debug
				subDictionary
				else
			End If
	End With
	Next
i = 1
End Sub

Sub subCheckWin 'checks win names against dictionary
For Each objClass In colClasses
	With objClass.path_
				If InStr(1,.Class, "win",1) Then
				strClass = ucase(Mid(.Class, 7))
				'WScript.echo .class & vbtab & strClass'debug
				subDictionary
				else
			End If
	End With
Next
End Sub

WScript.echo "there are " & objdictionary.count & " items in dictionary"'debug

Sub subDictionary
'WScript.echo i & " is i. strClass is: " & strClass'debug
If i = 1 then
	If objDictionary.Exists(strClass) Then
	WScript.echo strClass
	End If
Else
	objDictionary.add strClass, strClass
End If

End sub
