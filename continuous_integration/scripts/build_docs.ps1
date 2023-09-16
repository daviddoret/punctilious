# This Powershell script roughly mimics the ReadTheDocs build scripts,
# but the build is executed locally from the dev environment.
# The key idea is to build the docs but simultaneously to verify
# that the ReadTheDocs build should be successful.

$total_step = 7
$script = Split-Path $PSCommandPath -Leaf
$script_folder = $PSScriptRoot
$project_folder = Split-Path -Path $script_folder -Parent
$docs_folder = "$( $project_folder )\docs"
$docs_build_folder = "$( $docs_folder )\build"

$current_step = 1
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). start_venv.ps1"
$environment_directory = & $PSScriptRoot\start_venv.ps1

$current_step = 2
$command = "python -m pip install --upgrade --no-cache-dir pip setuptools"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command

$current_step = 3
$command = "python -m pip install --upgrade --no-cache-dir sphinx readthedocs-sphinx-ext"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command

$current_step = 4
$command = "python -m pip install --exists-action=w --no-cache-dir -r $( $docs_folder )\requirements.txt"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command

$current_step = 5
$command = "python -m pip install --exists-action=w --no-cache-dir -r $( $project_folder )\requirements.txt"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command

$current_step = 6
$command = "python -m sphinx -T -E -b html -d _build/doctrees -D language=en $docs_folder $docs_build_folder"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command

$current_step = 7
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). stop_env.ps1"
& $PSScriptRoot\stop_venv.ps1 -EnvironmentDirectory $environment_directory
