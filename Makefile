.PHONY: run lint lint-strict clean build
run:
	python3 a_maze_ing.py config.txt

lint:
	flake8
	mypy --warn-return-any --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8
	mypy --explicit-package-bases --strict .

debug:
	python3 -m pdb a_maze_ing.py config.txt

install: 
	pip install mazegen-1.0.0.tar.gz
	pip install mazegen-1.0.0-py3-none-any.whl

clean:
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

env:

	python3 -m venv env

build:
	pip install build
	python3 -m build
