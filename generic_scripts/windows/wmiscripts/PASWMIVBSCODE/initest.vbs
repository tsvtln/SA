
Dim obj

WScript.Echo "Test"

set obj = WScript.CreateObject("Primalscript.IniFile")

obj.WriteProfileString "Section","Key","Test","e:\test.ini"
obj.WriteProfileInt "Section","Key2",1,"E:\test.ini"
obj.WriteProfileString "Section2","Key","Test","e:\test.ini"
obj.WriteProfileInt "Section2","Key2",1,"E:\test.ini"

Dim NumKeys
Dim Pair

NumKeys = obj.GetProfileSection("Section","E:\test.ini")
WScript.Echo NumKeys

For i = 0 To NumKeys-1
	Pair = obj.KeyValuePairs(i)
	WScript.Echo Pair
Next

Dim KeyValue

KeyValue = obj.GetProfileString("Section","Key"," ","E:\test.ini")
WScript.Echo KeyValue
KeyValue = obj.GetProfileInt("Section","Key2",0,"E:\test.ini")
WScript.Echo KeyValue
