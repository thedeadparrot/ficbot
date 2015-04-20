install_dependencies:
	pip install -r requirements.txt
	python -m nltk.downloader punkt
run_tests:
	python -m unittest discover tests/
