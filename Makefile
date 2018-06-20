.PHONY: build
build:
	@pipenv run pyinstaller --onefile main.py

.PHONY: run
run:
	@pipenv run python main.py
