
strComputer = "."
nSpace = "\root\Microsoft\homenet"
Set objDictionary = CreateObject("scripting.dictionary")

Set objSWbemServices = _
    GetObject("winmgmts:\\" & strComputer & nSpace)
Set colClasses = objSWbemServices.SubclassesOf()

For Each objClass In colClasses
    Wscript.Echo objClass.Path_.Path
Next
