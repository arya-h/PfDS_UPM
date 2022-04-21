
venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

run: venv/bin/activate
	python3 data-scraper.py 
	python3 portfolio_allocations.py
	python3 portfolio_metrics.py
	python3 analysis.py

clean:
	rm -rf __pycache__
	rm -rf venv


help:
	@echo "---------------HELP-----------------"
	@echo "geckodriver must be available in the path"
	@echo "To run the program type make run"
	@echo "To clear cache  type make clean"
	@echo "------------------------------------"

