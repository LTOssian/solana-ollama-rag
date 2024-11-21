PYTHON = python3
REQUIREMENTS = requirements.txt
VENV_DIR = env

install: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

$(VENV_DIR)/bin/activate: 
	$(PYTHON) -m venv $(VENV_DIR)

start:
	docker compose up -d
	$(VENV_DIR)/bin/python index.py

clean:
	rm -rf $(VENV_DIR)
	find . -name "*.pyc" -exec rm -f {} \;
