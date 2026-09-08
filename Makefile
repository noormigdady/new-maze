.PHONY: run lint lint-strict clean

run:
	python3 amazing.py config.txt

lint:
	flake8
	mypy --warn-return-any --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8
	mypy --explicit-package-bases --strict .

debug:
	python3 -m pdb amazing.py config.txt

install:
	pip install -r requirements.txt

clean:
	rm -rf .mypy_cache
	rm maze.txt
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

env:
	python3 -m venv env
anal:
	python3 amazing.py config.txt
	python3 maze_analyzer.py maze.txt
