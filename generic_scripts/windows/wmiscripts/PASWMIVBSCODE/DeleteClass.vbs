
Dim service

Set service = GetObject("winmgmts:{impersonationLevel=impersonate}") 

Set objwbemobject= service.get("")

objwbemobject.Path_.Class = "MyNewClass" 
objwbemobject.put_
service.delete  "MyNewClass"
