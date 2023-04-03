python_run = venv/bin/python

all: install run

install:
	python -m venv venv
	python -m pip install -r req.txt

run:
	${python_run} main.py

tests:
	${python_run} -m unittest discover "." "*_test.py"

generate:
	for i in $$(seq 1900 $x); do \
		for j in {00..$y}; do \
			for k in {00..$z}; do \
				cat 20221101_1234_DME.csv > test/in/$${i}$${j}$${k}_1234_DME.csv; \
				sleep $$time; \
			done; \
		done; \
	done


hard_test:
	mkdir -p test/in
	make generate x=1915 y=02 z=03 time=0
	make run &
	make generate x=1915 y=02 z=03 time=20
	killall python || true

clean:
	rm -rf venv
	rm -rf pycache
	rm -rf .pyc
	rm -rf test/
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf coverage.xml
	rm -rf .coverage

.PHONY: tests install run generate hard_test clean


