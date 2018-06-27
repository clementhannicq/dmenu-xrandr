.PHONY: build
build:
	@pipenv run pyinstaller --onefile dmenuxrandr/main.py -p ./dmenuxrandr

.PHONY: run
run:
	@pipenv run python dmenuxrandr/main.py
