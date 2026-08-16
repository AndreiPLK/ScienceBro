# Guard: запускает демон live-страницы, если он не работает.
$alive = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match 'live_status' }
if (-not $alive) {
    Start-Process -FilePath 'C:\Users\user\ScienceBro\.venv\Scripts\python.exe' `
        -ArgumentList '-u', 'C:\Users\user\ScienceBro\tools\live_status.py', '--daemon' `
        -WindowStyle Hidden
}
