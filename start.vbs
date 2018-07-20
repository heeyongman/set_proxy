Function CurrentPath()
    strPath = Wscript.ScriptFullName
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.GetFile(strPath)
    CurrentPath = objFSO.GetParentFolderName(objFile)
End Function

strCurrentPath = CurrentPath()

strArgs = strCurrentPath & "\code\default\python27\1.0\python.exe " & strCurrentPath & "\code\default\launcher\start.py"
'WScript.Echo strArgs

Set oShell = CreateObject ("Wscript.Shell")
oShell.Run strArgs, 0