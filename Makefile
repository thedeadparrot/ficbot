install_dependencies:
	pip install -r requirements.txt
	python -m nltk.downloader punkt

tests:
	python -m unittest -v test_generator