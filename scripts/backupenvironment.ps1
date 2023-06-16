$environment = [Environment]::GetEnvironmentVariable('PATH', 'Machine');
Out-File cache\envbackup.txt -InputObject $environment -Force