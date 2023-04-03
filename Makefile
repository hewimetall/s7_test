
all:install run
install:
	python -m env venv
	python -m pip install -r req.txt

run:
	source venv/bin/active && python main.py
tests:
	source venv/bin/active && python -m unittest discover "." "*_test.py"

.PHONY:tests, install, run