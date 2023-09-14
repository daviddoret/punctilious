$environment_directory = "build_docs_temp_venv"
$total_step = 3
$script = Split-Path $PSCommandPath -Leaf
$docs_build_path = $PSScriptRoot
$docs_build_path = Split-Path -Path $docs_build_path -Parent
$docs_build_path = "$( $docs_build_path )\docs\build"

$current_step = 1
Write-Host "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). python -m venv $( $environment_directory )"
$environment_directory = & $PSScriptRoot\start_venv.ps1

$current_step = 2
Write-Host "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). python -m venv $( $environment_directory )"
Invoke-Expression -Command "python -m sphinx -T -E -b html -d _build/doctrees -D language = en . $docs_build_path"

Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey();

$current_step = 3
Write-Host "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). python -m venv $( $environment_directory )"
& $PSScriptRoot\stop_venv.ps1 -EnvironmentDirectory $environment_directory
