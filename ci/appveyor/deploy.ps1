If ($env:PYTHON_VERSION -eq "3.9") {
	If ($env:APPVEYOR_REPO_TAG -eq "true") {
		Invoke-Expression "$env:PYTHON\\python.exe -m twine upload --skip-existing dist\\*"
	} Else {
		write-output "Not on a tag on master, won't deploy to PyPI"
	}
}
