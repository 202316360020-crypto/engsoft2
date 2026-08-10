param(
    [string]$Name = "QuantInvest"
)

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $repoRoot

try {
    $python = ".\.venv\Scripts\python.exe"
    $portableRoot = Join-Path $repoRoot "portable"
    $workRoot = Join-Path $repoRoot "pyinstaller-build"

    if (-not (Test-Path $python)) {
        throw "Nao encontrei a virtualenv em .\.venv. Crie-a antes de empacotar a aplicacao."
    }

    if (Test-Path $portableRoot) {
        Remove-Item $portableRoot -Recurse -Force
    }

    if (Test-Path $workRoot) {
        Remove-Item $workRoot -Recurse -Force
    }

    & $python -m PyInstaller --noconfirm --clean --onedir --noconsole --name $Name --distpath $portableRoot --workpath $workRoot --collect-all flet run_app.py

    $portableApp = Join-Path $portableRoot $Name
    $zipPath = Join-Path $portableRoot "$Name-portable.zip"

    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }

    Compress-Archive -Path $portableApp -DestinationPath $zipPath -Force
}
finally {
    Pop-Location
}