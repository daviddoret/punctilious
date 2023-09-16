Set-Location $Env:USERPROFILE\PycharmProjects\punctilious
python -m pip install --upgrade twine
python -m twine upload --repository testpypi dist/*