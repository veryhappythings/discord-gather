.PHONY: test test-with-coverage

test:
	tox

test-with-coverage:
	tox
	coveralls
