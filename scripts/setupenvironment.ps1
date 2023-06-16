$currentDir = [string]$pwd
$oldEnvVar = [Environment]::GetEnvironmentVariable('CURRENTTITLEGENPATH','Machine');
$oldPath = [Environment]::GetEnvironmentVariable('PATH', 'Machine');
if ($oldEnvVar) {
	$oldPath = $oldPath.replace(($oldEnvVar + ";"), '')
}

if ($oldPath.Substring($oldPath.Length - 1) -ne ';') {
	$oldPath = $oldPath + ";"
}

[string]$newPath = $oldPath + $currentDir + ";"
[Environment]::SetEnvironmentVariable('PATH', "$newPath",'Machine');

[Environment]::SetEnvironmentVariable('CURRENTTITLEGENPATH', "$pwd",'Machine');