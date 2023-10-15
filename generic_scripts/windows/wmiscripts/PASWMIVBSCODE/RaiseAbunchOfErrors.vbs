
On Error Resume NEXT
For i = 1 To 10000
Err.Raise(i)
If InStr(1,Err.Description, "unknown",1) Then
else
WScript.echo Err.Number & vbtab & Err.Description
End if
Err.Clear
NEXT