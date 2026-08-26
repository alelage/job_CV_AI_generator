.PHONY: setup install run test clean

# Detect native Windows (CMD/PowerShell) and block it with a helpful message
ifeq ($(OS),Windows_NT)
    # Check if SHELL is a Unix-like shell (bash, sh, zsh)
    # Git Bash and WSL set SHELL to something containing "bash" or "sh"
    # Native CMD/PowerShell does NOT.
    ifeq (,$(or $(findstring bash,$(SHELL)),$(findstring sh,$(SHELL)),$(findstring zsh,$(SHELL))))
        $(error Native Windows (CMD/PowerShell) is not supported. Please use WSL (Windows Subsystem for Linux) or Git Bash.)
    endif
endif

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
