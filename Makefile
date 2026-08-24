.PHONY: setup install run test clean

VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@if [ ! -f credentials.json ]; then cp credentials.json.example credentials.json; fi

install:
	python3 -m pip install -r requirements.txt

run:
	$(PYTHON) -m streamlit run app.py

test:
	pytest tests

clean:
	rm -rf __pycache__ .pytest_cache $(VENV) *.pyc
