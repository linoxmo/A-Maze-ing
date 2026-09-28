PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python

NAME = a_maze_ing.py
CONFIG = .env

all: install

$(VENV):
	$(PYTHON) -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r reauirements.txt

run: install
	$(PY) $(NAME) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf *.pyc

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all install run clean fclean re
