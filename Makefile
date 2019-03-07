.PHONY: clean upload

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	git push --tags; python setup.py sdist upload
