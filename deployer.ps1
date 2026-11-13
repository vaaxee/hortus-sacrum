# Met l'app en ligne sur Vercel (projet hortus-sacrum), à partir de la version compilée.
# Usage, dans PowerShell depuis ce dossier :  & .\deployer.ps1
$ErrorActionPreference = 'Stop'
Push-Location app
npm.cmd run build
Pop-Location
if (Test-Path deploy\hortus-sacrum) { Remove-Item -Recurse -Force deploy\hortus-sacrum }
New-Item -ItemType Directory -Force deploy | Out-Null
Copy-Item -Recurse app\build deploy\hortus-sacrum
Push-Location deploy\hortus-sacrum
npx.cmd --yes vercel@latest deploy --prod --yes --scope gabriel3-06a3
Pop-Location
