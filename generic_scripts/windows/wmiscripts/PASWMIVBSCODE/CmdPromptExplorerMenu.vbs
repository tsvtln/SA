'=====================================================================
'    Purpose: Add's a Cmd Prompt Here item to "Right-Click" context menu in Explorer
'               which opens a command prompt (DOS) window in the selected folder
'=====================================================================

Dim WSHShell
Set WSHShell = WScript.CreateObject("WScript.Shell")

WSHShell.RegWrite "HKCR\Folder\Shell\MenuText\Command\", "cmd.exe /k cd " & chr(34) & "%1" & chr(34)
WSHShell.RegWrite "HKCR\Folder\Shell\MenuText\", "Cmd Prompt Here"

