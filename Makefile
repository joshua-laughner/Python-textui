build: setup.py
	python3 setup.py sdist bdist_wheel --universal

upload: upload-test

upload-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload-public:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

clean:
	rm -r dist/ build/ *.egg-info/
