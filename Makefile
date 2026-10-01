NAME = a_maze_ing.py
PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python
TMP = $(VENV)/.install

all: install

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

$(TMP): requirements.txt $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	$(PIP) install flake8 mypy
	touch $(TMP)

install: $(TMP)

run: install
	$(PYTHON_VENV) $(NAME) .env

debug: install
	$(PYTHON_VENV) -m pdb $(NAME) .env

lint: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all install run debug clean lint lint-strict fclean re
