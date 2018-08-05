help:
	@echo "ArcadeML: ML models learn how to play arcade games"
	@echo "Commands available: "
	@echo "  - setup: Install the Python application "
	@echo "  - start: Init the application "

setup:
	pip install -e .

start:
	cd src/arcademl; python main.py
