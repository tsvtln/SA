
Dim obj

Set obj = WScript.CreateObject("Primalscript.LoginDlg")

obj.ShowDialog()

If obj.WasOk = True Then
	WScript.Echo obj.UserName
	WScript.Echo obj.Password
End If 






