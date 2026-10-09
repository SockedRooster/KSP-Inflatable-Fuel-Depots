@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-Plugin.ps1" %*
echo.
if errorlevel 1 (
  echo Build failed; the storage lock is NOT installed. Review the error above.
) else (
  echo You can now copy GameData\InflataDepot into your KSP GameData directory.
)
pause
