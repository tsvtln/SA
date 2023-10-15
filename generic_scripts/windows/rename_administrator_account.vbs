On Error Resume Next

strComputer = "."

Set WshShell = WScript.CreateObject("WScript.Shell")
Set WshNetwork = WScript.CreateObject("WScript.Network")
Set oReg = GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & "." & "\root\default:StdRegProv")

strComputer = WshNetwork.ComputerName

'Rename Administrator
Set oMachine = GetObject("WinNT://" & strComputer)
Set oInfoUser = GetObject("WinNT://" & strComputer & "/Administrator,user")
set oUser = oMachine.MoveHere(oInfoUser.ADsPath,"Biaa1")

Set oInfoUser = GetObject("WinNT://" & strComputer & "/Guest,user")
set oUser = oMachine.MoveHere(oInfoUser.ADsPath,"Biga1")