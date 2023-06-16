$script_path = $PSCommandPath.replace(("\" + "runsetup.ps1"), '')
Start-Process powershell -ArgumentList ("Set-ExecutionPolicy Unrestricted; cd \`"${script_path}\`"; .\scripts\backupenvironment.ps1") -Verb runAs
Start-Process powershell -ArgumentList ("Set-ExecutionPolicy Unrestricted; cd \`"${script_path}\`"; .\scripts\setupbatch.ps1") -Verb runAs
Start-Process powershell -ArgumentList ("Set-ExecutionPolicy Unrestricted; cd \`"${script_path}\`"; .\scripts\setupenvironment.ps1") -Verb runAs