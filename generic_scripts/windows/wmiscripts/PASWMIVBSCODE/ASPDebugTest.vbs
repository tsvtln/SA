'==========================================================================
' COMMENT: Translated to VB from the JScript version
'==========================================================================

Option Explicit
Dim Debug

set Debug = CreateObject ("PrimalScript.ASPOutputDebug")

Debug.Initialize "localhost",500
if Debug.Error = 1 then
	WScript.Echo "Failed to allocate client socket!"
elseif Debug.Error = 2 then
	WScript.Echo "Failed to create client socket!"
elseif Debug.Error = 3 then
	WScript.Echo "Failed to connect"
end if	

Debug.OutputDebugString "Testing the ASP Debugger"
if Debug.Error = 4 then
	WScript.Echo "Failed to send on client socket"
end if

Debug.OutputDebugString "Testing second line"
if Debug.Error = 4 then
	WScript.Echo "Failed to send on client socket"
end if

Debug.OutputDebugString "ASP can now write to ports"
if Debug.Error = 4 Then
	WScript.Echo "Failed to send on client socket"
end if

Debug.OutputDebugString "On another machine"
if Debug.Error = 4 then
	WScript.Echo "Failed to send on client socket"
end if

Debug.OutputDebugString "On on localhost"
if Debug.Error = 4 then
	WScript.Echo "Failed to send on client socket"
end if

Debug.Close
Set Debug = nothing
