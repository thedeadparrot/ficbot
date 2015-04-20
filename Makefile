install_dependencies:
	pip install -r requirements.txt
	python -m nltk.downloader punkt
install_test_dependencies: install_dependencies
	pip install -r test-requirements.txt
run_tests:
	python -m unittest discover tests/
