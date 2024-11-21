PYTHON = python3
REQUIREMENTS = requirements.txt

install:
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

start:
	$(PYTHON) index.py

clean:
	find . -name "*.pyc" -exec rm -f {} \;
