clean-pyenv:
	pip freeze | xargs pip uninstall -y
