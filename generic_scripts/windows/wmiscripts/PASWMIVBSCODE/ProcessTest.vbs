
Dim obj
Dim Max
Set obj = WScript.CreateObject("Primalscript.ProcessEnum")

Max = obj.Enumerate()

Dim Counter

For Counter = 0 To Max - 1
	WScript.Echo obj.Processes(Counter)
Next






